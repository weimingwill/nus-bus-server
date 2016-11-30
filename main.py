import requests
import json
import settings
from math import pow, sqrt
from entities import LoginCredential, LoginToken, BusStop, Shuttle

from flask import Flask, request, abort

app = Flask(__name__)


@app.route('/')
def hello():
    """Return a friendly HTTP greeting."""
    return 'Hello World!'


@app.route("/bus_location", methods=['GET'])
def get_bus_location():
    query = LoginToken.query().order(-LoginToken.time)
    token = query.get()
    if token:
        app.logger.info("token: {}".format(token.id))
        resp = send_bus_location_request(token.id)
        if resp.status_code == 200:
            return resp.content, 200

    token_id = get_credentials()
    if not token_id:
        return "Invalid login credential", 400

    resp = send_bus_location_request(token_id)
    buses = json.loads(resp.content)
    buses = put_bus_service(buses)
    data = json.dumps(buses)
    return data, 200


def send_bus_location_request(token_id):
    payload = {"token": token_id}
    resp = requests.get(settings.BUS_TRACKING_BUS_LOCATION_URL, params=payload)
    return resp


def put_bus_service(buses):
    busstops = get_busstops()
    for busstop in busstops:
        shuttles = get_shuttle(busstop.name)
        for shuttle in shuttles:
            if shuttle.arrivalTime != "-" and (shuttle.arrivalTime == "Arr" or int(shuttle.arrivalTime) < 2):
                for bus in buses:
                    distance = calculate_distance(busstop.latitude, busstop.longitude,
                                                  bus[settings.LATITUDE], bus[settings.LONGITUDE])
                    shuttle_name = shuttle.name
                    if distance >= 200:
                        shuttle_name = ""
                    bus[settings.BUS_SERVICE_KEY] = shuttle_name
    return buses


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
    return sqrt(pow(lon1 - lon2, 2) + pow(lat1 - lat2, 2))

# @app.route('/get_login_token', methods=['GET'])
# def get_login_token():
#     data = {"domain": settings.DOMAIN, "name": settings.USERNAME, "password": settings.PWD}
#     resp = requests.post(settings.BUS_TRACKING_LOGIN_URL, data)
#     return resp.content, 200


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


if __name__ == "__main__":
    app.run()
