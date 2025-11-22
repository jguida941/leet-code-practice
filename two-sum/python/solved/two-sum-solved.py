class Solution(object):
    def twoSum(self, nums, target):
        """
        :type nums: List[int]
        :type target: int
        :rtype: List[int]
        """
        index_by_value = {}             # loop 1: {2:0}

        # [2,7,11,15], target = 9
        for index, value_a in enumerate(nums):
            value_b = target - value_a  # 1oop 1: target = 9, value_a 0: 2,
                                        # loop 1:  value_b = 9 - 2
                                        # loop 2:  value_b = 9 - 7

            if value_b in index_by_value:  # loop 1:  7 not in dict, skip
                # loop 2:  2 in dict
                return [index_by_value[value_b], index]  # loop 2: return index_by_value[2]= 0

            index_by_value[value_a] = index
        return []

if __name__ == "__main__":

    nums = [2,7,11,15]
    target = 9

    solver = Solution()
    result = solver.twoSum(nums,target)
    print(result)

