from typing import List, Tuple, Optional

class ListNode:
    def __init__(self, val: int = 0, next: "ListNode | None" = None):
        self.val = val
        self.next = next

def list_to_nodes(values: List[int]) -> Optional[ListNode]:
    dummy = ListNode()
    cur = dummy
    for value in values:
        cur.next = ListNode(value)
        cur = cur.next
    return dummy.next

def nodes_to_list(head: Optional[ListNode]) -> List[int]:
    out: List[int] = []
    cur = head
    while cur:
        out.append(cur.val)
        cur = cur.next
    return out

def add_two_numbers_logic(l1: List[int], l2: List[int], base: int = 10) -> Tuple[List[int], List[str]]:
    node1 = list_to_nodes(l1)
    node2 = list_to_nodes(l2)

    dummy = ListNode()
    cur = dummy
    carry = 0
    step = 0
    trace: List[str] = [f"Input A: {l1}", f"Input B: {l2}", f"Base: {base}"]

    while node1 or node2 or carry:
        v1 = node1.val if node1 else 0
        v2 = node2.val if node2 else 0
        carry_in = carry
        total = v1 + v2 + carry_in
        carry = total // base
        digit = total % base
        trace.append(
            f"Step {step}: v1={v1}, v2={v2}, carry in={carry_in}, total={total}, "
            f"write digit={digit}, carry out={carry}"
        )
        cur.next = ListNode(digit)
        cur = cur.next
        node1 = node1.next if node1 else None
        node2 = node2.next if node2 else None
        step += 1

    result = nodes_to_list(dummy.next)
    trace.append(f"Result digits (reverse order): {result}")
    return result, trace

def add_two_nums_complexity(n: int) -> List[int]:
    """O(max(m, n)) -> O(n) roughly."""
    return list(range(1, n + 1))
