FLOWCHART_NODES = {
    "start": (
        "Start + dummy",
        "Create a dummy head + carry=0 so appending nodes is uniform.",
        -260,
        0,
    ),
    "read": (
        "Read digits",
        "Pull v1/v2 from the current l1/l2 nodes (or 0 if we've run out).",
        100,
        120,
    ),
    "sum": (
        "Compute total",
        "Add v1 + v2 + carry to get the raw sum for this column.",
        100,
        260,
    ),
    "split": (
        "Split digit/carry",
        "digit = total % base, carry = total // base.",
        -260,
        400,
    ),
    "append": (
        "Append digit",
        "Create a node containing digit and hook it to the running list.",
        220,
        400,
    ),
    "advance": (
        "Advance pointers",
        "Move l1/l2 (if they exist) and repeat until no digits and carry=0.",
        -20,
        560,
    ),
    "done": (
        "Return dummy.next",
        "Return the list beginning after the dummy node for the real answer.",
        -20,
        700,
    ),
}

FLOWCHART_EDGES = [
    ("start", "read"),
    ("read", "sum"),
    ("sum", "split"),
    ("sum", "append"),
    ("split", "append"),
    ("append", "advance"),
    ("advance", "read"),
    ("advance", "done"),
]

TEST_CASES = [
    ([2, 4, 3], [5, 6, 4], [7, 0, 8]),
    ([0], [0], [0]),
    ([9, 9, 9, 9], [9, 9, 9, 9], [8, 9, 9, 9, 1]),
    ([5], [5], [0, 1]),
]

TEMPLATE_CODE = '''class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1, l2):
    """Return the head of the new linked list sum."""
    carry = 0
    dummy = ListNode()
    cur = dummy

    while l1 or l2 or carry:
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0
        total = v1 + v2 + carry
        carry = total // 10
        cur.next = ListNode(total % 10)
        cur = cur.next
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
'''
