# API Queries

The following is a list of potential API queries to implement. They cover both
live and historical data.

## Live Data

* Given a bus tracking number, returned detailed location information, including:
  * The block ID
  * The route
  * The next stop, based on the query time.
    * Include the stop ID, name, coordinates, scheduled/estimated arrival and 
    departure times.
  
* Given a set of filters, return all scheduled/active buses matching the given 
criteria, along with their corresponding block IDs. Filters include:
  * A range of tracking numbers
  * The model of the bus
  * The year of the bus
  * The length of the bus
  * The propulsion type of the bus
  * A route
  * A specific block ID

* Given a stop ID, return:
  * Stop information
    * ID, stop code, and name
    * Coordinates
    * Url
  * A list of upcoming arrivals
    * Vehicle information
      * Tracking number
      * Year and model
      * Length
      * Propulsion type
    * Assigned block ID
    * Route being served
    * Scheduled departure time
    * Minutes early/late according to estimated departure time

## Historical Data

* Given a bus tracking number, return detailed historical information, including:
  * Vehicle information
  * All recorded block IDs by date
  * All routes served

* Given a set of filters, return all block IDs and routes served by the buses
matching the given criteria. Filters include:
    * A range of tracking numbers
    * The model of the bus
    * The year of the bus
    * The length of the bus
    * The propulsion type of the bus

* Given a block ID, return a list of buses that were assigned to it by date.