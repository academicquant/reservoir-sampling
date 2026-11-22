import math
import random
import unittest
from collections import Counter

from reservoir import algorithm_l, algorithm_r, weighted_sample


def within(count, trials, p, sigmas=4.5):
    sd = math.sqrt(trials * p * (1 - p))
    return abs(count - trials * p) <= sigmas * sd


class TestUniform(unittest.TestCase):
    def check_uniform(self, fn, n=12, k=4, trials=60_000):
        rng = random.Random(1)
        counts = Counter()
        for _ in range(trials):
            s = fn(range(n), k, rng)
            self.assertEqual(len(s), k)
            self.assertEqual(len(set(s)), k)
            counts.update(s)
        for i in range(n):
            self.assertTrue(within(counts[i], trials, k / n), (fn.__name__, i, counts[i]))

    def test_algorithm_r_is_uniform(self):
        self.check_uniform(algorithm_r)

    def test_algorithm_l_is_uniform(self):
        self.check_uniform(algorithm_l)

    def test_pairs_are_uniform_too(self):
        # every one of the C(5, 2) = 10 subsets should turn up a tenth of the time
        rng = random.Random(2)
        trials = 50_000
        for fn in (algorithm_r, algorithm_l):
            counts = Counter(frozenset(fn(range(5), 2, rng)) for _ in range(trials))
            self.assertEqual(len(counts), 10)
            for c in counts.values():
                self.assertTrue(within(c, trials, 0.1), (fn.__name__, c))

    def test_short_stream_returns_everything(self):
        for fn in (algorithm_r, algorithm_l):
            self.assertEqual(sorted(fn(range(3), 5, random.Random(0))), [0, 1, 2])


class TestWeighted(unittest.TestCase):
    def test_single_draw_follows_the_weights(self):
        rng = random.Random(3)
        weights = {"a": 1.0, "b": 2.0, "c": 3.0, "d": 4.0}
        trials = 60_000
        counts = Counter(weighted_sample(weights.items(), 1, rng)[0] for _ in range(trials))
        for x, w in weights.items():
            self.assertTrue(within(counts[x], trials, w / 10.0), (x, counts[x]))

    def test_zero_weight_never_chosen(self):
        rng = random.Random(4)
        for _ in range(2_000):
            self.assertNotIn("z", weighted_sample([("z", 0.0), ("a", 1.0), ("b", 1.0)], 2, rng))


if __name__ == "__main__":
    unittest.main()
