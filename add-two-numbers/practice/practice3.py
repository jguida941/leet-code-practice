class ListNode(object):
    def __init__(self, value=0, next=None):
        self.value = value
        self.next = next


class Solution(object):
    def addTwoNums(self, l1, l2):
        dummy = ListNode()
        current_node = dummy
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.value if l1 else 0
            v2 = l2.value if l2 else 0

            total = v1 + v2 + carry
            carry = total // 10
            val = total % 10

            current_node.next = ListNode(val)
            current_node = current_node.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next


# --- helpers for testing and printing ---

def list_to_listnode(values):
    """Build a linked list from a Python list and return the head."""
    dummy = ListNode()
    cur = dummy
    for v in values:
        cur.next = ListNode(v)
        cur = cur.next
    return dummy.next


def listnode_to_list(head):
    """Convert a linked list back to a Python list of values."""
    out = []
    cur = head
    while cur:
        out.append(cur.value)
        cur = cur.next
    return out


if __name__ == "__main__":
    # Example from the problem:
    # l1 = 2 -> 4 -> 3  (represents 342)
    # l2 = 5 -> 6 -> 4  (represents 465)
    l1 = list_to_listnode([2, 4, 3])
    l2 = list_to_listnode([5, 6, 4])

    solver = Solution()
    result = solver.addTwoNums(l1, l2)

    # Print as a Python list
    print("Result as list:", listnode_to_list(result))  # expect [7, 0, 8]
