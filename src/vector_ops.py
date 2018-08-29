import math


def vec_sub(v1, v2):
    return tuple((v2[0] - v1[0], v2[1] - v1[1]))


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
