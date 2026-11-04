class Fenwick:
    def __init__(self, n):
        self.n = n
        self.tree = [0] * (n + 1)

    def add(self, i, val):
        while i <= self.n:
            self.tree[i] += val
            i += i & -i

    def query(self, i):
        result = 0
        while i > 0:
            result += self.tree[i]
            i -= i & -i
        return result

    def kth(self, k):
        idx = 0
        bit = 1 << (self.n.bit_length() - 1)

        while bit:
            nxt = idx + bit

            if nxt <= self.n and self.tree[nxt] < k:
                idx = nxt
                k -= self.tree[nxt]

            bit >>= 1

        return idx + 1


class Solution:
    def minOperations(self, nums: List[int], x: int, k: int) -> int:
        n = len(nums)
        values = sorted(set(nums))
        m = len(values)

        pos = {v: i + 1 for i, v in enumerate(values)}
        arr = [pos[v] for v in nums]

        count = Fenwick(m)
        sums = Fenwick(m)

        window_sum = 0

        # First window
        for i in range(x):
            count.add(arr[i], 1)
            sums.add(arr[i], nums[i])
            window_sum += nums[i]

        costs = []
        for i in range(n - x + 1):

            mid = count.kth((x + 1) // 2)
            median = values[mid - 1]

            left_count = count.query(mid)
            left_sum = sums.query(mid)

            right_count = x - left_count
            right_sum = window_sum - left_sum

            cost = (
                median * left_count - left_sum
                + right_sum - median * right_count
            )

            costs.append(cost)

            if i + x < n:
                outgoing = i
                incoming = i + x

                count.add(arr[outgoing], -1)
                sums.add(arr[outgoing], -nums[outgoing])

                count.add(arr[incoming], 1)
                sums.add(arr[incoming], nums[incoming])

                window_sum += nums[incoming] - nums[outgoing]

        INF = float('inf')

        prev = [0] * (n + 1)

        for j in range(1, k + 1):
            curr = [INF] * (n + 1)

            for i in range(1, n + 1):
                curr[i] = curr[i - 1]

                if i >= x:
                    curr[i] = min(
                        curr[i],
                        prev[i - x] + costs[i - x]
                    )

            prev = curr

        return prev[n]
