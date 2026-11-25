from datetime import timedelta
from api.domain.raw_api_data.bus_observation import BusObservation
from api.workflows.live_bus_assignment_builder.block_id_inference.block_candidate_provider import BlockCandidateProvider
from api.workflows.live_bus_assignment_builder.block_id_inference.live_trip_provider import LiveTripProvider
from gtfs.domain.values.winnipeg_block_id import WinnipegBlockID


def infer_block_id(
        observations: list[BusObservation],
        service_id: str,
        block_id_loader: BlockCandidateProvider,
        trip_loader: LiveTripProvider,
) -> WinnipegBlockID | None:
    """
    Infers a single block ID within the given service pattern from the given
    list of bus observations. The algorithm consists of two phases, and
    terminates as soon as the number of candidate block IDs is one (return that
    block ID) or zero (return None).
    The first phase uses the given BlockCandidateProvider to load candidate
    block IDs for each observation, and finds the intersection of those
    candidate sets.
    The second phase retrieves the trips associated with the bus observations,
    and uses the stop visits therein to further narrow down the candidate set.

    In practice, a single observation is sufficient in ~90% of cases to
    determine the block ID. Using all observations, a block ID can be inferred
    ~95% of the time. The expensive trip-comparison phase is therefore rarely
    executed.
    """
    block_id_candidates: set | None = None

    block_id_candidates = _update_block_id_candidates_from_live_observations(
        block_id_loader=block_id_loader,
        block_id_candidates=block_id_candidates,
        observations=observations,
        service_id=service_id
    )

    if block_id_candidates is None:
        return None
    elif len(block_id_candidates) == 1:
        return block_id_candidates.pop()

    block_id_candidates = _update_block_id_candidates_from_trip_schedules(
        block_id_loader=block_id_loader,
        block_id_candidates=block_id_candidates,
        trip_loader=trip_loader,
        trip_keys=_get_distinct_trip_keys(observations),
        service_id=service_id
    )

    if block_id_candidates is not None and len(block_id_candidates) == 1:
        return block_id_candidates.pop()

    return None

def _update_block_id_candidates_from_live_observations(
        block_id_candidates: set[WinnipegBlockID] | None,
        observations: list[BusObservation],
        service_id: str,
        block_id_loader: BlockCandidateProvider
) -> set[WinnipegBlockID] | None:
    """
    Compares the given list of bus observations with stop visits obtained from
    the given BlockCandidateProvider to narrow the given set of block ID
    candidates.
    """
    for obs in observations:
        block_id_candidates = _update_block_id_candidates_from_data_point(
            block_id_loader=block_id_loader,
            block_id_candidates=block_id_candidates,
            service_id=service_id,
            stop_id=obs.stop_id,
            scheduled_arrival=obs.scheduled_arrival,
            scheduled_departure=obs.scheduled_departure
        )

        if not block_id_candidates:
            return None
        elif len(block_id_candidates) == 1:
            return block_id_candidates

    return block_id_candidates

def _update_block_id_candidates_from_trip_schedules(
        block_id_candidates: set[WinnipegBlockID],
        trip_keys: list[str],
        service_id: str,
        block_id_loader: BlockCandidateProvider,
        trip_loader: LiveTripProvider,
) -> set[WinnipegBlockID] | None:
    """
    Compares stop visits obtained from trips with stop visits obtained from
    the given BlockCandidateProvider to narrow the given set of block
    ID candidates.
    """
    print("Falling back on trip schedule...")

    for key in trip_keys:
        trip = trip_loader.get_live_trip(key)

        for visit in trip.stop_visits:
            block_id_candidates = _update_block_id_candidates_from_data_point(
                block_id_loader=block_id_loader,
                block_id_candidates=block_id_candidates,
                service_id=service_id,
                stop_id=visit.stop_id,
                scheduled_arrival=visit.scheduled_arrival,
                scheduled_departure=visit.scheduled_departure
            )

            if not block_id_candidates:
                return None
            elif len(block_id_candidates) == 1:
                return block_id_candidates

    return block_id_candidates

def _update_block_id_candidates_from_data_point(
        block_id_candidates: set[WinnipegBlockID] | None,
        service_id: str,
        stop_id: str,
        scheduled_arrival: timedelta | None,
        scheduled_departure: timedelta | None,
        block_id_loader: BlockCandidateProvider
) -> set[WinnipegBlockID]:
    """
    Obtains all block IDs containing a stop visit matching the given
    information, then uses that set to narrow the given set of block ID
    candidates.
    """
    current_block_id_candidates = set(block_id_loader.get_possible_block_ids(
        service_id=service_id,
        stop_id=stop_id,
        scheduled_arrival=scheduled_arrival,
        scheduled_departure=scheduled_departure
    ))

    if block_id_candidates is None:
        block_id_candidates = current_block_id_candidates
    else:
        block_id_candidates = block_id_candidates.intersection(
            current_block_id_candidates
        )

    return block_id_candidates

def _get_distinct_trip_keys(
        observations: list[BusObservation]
) -> list[str]:
    """
    Returns a list containing all distinct trip keys in the given bus
    observations.
    """
    return list(set(
        o.trip_key for o in observations
    ))