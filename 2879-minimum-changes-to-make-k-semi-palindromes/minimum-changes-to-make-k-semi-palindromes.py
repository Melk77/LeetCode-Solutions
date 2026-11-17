
class Solution:
    def minimumChanges(self, s: str, k: int) -> int:
        n = len(s)

        # Step 1: Precompute the cost of every substring
        cost = [[0] * n for _ in range(n)]

        for i in range(n):
            for j in range(i + 1, n):
                length = j - i + 1
                best = float('inf')

                # Try every proper divisor
                for d in range(1, length):
                    if length % d != 0:
                        continue

                    changes = 0

                    # Check each group
                    for offset in range(d):
                        left = offset
                        right = length - d + offset

                        while left < right:
                            if s[i + left] != s[i + right]:
                                changes += 1

                            left += d
                            right -= d

                    best = min(best, changes)

                cost[i][j] = best

        # Step 2: Dynamic Programming
        INF = float('inf')

        dp = [[INF] * (n + 1) for _ in range(k + 1)]

        dp[0][0] = 0

        for groups in range(1, k + 1):
            for i in range(2 * groups, n + 1):

                for j in range(2 * (groups - 1), i - 1):

                    dp[groups][i] = min(
                        dp[groups][i],
                        dp[groups - 1][j] + cost[j][i - 1]
                    )

        return dp[k][n]
