class Solution(object):
    def twoSum(self, nums, target):

        hashtable = {}

        for pos, x1 in enumerate(nums):
            x2 = target - x1
            if x2 in hashtable:
                return [hashtable[x2],pos]
            hashtable[x1] = pos
        return []
if __name__ == "__main__":
    nums = [2,7,11,15]
    target = 9

    solver = Solution()
    result = solver.twoSum(nums,target)
    print(result)