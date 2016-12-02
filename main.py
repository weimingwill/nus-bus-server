import requests
import json
import settings
from collections import defaultdict
from math import sqrt, atan2, sin, cos
from entities import LoginCredential, LoginToken, BusStop, Shuttle, VehicleServiceMap

from flask import Flask

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route("/bus_location", methods=['GET'])
def get_bus_location():
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
    query = LoginToken.query().order(-LoginToken.time)
    token = query.get()
    if token:
        app.logger.info("token: {}".format(token.id))
        resp = send_bus_location_request(token.id)
        if resp.status_code == 200:
            return resp.content

    token_id = get_credentials()
    if not token_id:
        return "Invalid login credential"

    resp = send_bus_location_request(token_id)
    return resp.content


def send_bus_location_request(token_id):
    payload = {"token": token_id}
    resp = requests.get(settings.BUS_TRACKING_BUS_LOCATION_URL, params=payload)
    return resp


def filter_moving_buses(buses):
    app.logger.info("filter moving buses")
    buses_dict = defaultdict(list)
    for bus in buses:
        bus["service"] = ""
        buses_dict[bus[settings.VEHICLE_SERIAL_KEY]].append(bus)
    app.logger.info("buses_dict: {}".format(str(buses_dict)))

    new_buses = []

    for buses in buses_dict.values():
        i = 0
        is_moving = False
        for i in xrange(0, len(buses) - 1):
            if buses[i][settings.LATITUDE] != buses[i + 1][settings.LATITUDE] \
                    or buses[i][settings.LONGITUDE] != buses[i + 1][settings.LONGITUDE]:
                is_moving = True
                break
        if is_moving:
            new_buses.append(buses[i + 1])
    app.logger.info("new buses: {}".format(str(new_buses)))
    return new_buses


# @app.route("/calculate_bus_service")
# def calculate_bus_service():
#     """
#     To calculate bus service number. Need to improve the algorithm
#     :return:
#     """
#     buses = json.loads(get_bus_location()[0])
#     app.logger.info("buses: " + str(buses))
#
#     vehicle_service_dict = {}
#     busstops = get_busstops()
#     for busstop in busstops:
#         shuttles = get_shuttle(busstop.name)
#         min_distance = 1000
#         for bus in buses:
#             distance = calculate_distance(busstop.latitude, busstop.longitude,
#                                           bus[settings.LATITUDE], bus[settings.LONGITUDE])
#             for shuttle in shuttles:
#                 if shuttle.arrivalTime != "-" \
#                         and (shuttle.arrivalTime == "Arr" or int(shuttle.arrivalTime) < 2) \
#                         and distance < 10:
#                     if distance < min_distance:
#                         min_distance = distance
#                         vehicle_service_dict.update({bus[settings.VEHICLE_SERIAL_KEY]: shuttle.name})
#                 else:
#                     vehicle_service_dict.update({bus[settings.VEHICLE_SERIAL_KEY]: ""})
#             # if distance < min_distance:
#             #     min_distance = distance
#             #     min_arrival_time = 60
#             #     for shuttle in shuttles:
#             #         if shuttle.arrivalTime == "Arr":
#             #             vehicle_service_dict.update({bus[settings.VEHICLE_SERIAL_KEY]: shuttle.name})
#             #             break
#             #         elif shuttle.arrivalTime != "-":
#             #             arrival_time = int(shuttle.arrivalTime)
#             #             if min_arrival_time > arrival_time:
#             #                 min_arrival_time = arrival_time
#             #                 vehicle_service_dict.update({bus[settings.VEHICLE_SERIAL_KEY]: shuttle.name})
#
#     app.logger.info("vehicle_service_dict: " + str(vehicle_service_dict))
#     vehicle_services = VehicleServiceMap.get_all()
#     if vehicle_services:
#         app.logger.info("update vehicle service map")
#         for vehicle, service in vehicle_service_dict.iteritems():
#             for vehicle_service in vehicle_services:
#                 if vehicle_service.vehicle == vehicle:
#                     vehicle_service.service = service
#                     vehicle_service.put()
#     else:
#         app.logger.info("initiate vehicle service map")
#         for vehicle, service in vehicle_service_dict.iteritems():
#             vehicle_service = VehicleServiceMap(vehicle=vehicle, service=service)
#             vehicle_service.put()
#     return "", 200


def get_busstops():
    resp = requests.get(settings.BUSSTOPS_URL)
    data = json.loads(resp.content)
    busstops = data[settings.BUSSTOP_RESULT_KEY][settings.BUSSTOPS_KEY]
    busstop_list = []
    for busstop_json in busstops:
        busstop = BusStop.serialize(busstop_json)
        busstop_list.append(busstop)
    return busstop_list


def get_shuttle(busstop):
    payload = {'busstopname': busstop}
    resp = requests.get(settings.SHUTTLE_URL, params=payload)
    data = json.loads(resp.content)
    shuttles = data[settings.SHUTTLE_RESULT_KEY][settings.SHUTTLES_KEY]
    shuttle_list = []
    for shuttle_json in shuttles:
        shuttle = Shuttle.serialize(shuttle_json)
        shuttle_list.append(shuttle)
    return shuttle_list


def calculate_distance(lat1, lon1, lat2, lon2):
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def get_credentials():
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