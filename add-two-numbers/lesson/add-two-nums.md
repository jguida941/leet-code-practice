# Add Two Numbers (Python)

## Problem
You are given two non-empty linked lists that represent two non-negative
integers. The digits are stored in reverse order, and each node contains a
single digit. Add the two numbers and return the sum as a linked list.

## Hints
- Each node may be `None` even if the other list still has digits, so think of
  `None` nodes as zeros.
- Keep a running `carry` so that `17` becomes `7` for the current digit and `1`
  for the next round.
- A dummy head node makes it easy to append new digits and return the final
  list without special cases.

## Reference Code
```python
class ListNode(object):
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


class Solution(object):
    def addTwoNumbers(self, l1, l2):
        dummy = ListNode()
        cur = dummy
        carry = 0

        while l1 or l2 or carry:
            v1 = l1.val if l1 else 0
            v2 = l2.val if l2 else 0

            val = v1 + v2 + carry
            carry = val // 10
            val = val % 10

            cur.next = ListNode(val)
            cur = cur.next

            l1 = l1.next if l1 else None
            l2 = l2.next if l2 else None

        return dummy.next
```

## Explanation

### What the function does
- Reads one digit at a time from both lists, treating missing digits as zero.
- Adds the digits plus any `carry` coming from the previous addition.
- Stores the ones place in the result list and keeps the tens place as the new
  carry.
- Moves along both lists until there are no digits and no carry left.

### Why the dummy node + single pointer works
- `dummy` anchors the head of the resulting list so you can always return
  `dummy.next` at the end.
- `cur` always points at the last node in the result, so you can append in
  constant time.
- This pattern avoids edge cases such as “is this the first node I’m adding?”

### Step-by-step example

#### Inputs
- `l1 = 2 -> 4 -> 3` (represents 342)
- `l2 = 5 -> 6 -> 4` (represents 465)

We keep three pieces of state:
1. `carry` – number to forward into the next column (start at 0)
2. `cur` – pointer to the last node in the result list
3. `l1`, `l2` – pointers to the current digit of each input list

---

#### Pass 1
1. `v1 = 2`, `v2 = 5`, `carry = 0`
2. `val = 2 + 5 + 0 = 7`
3. `carry = 7 // 10 = 0`, digit = `7 % 10 = 7`
4. Append `7` to the result list.

Result so far: `7`

---

#### Pass 2
1. Advance `l1` and `l2` → digits `4` and `6`
2. `val = 4 + 6 + 0 = 10`
3. `carry = 1`, digit = `0`
4. Append `0` to the result list.

Result so far: `7 -> 0`

---

#### Pass 3
1. Digits are `3` and `4`, carry is `1`
2. `val = 3 + 4 + 1 = 8`
3. `carry = 0`, digit = `8`
4. Append `8`

Result so far: `7 -> 0 -> 8`, which represents `807`

Since there are no remaining nodes and `carry` is `0`, we return `dummy.next`.
