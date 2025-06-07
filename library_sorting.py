import json

class SparseCircularArray:
    def __init__(self, nk, mk, head=0):
        self.nk = nk
        self.mk = mk
        self.real_keys = []
        self.head = head
        self.update_size()

    def update_size(self):
        self.n = len(self.real_keys)
        self.k = self.get_k(self.n)
        self.m = int(self.nk[self.k - 1] * self.mk[self.k - 1])
        self.build_sparse_array()

    def get_k(self, n):
        for k in range(1, len(self.nk)):
            if k == 1 and self.nk[k - 1] <= n <= self.nk[k]:
                return k
            elif self.nk[k - 1] < n <= self.nk[k]:
                return k
        raise ValueError("n εκτός ορίων nk")

   def build_sparse_array(self):
        self.y = [0] * self.m
        if not self.real_keys:
            return
        positions = self.get_uniform_positions(len(self.real_keys), self.m)
        for i, pos in enumerate(positions):
            val = self.real_keys[i]
            idx = pos
            prev = positions[i - 1] if i > 0 else (pos - 1) % self.m
            while True:
                self.y[idx] = val
                if idx == pos:
                    break
                idx = (idx + 1) % self.m
        self.head = positions[0]
        self.real_indices = positions

    def get_uniform_positions(self, n, m):
        q, r = divmod(m, n)
        positions = []
        pos = 0
        for i in range(n):
            d = q + 1 if (i * r) // n < ((i + 1) * r) // n else q
            positions.append(pos)
            pos += d
        return positions

    def binary_search(self, x):
        left, right = 0, self.m - 1
        while left <= right:
            mid = (left + right) // 2
            idx = (self.head + mid) % self.m
            if self.y[idx] < x:
                left = mid + 1
            else:
                right = mid - 1
        return (self.head + left) % self.m

    def is_dummy(self, i):
        return i not in self.real_indices

    def find_insertion_index(self, x):
        for i, key in enumerate(self.real_keys):
            if key > x:
                return i
        return len(self.real_keys)

    def insert_key(self, x):
        if x in self.real_keys:
            return
        if self.n == self.nk[self.k]:
            self.rebuild_on_insert(x)
            return

    idx = self.binary_search(x)
        if self.is_dummy(idx):
            self.real_keys.insert(self.find_insertion_index(x), x)
        else:
            t = 0
            i = idx
            while not self.is_dummy((i + 1) % self.m):
                t += 1
                i = (i + 1) % self.m
            for j in range(t, -1, -1):
                from_idx = (idx + j) % self.m
                to_idx = (idx + j + 1) % self.m
                self.y[to_idx] = self.y[from_idx]
            self.y[idx] = 0
            self.real_keys.insert(self.find_insertion_index(x), x)
            if idx == self.head:
                self.head = (self.head - 1) % self.m
        self.update_size()

    def rebuild_on_insert(self, x):
        self.k += 1
        self.real_keys.append(x)
        self.real_keys.sort()
        self.m = int(self.nk[self.k] * self.mk[self.k])
        self.build_sparse_array()

    def delete_key(self, x):
        if x not in self.real_keys:
            return
        idx = self.binary_search(x)
        if self.y[idx] != x:
            return
        L = 1
        while (idx + L) % self.m < self.m and self.y[(idx + L) % self.m] == x:
            L += 1
        replace_val = self.y[(idx + L) % self.m]
        for i in range(L):
            self.y[(idx + i) % self.m] = replace_val
        self.real_keys.remove(x)
        self.update_size()
        if self.k > 1 and self.n:
            return 






