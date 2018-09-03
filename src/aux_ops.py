import math


def vec_add(v1, v2):
    return tuple((v2[0] + v1[0], v2[1] + v1[1]))


def vec_sub(v1, v2):
    return tuple((v1[0] - v2[0], v1[1] - v2[1]))


def vec_normalize(v):
    mag = vec_mag(v)
    return tuple((v[0] / mag, v[1] / mag))


def vec_mag(v):
    return math.sqrt(v[0] * v[0] + v[1] * v[1])


def vec_mult_n(v, n):
    return tuple((v[0] * n, v[1] * n))


def vec_set_mag(v, n):
    return vec_mult_n(vec_normalize(v), n)


def vec_limit(v, n):
    if vec_mag(v) > n:
        return vec_set_mag(v, n)
    else:
        return v


def vec_angle(v):
    if v[0] == 0:
        return 0

    angle = -math.degrees(math.atan(v[1]/v[0]))

    if v[0] < 0 and v[1] > 0:
        angle -= 180
    elif v[0] < 0 and v[1] < 0:
        angle += 180
    return angle


def proportional_map(n, min1, max1, min2, max2):
    return (max2 - min2)/((max1 - min1)/(n - min1))
