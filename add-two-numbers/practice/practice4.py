class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next
class Solution(object):
    def addTwoNums(self,list_1,list_2):

        dummy = ListNode()
        curr_node = dummy
        carry = 0

        while list_1 or list_2 or carry:
            val_1 = list_1.val if list_1 else 0
            val_2 = list_2.val if list_2 else 0

            total = val_1 + val_2 + carry
            carry = total // 10
            digit = total % 10

            curr_node.next = ListNode(digit)
            curr_node = curr_node.next

            list_1 = list_1.next if list_1 else None
            list_2 = list_2.next if list_2 else None

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
        out.append(cur.val)
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


