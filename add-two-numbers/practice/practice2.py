#addTwoNumbers

""""
Problem
- You are given two non-empty linked lists that represent two non-negative
integers. The digits are stored in reverse order, and each node contains a
single digit. Add the two numbers and return the sum as a linked list.
"""
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next

class Solution(object):
    def addTwoNum(self, l1,l2):

        dummy_node = ListNode(0)
        current_node = dummy_node
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            value = v1 + v2 + carry
            carry = value // 10
            value = carry % 10


            current_node.next = ListNode(value)
            current_node.next = current_node

            l1 = l1.next if l1 else None
            l2 = l1.next if l2 else None
        return dummy_node.next





