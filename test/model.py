# Golden reference model for the barrel shifter family.
# Pure Python, no hardware knowledge: this is "what the answer should be".


def model(a, k, n, left=0, shift=0, arithmetic=0):
    """Return the expected N-bit output.

    a          : input word (0 .. 2^n - 1)
    k          : shift amount (0 .. n-1)
    left       : 0 = right, 1 = left
    shift      : 0 = rotate, 1 = shift
    arithmetic : 1 = arithmetic right shift (fill with sign bit)
    """
    mask = (1 << n) - 1
    k %= n

    if not shift:                                   # rotate
        if left:
            return ((a << k) | (a >> (n - k))) & mask
        return ((a >> k) | (a << (n - k))) & mask

    if left:                                        # shift left (logical = arithmetic)
        return (a << k) & mask

    if arithmetic:                                  # arithmetic shift right
        signed = a - (1 << n) if a >> (n - 1) else a   # two's complement
        return (signed >> k) & mask                 # Python >> on negatives fills with 1s

    return a >> k                                   # logical shift right


def vectors(n, max_exhaustive=8, n_random=2000, seed=1):
    """Yield (a, k) pairs: exhaustive for small N, random for large N."""
    import random
    if n <= max_exhaustive:
        for k in range(n):
            for a in range(1 << n):
                yield a, k
    else:
        rng = random.Random(seed)
        for k in range(n):                          # every k, with edge-case data
            for a in (0, 1, (1 << n) - 1, 1 << (n - 1)):
                yield a, k
        for _ in range(n_random):
            yield rng.randrange(1 << n), rng.randrange(n)
