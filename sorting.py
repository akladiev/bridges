import math


def radix_sort(container, key=lambda x: x):
    if not container:
        return []
    assert (all([key(x) >= 0 for x in container]))
    shift = 16
    n = 1
    while True:
        digits = {i: [] for i in range(2 ** shift)}
        digits_before_nth = []
        for element in container:
            elder_digits = key(element) >> (shift * n)
            digits_before_nth.append(elder_digits)
            nth_digit = (key(element) >> (shift * (n-1))) & ((2 ** shift) - 1)
            digits[nth_digit].append(element)
        container = [x for numbers in digits.values() for x in numbers]
        if all([x == 0 for x in digits_before_nth]):
            break
        n += 1
    return container


def bucket_sort(container, key=lambda x: x):
    if not container:
        return []
    num_elements = len(container)
    bucket_size = math.sqrt(num_elements)
    max_element, min_element = key(max(container, key=key)), key(min(container, key=key))
    num_buckets = math.ceil(bucket_size)
    if max_element == min_element:
        return list(container)
    buckets = [[] for _ in range(num_buckets)]
    for element in container:
        bucket_idx = int(key(element) * (num_buckets - 1) / (max_element - min_element))
        buckets[bucket_idx].append(element)
    buckets = [radix_sort(bucket, key=key) for bucket in buckets]
    container = [element for bucket in buckets for element in bucket]
    return container
