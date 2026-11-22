# Reservoir sampling in Python: Algorithm R, Algorithm L and weighted A-Res

Reservoir sampling answers a question I'd expect in any quant developer or software engineering interview that touches data streams. You're reading a stream of items whose length you don't know in advance, you can only keep k of them in memory, and when it ends you want a sample in which every item had the same chance of being kept.

`algorithm_r` is the version most people know. You keep the first k items, and then item i (counting from 0) replaces a random slot with probability k/(i + 1). It's short and it's correct, but it draws a random number for every item in the stream. `algorithm_l` gives you exactly the same distribution while jumping straight over the items it would have thrown away. On a stream of 1,000,000 items with k = 10, I counted 999,990 random draws for Algorithm R and 353 for Algorithm L with the same seed.

`weighted_sample` handles the case where each item comes with a weight and you want heavier items to be more likely. It's the Efraimidis and Spirakis method: give each item the key u^(1/w) for a uniform u, and keep the k largest keys in a heap. Items with zero weight are never chosen.

```python
import random
from reservoir import algorithm_r, algorithm_l, weighted_sample

algorithm_r(range(1_000_000), 10)
algorithm_l(open("trades.csv"), 100, random.Random(7))
weighted_sample([("a", 1.0), ("b", 2.0), ("c", 3.0)], 2)
```

## Tests

Running `python3 -m unittest test_reservoir` uses fixed seeds throughout. It checks that each of 12 items lands in a sample of 4 a third of the time under both algorithms and that all 10 pairs from 5 items come up equally often (within 4.5 standard deviations over tens of thousands of runs). It also checks that a stream shorter than k comes back whole, that a single weighted draw follows the weights 1:2:3:4 and that items with zero weight are skipped. You'll only need the Python standard library.

## More practice

If you'd like more of this kind of problem, I've written coding interview problems with worked solutions in six languages at https://academicquant.co.uk/coding-interview-course?utm_source=github&utm_medium=post&utm_campaign=github-reservoir-sampling

MIT licence.
