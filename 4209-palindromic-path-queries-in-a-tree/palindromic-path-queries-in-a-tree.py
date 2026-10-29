class Solution:
    def palindromePath(self, n: int, edges: list[list[int]], s: str, queries: list[str]) -> list[bool]:
        graph = [[] for _ in range(n)]

        for u, v in edges:
            graph[u].append(v)
            graph[v].append(u)

        parent = [-1] * n
        depth = [0] * n
        size = [1] * n
        heavy = [-1] * n

        order = [0]
        for u in order:
            for v in graph[u]:
                if v != parent[u]:
                    parent[v] = u
                    depth[v] = depth[u] + 1
                    order.append(v)

        for u in reversed(order):
            largest = 0

            for v in graph[u]:
                if parent[v] == u:
                    size[u] += size[v]

                    if size[v] > largest:
                        largest = size[v]
                        heavy[u] = v

        head = [0] * n
        pos = [0] * n
        timer = 0
        stack = [(0, 0)]

        while stack:
            u, h = stack.pop()

            while u != -1:
                head[u] = h
                pos[u] = timer
                timer += 1

                for v in graph[u]:
                    if parent[v] == u and v != heavy[u]:
                        stack.append((v, v))

                u = heavy[u]

        seg_size = 1
        while seg_size < n:
            seg_size *= 2

        seg = [0] * (2 * seg_size)

        for u in range(n):
            seg[seg_size + pos[u]] = 1 << (ord(s[u]) - ord('a'))

        for i in range(seg_size - 1, 0, -1):
            seg[i] = seg[2 * i] ^ seg[2 * i + 1]

        def update(p, value):
            p += seg_size
            seg[p] = value
            p //= 2

            while p:
                seg[p] = seg[2 * p] ^ seg[2 * p + 1]
                p //= 2

        def range_xor(left, right):
            left += seg_size
            right += seg_size
            result = 0

            while left <= right:
                if left & 1:
                    result ^= seg[left]
                    left += 1

                if not (right & 1):
                    result ^= seg[right]
                    right -= 1

                left //= 2
                right //= 2

            return result

        def path_xor(u, v):
            result = 0

            while head[u] != head[v]:
                if depth[head[u]] < depth[head[v]]:
                    u, v = v, u

                result ^= range_xor(pos[head[u]], pos[u])
                u = parent[head[u]]

            if depth[u] > depth[v]:
                u, v = v, u

            result ^= range_xor(pos[u], pos[v])
            return result

        answer = []

        for query in queries:
            parts = query.split()

            if parts[0] == "update":
                u = int(parts[1])
                c = parts[2]
                update(pos[u], 1 << (ord(c) - ord('a')))

            else:
                u = int(parts[1])
                v = int(parts[2])

                mask = path_xor(u, v)
                answer.append(mask == 0 or (mask & (mask - 1)) == 0)

        return answer