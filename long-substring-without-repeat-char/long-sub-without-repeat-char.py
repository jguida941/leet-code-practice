class Solution(object):
    def lengthOfLongestSubstring(self, s):

        charSet = set()
        start = 0
        result = 0

        for end in range(len(s)):
            while s[end] in charSet:
                charSet.remove(s[start])
                start +=1
            charSet.add(s[end])
            result = max(result, end - start +1)
        return result

# ---- test harness with prints ----

def run_tests():
    sol = Solution()

    test_cases = [
        ("abcabcbb", 3),   # "abc"
        ("bbbbb", 1),      # "b"
        ("pwwkew", 3),     # "wke"
        ("abba", 2),       # "ab" or "ba"
        ("", 0),           # empty string
        (" ", 1),          # single space
        ("dvdf", 3),       # "vdf"
        ("tmmzuxt", 5),    # "mzuxt"
    ]

    for s, expected in test_cases:
        got = sol.lengthOfLongestSubstring(s)
        print("s = {!r:10}  expected = {:2}  got = {:2}  {}".format(
            s, expected, got, "OK" if got == expected else "WRONG"
        ))

if __name__ == "__main__":
    run_tests()