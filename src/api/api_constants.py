# BUS
MIN_YEAR = 1990

# API REQUESTS
WINNIPEG_TRANSIT_API_STOP_SCHEDULE_BASE_URL = "https://api.winnipegtransit.com/v4/stops"
WINNIPEG_TRANSIT_API_TRIP_SCHEDULE_BASE_URL = "https://api.winnipegtransit.com/v4/trips"

# CRITICAL STOPS
# Fun fact: these were determined using an approximation algorithm for the
# Set Cover problem.
CRITICAL_STOP_IDS = [
    "10159", "17007", "40196", "10803", "10657", "61253", "37003", "10562",
    "10158", "30893", "11037", "40195", "60475", "30789", "10289", "60672",
    "20600", "62015", "10907", "40800", "60746", "50617", "61279", "50616",
    "40889", "50311", "50310", "61278", "10087", "37005", "20200", "10881",
    "20468", "61277", "10010", "50210", "40466", "30366", "40052", "20456",
    "10908", "10627", "61155", "10090", "10632", "30078", "40900", "50192",
    "10001", "20019", "60577", "10131", "10303", "20227", "30364", "61159"
]