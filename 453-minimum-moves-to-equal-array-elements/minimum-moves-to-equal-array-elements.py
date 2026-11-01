class Solution:
    def minMoves(self, nums: list[int]) -> int:
        minimum = min(nums)
        total = 0
        for num in nums:
            total += num - minimum
        return total