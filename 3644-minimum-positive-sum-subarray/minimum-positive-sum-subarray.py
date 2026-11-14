
class Solution:
    def minimumSumSubarray(self, nums: List[int], l: int, r: int) -> int:
        ans = float('inf')

        for k in range(l, r + 1):
            summ = sum(nums[:k])

            if summ > 0:
                ans = min(ans, summ)

            for i in range(k, len(nums)):
                summ += nums[i] - nums[i - k]

                if summ > 0:
                    ans = min(ans, summ)

        return ans if ans != float('inf') else -1
