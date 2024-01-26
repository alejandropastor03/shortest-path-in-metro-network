from math import *
from typing import List


def distancia_coor(A, B: List)->float:
    lat1 = A[0]
    lat2 = B[0]
    lon1 = A[1]
    lon2 = B[1]
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    base = 6371 * c * 1000
    return base
