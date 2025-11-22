# Definition for singly-linked list.
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        """
        :type l1: Optional[ListNode]
        :type l2: Optional[ListNode]
        :rtype: Optional[ListNode]
        """
        dummy = ListNode()  # dummy -- > None
        cur = dummy         # curr -- > dummy --> None
        carry = 0  # carry from the previous digit addition (starts at 0)

        # keep looping while at-least one of this is not Null
        # only stop when both are none
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            # sum of the two digits plus incoming carry
            val = v1 + v2 + carry

            # split into ones, tens etc
            # example: val = 17 -> carry = 1, digit = 7
            carry = val // 10  # 1
            val = val % 10  # 7
            cur.next = ListNode(val)

            # update pointers to move to the next nodes in each list (if they exist)
            cur = cur.next  # move cur to the new last node in the result list

            # if l1/l2 is not None, move to l1.next, otherwise keep it as None
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
    result = solver.addTwoNumbers(l1, l2)

    # Print as a Python list
    print("Result as list:", listnode_to_list(result))  # expect [7, 0, 8]
