def proportional_map(n, min1, max1, min2, max2):
    if n - min1 == 0:
        return 0
    return (max2 - min2) / ((max1 - min1)/(n - min1))

def metric_to_pixel(n):
    return n / 0.13

def pixel_to_metric(n):
    return n * 0.13
