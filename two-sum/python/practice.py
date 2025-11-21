class Solution(object):
    def twoSum(self, nums: list[int], target: int)-> list[int]:
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        # Use a hash table (dict) to map number -> index for O(1) lookup
        # dict is implemented as a hash table under the hood in python
        hashtable = {} # number value --> index

        """
        nums   = [2, 7, 11, 15]
        target = 9
        Find the indices of two numbers that add up to 9.
        Loop 1:
            index    = 0
            currNum  = 2
            enumerate(nums) gives us the pair (0, 2).
            We then store this in the dict as: hashtable[2] = 0
        """
        # Loop through nums
        for index, currNum in enumerate(nums):
            # Get the differance
            otherNum = target - currNum

            # Check if difference is in index
            if otherNum in hashtable:
                # If so return hashtable
                return [hashtable[otherNum],index]
            hashtable[currNum] = index
        return []


if __name__ == "__main__":
    nums = [2, 7, 11, 15]
    target = 9

    solver = Solution()
    result = solver.twoSum(nums, target)
    print("Result indices:", result)

    i, j = result
    print("Values at indices is: ", nums[i], nums[j])
    print("Sum of values is:", nums[i] + nums[j])

