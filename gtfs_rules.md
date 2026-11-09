# GTFS Rules

This document establishes rules for GTFS entities in the tracker. Many of these
rules come from the official GTFS specification, while others are specific to
this implementation.
Some of the unofficial rules are inferred from years of historical Winnipeg
Transit GTFS archives, while others are enforced because they affect the core
functionality of the tracker.
The purpose of this document is to serve as an overarching source of truth for 
these rules, to which domain invariants and parsers/validators must adhere to.

## Agency

Agency objects are parsed from `agency.txt`. Some attributes included in Winnipeg
Transit's `agency.txt` are omitted. 
* `agency_name`, `agency_url`, and `agency_timezone` are required.
* `agency_name` cannot be empty or only whitespace.
* `agency_url` must be a valid URL according to the `validators` package.
* `agency_timezone` must represent a valid IANA timezone.
* Only one agency is permitted.

The official GTFS specification allows for more than one agency, but this
introduces additional complexity in many files, and is not a realistic
possibility in the near future of Winnipeg.

## Feed Info

The feed info object is parsed from `feed_info.txt`. Some attributes included in
Winnipeg Transit's `feed_info.txt` are omitted.
* `feed_publisher_name` and `feed_publisher_url` are required.
* `feed_publisher_name` cannot be empty or only whitespace.
* `feed_publisher_url` must be a valid URL according to the `validators` 
package.
* If `feed_start_date` or `feed_end_date` are absent, they are set to default
values which are essentially boundless (e.g. the year 1000 for the start date
and the year 3000 for the end date).
* If both `feed_start_date` and `feed_end_date` are present, `feed_start_date`
cannot come after `feed_end_date`.
* Only one feed info is permitted.

## Route

Route objects are parsed from `routes.txt`. The following rules are enforced on
routes:
* `route_id` and `route_type` are required.
* One of `route_short_name` and `route_long_name` is required.
* `route_id` cannot be empty or only whitespace.
* If present, `route_short_name` cannot be empty or only whitespace.
* If present, `route_long_name` cannot be empty or only whitespace.
* If present, `route_url` must be a valid URL according to the 
`validators` package.
* If present, `route_color` and `route_text_color` must consist of exactly six 
hexadecimal characters.
* If absent, `route_color` and `route_text_color` are set to default values.
* If present, `route_sort_order` must be non-negative.
* No two routes can share the same `route_id`.

## Stop

Stop objects are parsed from `stops.txt`. The following rules are enforced on
stops:
* `stop_id`, `stop_name`, and stop coordinates (`stop_lat`, and `stop_lon`) are 
required.
* `stop_id` cannot be empty or only whitespace.
* `stop_name` cannot be empty or only whitespace.
* If present, `stop_url` must be a valid URL according to the 
`validators` package.
* `stop_lat` must be a floating point value in the interval [-90, 90].
* `stop_lon` must be a floating point value in the interval [-180, 180].
* No two stops can share the same `stop_id`.

## Service Pattern

Service pattern objects are parsed from `calendar.txt`. The following rules are
enforced on service patterns:
* `service_id`, `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, 
`friday`, `saturday`, `start_date`, and `end_date` are required.
* `service_id` cannot be empty or only whitespace.
* `sunday`, `monday`, `tuesday`, `wednesday`, `thursday`, `friday`, and 
`saturday` must be 0 or 1.
* `start_date` and `end_date` must be in YYYYMMDD format.
* `start_date` cannot occur after `end_date`.
* No two service patterns can share the same `service_id`.

## Service Pattern Override

Service pattern override objects are parsed from `calendar_dates.txt`, and are
stored within their respective service pattern objects. The following rules are
enforced on service pattern overrides:
* `service_id`, `date`, and `exception_type` are required.
* `service_id` cannot be empty or only whitespace.
* `service_id` must correspond to a service ID in `calendar.txt`.
* `date` must be in YYYYMMDD format.
* At most one service pattern override can be associated with the same date for
the same service pattern.

## Shape & Shape Point

Shape objects are composed of shape point objects parsed from `shapes.txt`. The
following rules are enforced on shapes and shape points:
* `shape_id`, `shape_pt_lat`, `shape_pt_lon`, and `shape_pt_sequence` are 
required.
* `shape_id` cannot be empty or only whitespace.
* `shape_pt_lat` must be a floating point value in the interval [-90, 90].
* `shape_pt_lon` must be a floating point value in the interval [-180, 180].
* `shape_pt_sequence` must be non-negative.
* `shape_pt_sequence` must be unique within the same shape.
* No two shapes can share the same `shape_id`.

# Stop Visit

Stop visit objects are parsed from `stop_times.txt`. The following rules are
enforced on stop visits:
* `trip_id`, `stop_id`, `arrival_time`, `departure_time`, and `stop_sequence`
are required.
* `trip_id` cannot be empty or only whitespace.
* `stop_id` cannot be empty or only whitespace.
* `trip_id` must correspond to a trip ID in `trips.txt`.
* `stop_id` must correspond to a stop ID in `stops.txt`.
* `arrival_time` cannot come after `departure_time`.
* `stop_sequence` must be non-negative.
* `stop_sequence` must be unique within the same trip.

The `arrival_time` and `departure_time` fields are not strictly required by
official GTFS rules, but they are crucial to the purpose of this tracker and
have historically been included in Winnipeg Transit's feed.

# Trip

Trip objects are parsed from `trips.txt`. The following rules are enforced on
trips:
* `trip_id`, `route_id`, `service_id`, and `block_id` are required.
* `trip_id` cannot be empty or only whitespace.
* If present, `trip_headsign` cannot be empty or only whitespace.
* `route_id` must correspond to a route ID in `routes.txt`.
* `stop_id` must correspond to a stop ID in `stops.txt`.
* `service_id` must correspond to a service ID in `calendar.txt`.
* If present, `shape_id` must correspond to a shape ID in `shapes.txt`.
* If present, `direction_id` must be 0 or 1.
* `block_id` must be of the form #-#-# (where # represents a non-negative 
integer).
* `service_id` must match the first token of `block_id`.
* No two trips can share the same `trip_id`.

The `block_id` field is not strictly required by official GTFS rules, and does
not have to follow a specific format, but this attribute is crucial to the
purpose of this tracker, and Winnipeg Transit has always used the #-#-# format
historically.