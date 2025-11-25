# Two Sum

## Problem Statement

Given an array of integers `nums` and an integer `target`, return the **indices** of the two numbers that add up to the target.

**Constraints:**
- Each input has **exactly one solution**
- You may **not use the same element twice**
- Return the answer in any order

**Example:**
```
Input:  nums = [2, 7, 11, 15], target = 9
Output: [0, 1]
Explanation: nums[0] + nums[1] = 2 + 7 = 9
```
## Key Insight

The brute force approach checks every pair, giving O(n²) time complexity. We can do better!

**The trick:** For each number, we know exactly what "partner" we need:

```
partner = target - current_number
```

If we can instantly check whether we've seen that partner before, we solve it in **O(n)** time.


## The Hash Map Strategy

Use a dictionary to remember every number we've seen and its index:

```
seen = {value: index}
```

For each new number:
1. Calculate what partner we need
2. Check if partner exists in our dictionary
3. If yes - we found our answer!
4. If no - store current number and continue


## Reference Solution

```python
def two_sum(nums, target):
    seen = {}  # value -> index

    for i, num in enumerate(nums):
        partner = target - num

        if partner in seen:
            return [seen[partner], i]

        seen[num] = i

    return []  # No solution found
```

## Step-by-Step Walkthrough

Let's trace through with `nums = [2, 7, 11, 15]` and `target = 9`:

### Step 1: Initialize

```
seen = {}
target = 9
```
We start with an empty dictionary.

### Step 2: Process index 0

```
i = 0, num = 2
partner = 9 - 2 = 7
```
**Question:** Is `7` in seen?

**Answer:** No, seen is empty `{}`

**Action:** Store current number

```
seen[2] = 0
seen = {2: 0}
```

### Step 3: Process index 1

```
i = 1, num = 7
partner = 9 - 7 = 2
```
**Question:** Is `2` in seen?

**Answer:** Yes! `seen[2] = 0`

**Action:** Return the answer!
```
return [seen[2], 1] = [0, 1]
```

## Why This Works

**Trace Summary:**

```
Step 0: num=2, need=7, seen={}
        -> 7 not found -> store {2: 0}

Step 1: num=7, need=2, seen={2: 0}
        -> 2 FOUND at index 0 -> return [0, 1]
```

The dictionary gives us **O(1)** lookup, so the total time is **O(n)**.

## Complexity Analysis

**Time Complexity: O(n)**
- Single pass through the array
- Dictionary lookup is O(1)

**Space Complexity: O(n)**
- Dictionary stores up to n elements in worst case

## Common Edge Cases

### 1. Two Identical Numbers

```
nums = [3, 3], target = 6
Output: [0, 1]
```

**Why it matters:** You might think we need the same number twice, but we need two *different elements* with the same value.

**How it works:**
- At index 0: We see `3`, need `3`. Dictionary is empty, so we store `{3: 0}`
- At index 1: We see `3`, need `3`. We find `3` in dictionary at index 0!
- Return `[0, 1]` - two different positions, same value

**Key insight:** We check the dictionary *before* storing the current number, so we don't match an element with itself.


### 2. Negative Numbers

```
nums = [-1, -2, 3], target = 1
Output: [1, 2]
```

**Why it matters:** The algorithm must handle negative values correctly.

**How it works:**
- At index 0: num = `-1`, need = `1 - (-1) = 2`. Store `{-1: 0}`
- At index 1: num = `-2`, need = `1 - (-2) = 3`. Store `{-1: 0, -2: 1}`
- At index 2: num = `3`, need = `1 - 3 = -2`. Found `-2` at index 1!
- Return `[1, 2]` because `-2 + 3 = 1`

**Key insight:** Subtraction handles negatives naturally. `target - negative = target + positive`.


### 3. Zero in Array

```
nums = [0, 4, 3, 0], target = 0
Output: [0, 3]
```

**Why it matters:** Zero is tricky because `0 + 0 = 0`, and we need two *different* zeros.

**How it works:**
- At index 0: num = `0`, need = `0 - 0 = 0`. Dictionary empty, store `{0: 0}`
- At index 1: num = `4`, need = `-4`. Not found, store `{0: 0, 4: 1}`
- At index 2: num = `3`, need = `-3`. Not found, store `{0: 0, 4: 1, 3: 2}`
- At index 3: num = `0`, need = `0`. Found `0` at index 0!
- Return `[0, 3]`

**Key insight:** Same logic as identical numbers - we find the *first* zero when processing the *second* zero.


### 4. Solution at the End

```
nums = [1, 2, 3, 4], target = 7
Output: [2, 3]
```

**Why it matters:** The algorithm must scan the entire array if needed.

**How it works:**
- Index 0: num=1, need=6. Not found. Store `{1: 0}`
- Index 1: num=2, need=5. Not found. Store `{1: 0, 2: 1}`
- Index 2: num=3, need=4. Not found. Store `{1: 0, 2: 1, 3: 2}`
- Index 3: num=4, need=3. Found `3` at index 2!
- Return `[2, 3]`

**Key insight:** Worst case is O(n) when the solution is the last pair checked.


### 5. No Solution Exists

```
nums = [1, 2, 3], target = 100
Output: []
```

**Why it matters:** Your code should handle cases where no valid pair exists.

**How it works:**
- Scans entire array, never finds a matching partner
- Returns empty list `[]` after the loop

**Key insight:** Always have a fallback return statement after the loop!


## Tips for Interviews

1. **Clarify first** - Can numbers be negative? Can there be duplicates?

2. **Start simple** - Mention the brute force O(n²) approach first

3. **Then optimize** - Explain how the hash map reduces to O(n)

4. **Discuss edge cases** - Show you think about duplicates and zeros

5. **Write clean code** - Use meaningful variable names like `partner` or `complement`

## Practice Variations

Once you master Two Sum, try these related problems:

- **Three Sum** - Find triplets that sum to target
- **Two Sum II** - Input array is already sorted
- **Two Sum IV** - Input is a binary search tree
- **Four Sum** - Find quadruplets that sum to target
