from gtfs.csv_parsing.route_parser import parse_routes
from gtfs.error_messages import get_err_msg

try:
    routes = parse_routes("routes.txt")
    for route in routes:
        print(route.id, route.long_name if not None else "")
except Exception as e:
    print(get_err_msg(e))