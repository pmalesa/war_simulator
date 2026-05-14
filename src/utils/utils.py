def clamp(self, x: int, min_val: int, max_val: int) -> int:
    return min(max(min_val, x), max_val)
