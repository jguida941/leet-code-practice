class Solution(object):
    def twoSum(self, nums, target):

            hashtable = {}

            for pos, x1 in enumerate(num):
                x2 = target - x1
                if x2 in hashtable:
                    return [hashtable[x2],pos]
                hashtable[x1] = pos
            return []
if __name__ == "main":
    nums = [2,7,11,15]
    target = p
    solver = Solution()
    result = solver.TwoSum(num,target)