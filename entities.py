import settings

from google.appengine.ext import ndb


class LoginCredential(ndb.Model):
    domain = ndb.StringProperty()
    name = ndb.StringProperty()
    password = ndb.StringProperty()


class LoginToken(ndb.Model):
    id = ndb.StringProperty()
    time = ndb.DateTimeProperty(auto_now=True)


class BusStop(ndb.Model):
    caption = ndb.StringProperty()
    name = ndb.StringProperty()
    latitude = ndb.FloatProperty()
    longitude = ndb.FloatProperty()

    @classmethod
    def serialize(cls, busstop_json):
        busstop = BusStop()
        busstop.caption = busstop_json["caption"]
        busstop.name = busstop_json["name"]
        busstop.latitude = float(busstop_json[settings.LATITUDE])
        busstop.longitude = float(busstop_json[settings.LONGITUDE])
        return busstop

    @classmethod
    def get_busstops(cls):
        # resp = requests.get(settings.BUSSTOPS_URL)
        # data = json.loads(resp.content)
        busstops = settings.BUSSTOPS[settings.BUSSTOP_RESULT_KEY][settings.BUSSTOPS_KEY]
        busstop_list = []
        for busstop_json in busstops:
            busstop = BusStop.serialize(busstop_json)
            busstop_list.append(busstop)
        return busstop_list


class Shuttle(ndb.Model):
    arrivalTime = ndb.StringProperty()
    nextArrivalTime = ndb.StringProperty()
    name = ndb.StringProperty()

    @classmethod
    def serialize(cls, shuttle_json):
        shuttle = Shuttle()
        shuttle.name = shuttle_json["name"]
        shuttle.arrivalTime = shuttle_json["arrivalTime"]
        shuttle.nextArrivalTime = shuttle_json["nextArrivalTime"]
        return shuttle


class VehicleServiceMap(ndb.Model):
    vehicle = ndb.StringProperty()
    service = ndb.StringProperty()

    @classmethod
    def get_all(cls):
        result = VehicleServiceMap.query().fetch(100)
        return result

    @classmethod
    def update(cls, vehicle_service_dict):
        vehicle_services = VehicleServiceMap.get_all()
        if vehicle_services:
            for vehicle, service in vehicle_service_dict.iteritems():
                for vehicle_service in vehicle_services:
                    if vehicle_service.vehicle == vehicle:
                        vehicle_service.service = service
                        vehicle_service.put()
        else:
            for vehicle, service in vehicle_service_dict.iteritems():
                vehicle_service = VehicleServiceMap(vehicle=vehicle, service=service)
                vehicle_service.put()


class VehicleBusstopsMap(ndb.Model):
    vehicle = ndb.StringProperty()
    busstops = ndb.StringProperty(repeated=True)

    @classmethod
    def get_all(cls):
        result = VehicleBusstopsMap.query().fetch(100)
        return result

    @classmethod
    def entities_to_dict(cls, vehicle_busstops):
        vehicle_busstops_dict = {}
        if vehicle_busstops:
            for each in vehicle_busstops:
                vehicle_busstops_dict[each.vehicle] = each.busstops
        return vehicle_busstops_dict

    @classmethod
    def reset_stopped_buses(cls, stopped_buses):
        vehicle_busstops = VehicleBusstopsMap.get_all()
        vehicle_busstops_dict = VehicleBusstopsMap.entities_to_dict(vehicle_busstops)
        updated_vehicles = []
        for bus in stopped_buses:
            vehicle = bus[settings.VEHICLE_SERIAL_KEY]
            if vehicle in vehicle_busstops_dict.keys():
                previous_bus_stops = vehicle_busstops_dict[vehicle]
                if previous_bus_stops:
                    updated_vehicles.append(vehicle)
            else:
                updated_vehicles.append(vehicle)

        for vehicle_busstop in vehicle_busstops:
            if vehicle_busstop.vehicle in updated_vehicles:
                vehicle_busstop.busstops = []
                vehicle_busstop.put()

    @classmethod
    def create_or_update(cls, vehicle_busstops, updated_busstops_dict):
        if vehicle_busstops:
            for vehicle_busstop in vehicle_busstops:
                vehicle = vehicle_busstop.vehicle
                if vehicle in updated_busstops_dict.keys():
                    vehicle_busstop.busstops = updated_busstops_dict[vehicle]
                    vehicle_busstop.put()
        else:
            for vehicle, busstops in updated_busstops_dict.iteritems():
                vehicle_busstop = VehicleBusstopsMap(vehicle=vehicle, busstops=busstops)
                vehicle_busstop.put()

