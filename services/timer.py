from time import perf_counter


class Timer:
    """
    Simple execution timer.
    """

    def __init__(self):
        self.start = perf_counter()

    def elapsed(self) -> float:
        return perf_counter() - self.start