"""Reservoir sampling: a uniform sample of k items from a stream of unknown length in one pass
and O(k) memory (Algorithm R and the faster skip-ahead Algorithm L), plus weighted sampling
without replacement (Efraimidis-Spirakis A-Res)."""
import heapq
import math
import random


def algorithm_r(stream, k, rng=random):
    """Keep the first k items; item i (0-based, i >= k) replaces a random slot with probability k/(i+1)."""
    sample = []
    for i, x in enumerate(stream):
        if i < k:
            sample.append(x)
        else:
            j = rng.randrange(i + 1)
            if j < k:
                sample[j] = x
    return sample


def algorithm_l(stream, k, rng=random):
    """Same distribution as Algorithm R, but jumps over the items it would reject,
    so it draws O(k log(n/k)) random numbers instead of n."""
    it = iter(stream)
    sample = []
    for x in it:
        sample.append(x)
        if len(sample) == k:
            break
    if len(sample) < k:
        return sample
    w = math.exp(math.log(rng.random()) / k)
    while True:
        skip = math.floor(math.log(rng.random()) / math.log(1.0 - w))
        x = None
        for _ in range(skip + 1):
            x = next(it, _END)
            if x is _END:
                return sample
        sample[rng.randrange(k)] = x
        w *= math.exp(math.log(rng.random()) / k)


_END = object()


def weighted_sample(stream, k, rng=random):
    """A-Res: from (item, weight) pairs, keep the k items with the largest u ** (1 / weight)."""
    heap = []
    for x, wt in stream:
        if wt <= 0:
            continue
        key = rng.random() ** (1.0 / wt)
        if len(heap) < k:
            heapq.heappush(heap, (key, id(x), x))
        elif key > heap[0][0]:
            heapq.heapreplace(heap, (key, id(x), x))
    return [x for _, _, x in heap]
