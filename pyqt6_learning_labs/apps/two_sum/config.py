FLOWCHART_NODES = {
    "start": (
        "Start + init seen{}",
        "Create an empty dictionary (hash map) to remember values -> indices",
        -280,
        0,
    ),
    "loop": (
        "Loop over nums",
        "Enumerate the array while tracking the current index and value.",
        -40,
        140,
    ),
    "need": (
        "Compute needed",
        "At each step compute target - value to find the complement we still need.",
        -40,
        280,
    ),
    "check": (
        "Is needed stored?",
        "If the complement was seen earlier we can immediately return both indices.",
        -260,
        420,
    ),
    "return": (
        "Return indices",
        "Output the stored index of the complement with the current index and finish.",
        220,
        420,
    ),
    "store": (
        "Store value:index",
        "Otherwise cache value -> index and continue to the next item.",
        -40,
        560,
    ),
}

FLOWCHART_EDGES = [
    ("start", "loop"),
    ("loop", "need"),
    ("need", "check"),
    ("check", "return"),
    ("check", "store"),
    ("store", "loop"),
]

TEST_CASES = [
    ([2, 7, 11, 15], 9, [0, 1]),
    ([3, 3], 6, [0, 1]),
    ([3, 2, 4], 6, [1, 2]),
    ([1, 2, 3, 4, 5, 6], 11, [4, 5]),
]

TEMPLATE_CODE = '''def two_sum(nums, target):
    """Return the indices of the two numbers that hit the target."""
    seen = {}
    for i, value in enumerate(nums):
        need = target - value
        if need in seen:
            return [seen[need], i]
        seen[value] = i
    return []
'''
