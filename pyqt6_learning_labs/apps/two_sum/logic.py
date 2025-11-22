from typing import List, Tuple, Dict

def two_sum_logic(nums: List[int], target: int) -> Tuple[List[int], List[str]]:
    """
    Return indices and a textual trace of the algorithm.
    """
    seen: Dict[int, int] = {}
    steps = [f"Target: {target}", f"Input: {nums}"]

    for index, value in enumerate(nums):
        needed = target - value
        steps.append(f"Index {index}: value={value}, need={needed}")

        if needed in seen:
            steps.append(
                f"Found complement! seen[{needed}]={seen[needed]} so return [{seen[needed]}, {index}]"
            )
            return [seen[needed], index], steps

        seen[value] = index
        steps.append(f"Store {value} -> {index} in dictionary: {seen}")

    steps.append("No pair found that sums to the target.")
    return [], steps

def two_sum_complexity(n: int) -> List[int]:
    """O(n) complexity."""
    return list(range(1, n + 1))
