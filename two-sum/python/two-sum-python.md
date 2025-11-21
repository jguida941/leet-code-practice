# Two Sum (Python)

## Problem
Given an array `nums` and a target value, return the indices of the two numbers
whose sum equals the target. Each input has exactly one solution, and you cannot
reuse the same element twice.

## Hints
- Indices refer to the original positions inside `nums`.
- A dictionary can store each number and its index as you scan the list.
- With a dictionary lookup the solution runs in O(n) time.

## Reference Code
```python
class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        index_by_value = {}

        for i, value in enumerate(nums):
            complement = target - value

            if complement in index_by_value:
                return [index_by_value[complement], i]

            index_by_value[value] = i

        return []
```

## Explanation

### What the function does
- Walks through the list once, looking for a pair that hits the target sum.
- Returns the indices as soon as the matching pair is found.

### The typical solution pattern (hash map / dictionary)
- Use a dictionary to remember every number seen so far along with its index.
- For each new number, ask “what number gets me to the target?” and check the
  dictionary. If the needed number already exists, you have the answer.
- Because dictionary lookups are constant time, each element is processed once.

### Step-by-step example

## Step-by-step example: Two Sum

Given:

- `nums = [2, 7, 11, 15]`
- `target = 9`

We keep a dictionary `seen` that remembers which values we have already visited and at which index they appeared.

Mapping: `value -> index`

---

## STEP 1

1. **Start empty**

   ```python
   seen = {}

We have not stored any numbers yet, so seen is empty.

⸻

STEP 2

We now iterate over nums = [2, 7, 11, 15] with target = 9.
2.	Index 0 (num = 2)
- We want two numbers that add up to 9.
  If one number is 2, the other must be 7 because 2 + 7 = 9.
-  code computes this “partner” using subtraction:

`need = target - num`  # 9 - 2 = 7

So here need = 7.

- We now ask: “Have we already seen a 7 earlier in the array?”

if need in seen:
    ...

Right now seen is {}, so the answer is no.

- Since `7` is not in seen, we record that we saw the value `2` at `index 0`:

`seen[2] = 0`
# seen is now {2: 0}

- This means: value 2 is stored at index 0.

⸻

STEP 3
3.	Index 1 (num = 7)
- Again we want two numbers that add up to 9.
- If the current number is 7, the other one must be 2 because 7 + 2 = 9.
-  code does the same computation:

`need = target - num`  # 9 - 7 = 2

So here need = 2.

- Now we check if 2 is in seen.
- Currently seen is `{2: 0}`, so `2` is present, at index `0`.

if need in seen:
    `return [seen[need], i]`  # [seen[2], 1] -> [0, 1]

That means:
- The previous value 2 at index 0, and
-  current value 7 at index 1  add up to the target 9.

- We return:

`return [0, 1]` and stop, because we have found the required pair.
