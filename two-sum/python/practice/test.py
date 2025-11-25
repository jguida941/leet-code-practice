class Solution(object):
    def addTwoSum(self, nums, target):

        hashmap = {}

        for pos,x1 in enumerate(nums):
            x2 = target - x1
            if x2 in hashmap:
                return [hashmap[x2],pos]
            hashmap[x1] = pos
        return []
# --------- Helper -----------
if __name__ == "__main__":
    nums = [2,7,11,15]
    target = 9
    solver = Solution()
    result = solver.addTwoSum(nums,target)
    print(result)