import requests
import json
import settings
from collections import defaultdict
from utils import calculate_distance, match_route_pattern
from entities import LoginCredential, LoginToken, BusStop, Shuttle, VehicleServiceMap, VehicleBusstopsMap

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route("/bus_location", methods=['GET'])
def get_bus_location():
    """
    Get moving buses with services number
    :return:
    """
    buses = json.loads(get_origin_bus_locations())
    buses = filter_moving_buses(buses)

    # vehicle_services = VehicleServiceMap.get_all()
    # if vehicle_services:
    #     for bus in buses:
    #         for vehicle_service in vehicle_services:
    #             if bus[settings.VEHICLE_SERIAL_KEY] == vehicle_service.vehicle:
    #                 bus["service"] = vehicle_service.service
    buses = json.dumps(buses)
    return buses, 200


def get_origin_bus_locations():
    """
    Get all buses locations.
    :return:
    """
    query = LoginToken.query().order(-LoginToken.time)
    token = query.get()
    if token:
        app.logger.info("token: {}".format(token.id))
        resp = send_bus_location_request(token.id)
        if resp.status_code == 200:
            return resp.content

    # Get new token if current token is expired.
    token_id = get_credentials()
    if not token_id:
        return "Invalid login credential"

    resp = send_bus_location_request(token_id)
    return resp.content


def send_bus_location_request(token_id):
    """
    Http request to third party API to get all buses
    :param token_id:
    :return:
    """
    payload = {"token": token_id}
    resp = requests.get(settings.BUS_TRACKING_BUS_LOCATION_URL, params=payload)
    return resp


def filter_moving_buses(buses):
    """
    Filter out stopped buses, for showing only moving buses.
    If latitude and longitude of a bus doesn't change, it means that bus is not moving.
    :param buses: list of all running buses
    :return:
    """
    app.logger.info("filter moving buses")
    buses_dict = defaultdict(list)
    for bus in buses:
        bus["service"] = ""
        buses_dict[bus[settings.VEHICLE_SERIAL_KEY]].append(bus)

    moving_buses, stopped_buses = [], []

    for buses in buses_dict.values():
        i = 0
        is_moving = False
        for i in xrange(0, len(buses) - 1):
            if buses[i][settings.LATITUDE] != buses[i + 1][settings.LATITUDE] \
                    or buses[i][settings.LONGITUDE] != buses[i + 1][settings.LONGITUDE]:
                is_moving = True
                break
        if is_moving:
            moving_buses.append(buses[i + 1])
        else:
            stopped_buses.append(buses[i + 1])

    # VehicleBusstopsMap.reset_stopped_buses(stopped_buses)
    return moving_buses


# @app.route("/calculate_bus_service", methods=["GET"])
# def calculate_bus_service():
#     """
#     To calculate bus service number. Need to improve the algorithm
#     By comparing the busstops a busstop has passed with bus service routine busstops.
#     :return:
#     """
#     buses = json.loads(get_bus_location()[0])
#     busstops = BusStop.get_busstops()
#
#     vehicle_busstops = VehicleBusstopsMap.get_all()
#     vehicle_busstops_dict = VehicleBusstopsMap.entities_to_dict(vehicle_busstops)
#     updated_busstops_dict = {}
#
#     for bus in buses:
#         vehicle_serial = bus[settings.VEHICLE_SERIAL_KEY]
#         min_distance = 1000
#         closest_busstop = ""
#         for busstop in busstops:
#             distance = calculate_distance(busstop.latitude, busstop.longitude,
#                                           bus[settings.LATITUDE], bus[settings.LONGITUDE])
#             if distance < 5 and distance < min_distance:
#                 min_distance = distance
#                 closest_busstop = busstop.name
#         new_vehicle_busstops = [closest_busstop]
#         if vehicle_serial in vehicle_busstops_dict.keys():
#             new_vehicle_busstops = vehicle_busstops_dict[vehicle_serial]
#             new_vehicle_busstops.append(closest_busstop)
#
#         new_vehicle_busstops = list(set(new_vehicle_busstops))
#         updated_busstops_dict[vehicle_serial] = new_vehicle_busstops
#
#     app.logger.info("updated_busstops_dict: " + str(updated_busstops_dict))
#
#     vehicle_service_dict = {}
#     for vehicle, busstops in updated_busstops_dict.iteritems():
#         if len(busstops) < 2:
#             vehicle_service_dict[vehicle] = ""
#         else:
#             bus_services = ""
#             for service, route_stops in settings.BUS_SERVICE_STOPS_DICT:
#                 if match_route_pattern(busstops, route_stops):
#                     if not bus_services:
#                         bus_services += service
#                     else:
#                         bus_services += "/" + service
#             app.logger.info("result bus services: " + bus_services)
#             vehicle_service_dict[vehicle] = bus_services
#
#     app.logger.info("create or update vehicle busstops map")
#     app.logger.info("vehicle busstops: {}, updated_busstops_dict: {}".format(str(vehicle_busstops), str(updated_busstops_dict)))
#     VehicleBusstopsMap.create_or_update(vehicle_busstops, updated_busstops_dict)
#     app.logger.info("update vehicle service map, vehicle_service_dict: " + str(vehicle_service_dict))
#     VehicleServiceMap.update(vehicle_service_dict)
#     return "", 200


def get_shuttle(busstop):
    """
    Send http request to shuttle API provider to get shuttle details
    :param busstop: string, busstop name
    :return: list of shuttles
    """
    payload = {'busstopname': busstop}
    resp = requests.get(settings.SHUTTLE_URL, params=payload)
    data = json.loads(resp.content)
    shuttles = data[settings.SHUTTLE_RESULT_KEY][settings.SHUTTLES_KEY]
    shuttle_list = []
    for shuttle_json in shuttles:
        shuttle = Shuttle.serialize(shuttle_json)
        shuttle_list.append(shuttle)
    return shuttle_list


def get_credentials():
    """
    Get credential form ndb to get login token.
    :return:
    """
    query = LoginCredential.query(LoginCredential.domain == settings.DOMAIN,
                                  LoginCredential.name == settings.USERNAME)
    credential = query.get()
    if credential:
        data = {"domain": credential.domain, "name": credential.name, "password": credential.password}
        resp = requests.post(settings.BUS_TRACKING_LOGIN_URL, data)
        data = json.loads(resp.content)
        if "token" in data.keys():
            token_id = data["token"]
            token = LoginToken(id=token_id)
            token.put_async()
            return token_id


# @app.route("/set_credential", methods=['POST'])
# def set_credential():
#     if not request.get_json() \
#             or 'domain' not in request.get_json() \
#             or 'name' not in request.get_json() \
#             or 'password' not in request.get_json():
#         abort(400)
#     data = request.get_json()
#     credential = LoginCredential(domain=data['domain'], name=data['name'], password=data['password'])
#     credential.put()
#     return "", 200


@app.errorhandler(404)
def page_not_found(e):
    """Return a custom 404 error."""
    return 'Sorry, Nothing at this URL.', 404


@app.errorhandler(500)
def application_error(e):
    """Return a custom 500 error."""
    return 'Sorry, unexpected error: {}'.format(e), 500