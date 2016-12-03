PROJECT_ID = "nus-bus-149718"

# urls
BUSSTOP_API_URL = "https://nextbus.comfortdelgro.com.sg/eventservice.svc"
BUSSTOPS_URL = BUSSTOP_API_URL + "/BusStops"
SHUTTLE_URL = BUSSTOP_API_URL + "/Shuttleservice"

BUS_TRACKING_API_BASE_URL = "https://api.ami-lab.org/api/v1"
BUS_TRACKING_LOGIN_URL = BUS_TRACKING_API_BASE_URL + "/user/login"
BUS_TRACKING_BUS_LOCATION_URL = BUS_TRACKING_API_BASE_URL + "/veniam/location"

# login credential
DOMAIN = "nusstu"
USERNAME = "a0119405"

# bus and shuttle services
BUSSTOP_RESULT_KEY = "BusStopsResult"
BUSSTOPS_KEY = "busstops"

SHUTTLE_RESULT_KEY = "ShuttleServiceResult"
SHUTTLES_KEY = "shuttles"

LATITUDE = "latitude"
LONGITUDE = "longitude"

BUS_SERVICE_KEY = "service"

VEHICLE_SERIAL_KEY = "vehicle_serial"

# bus service
BUS_A1 = ["PGPT", "KR-MRT", "LT29", "UHALL", "STAFFCLUB-OPP", "YIH", "CENLIB", "LT13", "AS7", "COM2", "BIZ2", "PGP12-OPP", "PGP7", "PGPT"]
BUS_A2 = ["PGPT", "PGP14-15", "PGP12", "HSSML-OPP", "NUSS-OPP", "COM2", "LT13-OPP", "COMCEN", "YIH-OPP", "MUSEUM", "STAFFCLUB", "UHALL-OPP", "S17", "KR-MRT-OPP", "PGP"]
BUS_D1 = ["HSSML-OPP", "NUSS-OPP", "COM2", "LT13-OPP", "COMCEN", "YIH-OPP", "MUSEUM", "UTOWN", "YIH", "CENLIB", "LT13", "AS7", "COM2", "BIZ2"]
BUS_D2 = ["PGP12-OPP", "PGP7", "PGPT", "KR-MRT", "LT29", "UHALL", "STAFFCLUB-OPP", "MUSEUM", "UTOWN", "STAFFCLUB", "UHALL-OPP", "S17", "KR-MRT-OPP", "PGP"]
BUS_B = ["KR-BT", "MUSEUM", "YIH", "CENLIB", "LT13", "AS7", "COM2", "LT13-OPP", "COMCEN", "YIH-OPP", "RAFFLES", "BLK-EA-OPP", "KR-BT"]
BUS_C = ["KR-BT", "MUSEUM", "STAFFCLUB", "UHALL-OPP", "S17", "LT29", "UHALL", "STAFFCLUB-OPP", "RAFFLES", "BLK-EA-OPP", "KR-BT"]
BUS_A1E = ["KR-MRT", "LT29", "UHALL", "STAFFCLUB-OPP", "YIH", "CENLIB", "LT13", "AS7", "COM2", "BIZ2", "PGP12-OPP", "PGP7", "PGPT"]
BUS_A2E = ["LT13-OPP", "COMCEN", "YIH-OPP", "MUSEUM", "STAFFCLUB", "UHALL-OPP", "S17", "KR-MRT-OPP"]
BUS_BTC = ["MUSEUM", "YIH", "CENLIB", "LT13", "AS7", "BIZ2", "PGP12-OPP", "PGP7", "PGPT", "BUKITTIMAH-BTC2", "BG-MRT", "MUSEUM", "BLK-EA-OPP"]
BUS_UT_CLB = ["UTOWN", "CENLIB", "UTOWN"]
BUS_UT_FOS = ["UTOWN", "LT29", "UTOWN"]

# BUS_SERVICES = ["A1", "A2", "D1", "D2", "B", "C", "A1E", "A2E", "BTC"]
# BUS_SERVICES_STOPS = [BUS_A1, BUS_A2, BUS_D1, BUS_D2, BUS_B, BUS_C, BUS_A1E, BUS_A2E, BUS_BTC]
BUS_SERVICE_STOPS_DICT = {
  "A1": BUS_A1,
  "A2": BUS_A2,
  "D1": BUS_D1,
  "D2": BUS_D2,
  "A1E": BUS_A1E,
  "A2E": BUS_A2E,
  "B": BUS_B,
  "C": BUS_C,
  "BTC": BUS_BTC
}
# BUS_SERVICE_STOPS_DICT = {BUS_SERVICES[x]: BUS_SERVICES_STOPS[x] for x in xrange(0, len(BUS_SERVICES))}

# busstops
BUSSTOPS = {
  "BusStopsResult": {
    "busstops": [
      {
        "caption": "AS7",
        "latitude": 1.2936110496521,
        "longitude": 103.771942138672,
        "name": "AS7"
      },
      {
        "caption": "BIZ 2",
        "latitude": 1.29333305358887,
        "longitude": 103.775001525879,
        "name": "BIZ2"
      },
      {
        "caption": "Botanic Gardens MRT",
        "latitude": 1.32270002365112,
        "longitude": 103.815101623535,
        "name": "BG-MRT"
      },
      {
        "caption": "BTC - Oei Tiong Ham Building",
        "latitude": 1.3191,
        "longitude": 103.8168,
        "name": "BUKITTIMAH-BTC2"
      },
      {
        "caption": "Central Library",
        "latitude": 1.29639995098114,
        "longitude": 103.772201538086,
        "name": "CENLIB"
      },
      {
        "caption": "College Green Hostel",
        "latitude": 1.32333302497864,
        "longitude": 103.816307067871,
        "name": "CGH"
      },
      {
        "caption": "COM2 (CP13)",
        "latitude": 1.29416704177856,
        "longitude": 103.773612976074,
        "name": "COM2"
      },
      {
        "caption": "Computer Centre",
        "latitude": 1.29750001430511,
        "longitude": 103.772903442383,
        "name": "COMCEN"
      },
      {
        "caption": "Kent Ridge Bus Terminal",
        "latitude": 1.29416704177856,
        "longitude": 103.769721984863,
        "name": "KR-BT"
      },
      {
        "caption": "Kent Ridge MRT",
        "latitude": 1.29379999637604,
        "longitude": 103.784896850586,
        "name": "KR-MRT"
      },
      {
        "caption": "Kent Vale",
        "latitude": 1.30209994316101,
        "longitude": 103.769096374512,
        "name": "KV"
      },
      {
        "caption": "LT13",
        "latitude": 1.29429996013641,
        "longitude": 103.770797729492,
        "name": "LT13"
      },
      {
        "caption": "LT29",
        "latitude": 1.29739999771118,
        "longitude": 103.780899047852,
        "name": "LT29"
      },
      {
        "caption": "Museum",
        "latitude": 1.30099999904633,
        "longitude": 103.773803710938,
        "name": "MUSEUM"
      },
      {
        "caption": "Opp Block EA",
        "latitude": 1.30050003528595,
        "longitude": 103.77010345459,
        "name": "BLK-EA-OPP"
      },
      {
        "caption": "Opp HSSML",
        "latitude": 1.29277801513672,
        "longitude": 103.775001525879,
        "name": "HSSML-OPP"
      },
      {
        "caption": "Opp Kent Ridge MRT",
        "latitude": 1.2936999797821,
        "longitude": 103.785202026367,
        "name": "KR-MRT-OPP"
      },
      {
        "caption": "Opp NUSS",
        "latitude": 1.29330003261566,
        "longitude": 103.772399902344,
        "name": "NUSS-OPP"
      },
      {
        "caption": "Opp PGP Hse No 12",
        "latitude": 1.29379999637604,
        "longitude": 103.777000427246,
        "name": "PGP12-OPP"
      },
      {
        "caption": "Opp UHall",
        "latitude": 1.29750001430511,
        "longitude": 103.778297424316,
        "name": "UHALL-OPP"
      },
      {
        "caption": "Opp University Health Centre",
        "latitude": 1.29879999160767,
        "longitude": 103.775497436523,
        "name": "STAFFCLUB-OPP"
      },
      {
        "caption": "Opp YIH",
        "latitude": 1.29910004138947,
        "longitude": 103.774299621582,
        "name": "YIH-OPP"
      },
      {
        "caption": "PGP Hse No 12",
        "latitude": 1.2936110496521,
        "longitude": 103.776947021484,
        "name": "PGP12"
      },
      {
        "caption": "PGP Hse No 14 and No 15",
        "latitude": 1.29305601119995,
        "longitude": 103.777778625488,
        "name": "PGP14-15"
      },
      {
        "caption": "PGP Hse No 7",
        "latitude": 1.29320001602173,
        "longitude": 103.777801513672,
        "name": "PGP7"
      },
      {
        "caption": "PGPR",
        "latitude": 1.29083299636841,
        "longitude": 103.780830383301,
        "name": "PGP"
      },
      {
        "caption": "Prince George's Park",
        "latitude": 1.29194402694702,
        "longitude": 103.7802734375,
        "name": "PGPT"
      },
      {
        "caption": "Raffles Hall",
        "latitude": 1.30099999904633,
        "longitude": 103.772598266602,
        "name": "RAFFLES"
      },
      {
        "caption": "S17",
        "latitude": 1.29739999771118,
        "longitude": 103.781700134277,
        "name": "S17"
      },
      {
        "caption": "UHall",
        "latitude": 1.29760003089905,
        "longitude": 103.777900695801,
        "name": "UHALL"
      },
      {
        "caption": "University Health Centre",
        "latitude": 1.2989000082016,
        "longitude": 103.77619934082,
        "name": "STAFFCLUB"
      },
      {
        "caption": "University Town",
        "latitude": 1.30361104011536,
        "longitude": 103.774444580078,
        "name": "UTown"
      },
      {
        "caption": "Ventus (Opp LT13)",
        "latitude": 1.29519999027252,
        "longitude": 103.770500183105,
        "name": "LT13-OPP"
      },
      {
        "caption": "YIH",
        "latitude": 1.29869997501373,
        "longitude": 103.774299621582,
        "name": "YIH"
      }
    ]
  }
}