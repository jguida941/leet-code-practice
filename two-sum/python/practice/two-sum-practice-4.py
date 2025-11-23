class Solution(object):
    def twoSum(self, nums, target):

        hashmap = {}

        for pos, x1 in enumerate(nums):
            x2 = target - x1
            if x2 in hashmap:
                return [hashmap[x2], pos]
            hashmap[x1] = pos
        return []


# --------- Helper -----------
if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9

    solver = Solution()
    result = solver.twoSum(nums, target)
    print("Result indices:", result)

    i, j = result
    print(f"Values at indices {i} and {j} are: {nums[i]} and {nums[j]}")
    print(f"Sum of values: {nums[i]} + {nums[j]} =", nums[i] + nums[j])

