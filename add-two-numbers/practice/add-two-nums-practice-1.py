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
        dummy_node = ListNode(0)   # dummy head node
        curr_node = dummy_node
        carry = 0

        # keep going while there are digits left in either list, or a carry
        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            val = v1 + v2 + carry
            carry = val // 10
            digit = val % 10

            # append new node with this digit
            curr_node.next = ListNode(digit)
            curr_node = curr_node.next

            # move list pointers forward
            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        # skip dummy and return real head
        return dummy_node.next

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
