# Definition for singly-linked list.
# class ListNode(object):
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next

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