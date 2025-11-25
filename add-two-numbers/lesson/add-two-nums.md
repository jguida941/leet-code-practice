# Add Two Numbers

## Problem Statement

You are given two **non-empty linked lists** representing two non-negative integers. The digits are stored in **reverse order**, and each node contains a single digit. Add the two numbers and return the sum as a linked list.

**Constraints:**
- Each linked list contains at least one node
- Digits are stored in reverse order (least significant first)
- Each node value is between 0 and 9
- No leading zeros (except the number 0 itself)

**Example:**
```
Input:  l1 = [2,4,3], l2 = [5,6,4]
Output: [7,0,8]
Explanation: 342 + 465 = 807 (reversed: 7 -> 0 -> 8)
```


## Key Insight

The digits being stored in **reverse order** is actually a gift! It means we process from least-significant to most-significant digit - exactly how we do addition by hand.

**The trick:** Keep a running `carry` value, and treat missing nodes as zeros:

```
digit_sum = val1 + val2 + carry
new_digit = digit_sum % 10
new_carry = digit_sum // 10
```


## The Linked List Approach

Use a **dummy head node** to simplify list construction:

```
dummy -> [result nodes...]
```

**Why a dummy node?**
- Avoids special handling for the first node
- Always return `dummy.next` at the end
- Clean, consistent code


## Reference Solution

```python
class ListNode:
    def __init__(self, val=0, next=None):
        self.val = val
        self.next = next


def add_two_numbers(l1, l2):
    dummy = ListNode()  # Placeholder head
    cur = dummy         # Pointer to build result
    carry = 0

    while l1 or l2 or carry:
        # Get values (0 if node is None)
        v1 = l1.val if l1 else 0
        v2 = l2.val if l2 else 0

        # Calculate sum and carry
        total = v1 + v2 + carry
        carry = total // 10
        digit = total % 10

        # Append new digit to result
        cur.next = ListNode(digit)
        cur = cur.next

        # Advance input pointers
        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return dummy.next
```


## Step-by-Step Walkthrough

Let's trace through with `l1 = [2,4,3]` (342) and `l2 = [5,6,4]` (465):

### Initialize

```
dummy = ListNode()
cur = dummy
carry = 0
```

We start with an empty result list and no carry.

### Pass 1: Process first digits

```
l1.val = 2, l2.val = 5, carry = 0
total = 2 + 5 + 0 = 7
carry = 7 // 10 = 0
digit = 7 % 10 = 7
```

**Action:** Append node with value `7`

```
Result: dummy -> 7
```

### Pass 2: Process second digits

```
l1.val = 4, l2.val = 6, carry = 0
total = 4 + 6 + 0 = 10
carry = 10 // 10 = 1
digit = 10 % 10 = 0
```

**Action:** Append node with value `0`, carry forward `1`

```
Result: dummy -> 7 -> 0
```

### Pass 3: Process third digits

```
l1.val = 3, l2.val = 4, carry = 1
total = 3 + 4 + 1 = 8
carry = 8 // 10 = 0
digit = 8 % 10 = 8
```

**Action:** Append node with value `8`

```
Result: dummy -> 7 -> 0 -> 8
```

### Termination

Both lists exhausted, carry is 0. Loop ends.

**Return:** `dummy.next` which is `7 -> 0 -> 8` (represents 807)

**Verification:** 342 + 465 = 807


## Complexity Analysis

**Time Complexity: O(max(m, n))**
- m = length of l1, n = length of l2
- We traverse each list exactly once

**Space Complexity: O(max(m, n))**
- Result list has at most max(m, n) + 1 nodes
- The +1 accounts for a possible carry at the end


## Common Edge Cases

### 1. Different Length Lists

```
l1 = [9,9,9,9,9,9,9]  (9999999)
l2 = [9,9,9,9]        (9999)
Output: [8,9,9,9,0,0,0,1]  (10009998)
```

**Why it matters:** Lists won't always be the same length. Your code must handle continuing when one list is exhausted.

**How it works:**
- First 4 passes process both lists normally
- Passes 5-7: l2 is None, so v2 = 0
- The carry propagates through the remaining digits
- Final carry creates an extra node

**Key insight:** The condition `while l1 or l2 or carry` ensures we continue as long as ANY work remains.


### 2. Result Has Extra Digit (Carry at End)

```
l1 = [9,9]  (99)
l2 = [1]    (1)
Output: [0,0,1]  (100)
```

**Why it matters:** When the sum causes a carry after all digits are processed, we need an extra node.

**How it works:**
- Pass 1: 9 + 1 = 10 → digit=0, carry=1
- Pass 2: 9 + 0 + 1 = 10 → digit=0, carry=1
- Pass 3: l1=None, l2=None, but carry=1 → digit=1, carry=0
- Loop exits

**Key insight:** Including `carry` in the while condition handles this automatically - no special case needed.


### 3. Single Digit Numbers

```
l1 = [5]
l2 = [5]
Output: [0,1]  (10)
```

**Why it matters:** The simplest case still needs to handle carry correctly.

**How it works:**
- Pass 1: 5 + 5 = 10 → digit=0, carry=1
- Pass 2: Both lists empty, carry=1 → digit=1, carry=0
- Return [0,1]

**Key insight:** Even single digits can produce two-digit results.


### 4. One List is Zero

```
l1 = [0]
l2 = [7,3]  (37)
Output: [7,3]  (37)
```

**Why it matters:** Adding zero should return the other number unchanged.

**How it works:**
- Pass 1: 0 + 7 = 7 → digit=7
- Pass 2: l1=None (treat as 0), l2.val=3 → digit=3
- Return [7,3]

**Key insight:** Treating None as 0 handles this naturally.


### 5. Large Carry Chain

```
l1 = [9,9,9]  (999)
l2 = [1]      (1)
Output: [0,0,0,1]  (1000)
```

**Why it matters:** A single 1 can cause a cascade of carries through the entire number.

**How it works:**
- Pass 1: 9 + 1 = 10 → digit=0, carry=1
- Pass 2: 9 + 0 + 1 = 10 → digit=0, carry=1
- Pass 3: 9 + 0 + 1 = 10 → digit=0, carry=1
- Pass 4: 0 + 0 + 1 = 1 → digit=1, carry=0

**Key insight:** The algorithm handles carry chains of any length without modification.


## Tips for Interviews

1. **Clarify edge cases** - Ask about different lengths, leading zeros, empty lists

2. **Explain the dummy node** - Show you understand why it simplifies the code

3. **Walk through the math** - Demonstrate you understand integer division and modulo

4. **Discuss the while condition** - Explain why `l1 or l2 or carry` covers all cases

5. **Mention in-place vs new list** - Note that we create a new list (can't modify inputs)


## Practice Variations

Once you master Add Two Numbers, try these related problems:

- **Add Two Numbers II** - Digits in normal order (most significant first)
- **Multiply Strings** - Multiply two numbers represented as strings
- **Plus One** - Add 1 to a number represented as array
- **Add Binary** - Add two binary strings
