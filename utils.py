from math import sqrt, atan2, sin, cos


def calculate_distance(lat1, lon1, lat2, lon2):
    """
    calculate the distance between two geo point.
    :param lat1: latitude of location 1
    :param lon1: longitude of location 1
    :param lat2: latitude of location 2
    :param lon2: longitude of location 2
    :return: distance
        :type: double
    """
    R = 6373.0
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distance = R * c
    return distance


def match_route_pattern(busstops, route_stops):
    """
    Verify whether the bus is on this route.
    :param busstops: list of bus stops passed by a bus
    :param route_stops: list of bus stops of a bus route
    :return: boolean
    """
    i, j, count = 0, 0, 0
    while i < len(busstops):
        while j < len(route_stops):
            if busstops[i] == route_stops[j]:
                i += 1
                j += 1
                count += 0
                break
            j += 1
    if count > 1:
        return True
    else:
        return False
