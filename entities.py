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
