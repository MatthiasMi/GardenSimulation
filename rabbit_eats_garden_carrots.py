# !/usr/bin/env python3
# coding: utf-8

# rabbit_eats_garden_carrots.py: Simulates putting a rabbit in a garden, counting carrots it eats.
# Author: Matthias

"""
## Challenge:

A very hungry rabbit is placed in the center of a garden, represented by a rectangular N x M 2D matrix.
The values of the matrix will represent numbers of carrots available to the rabbit in each square of the garden. If
the garden does not have an exact center, the rabbit should start in the square closest to the center with the
highest carrot count.
On a given turn, the rabbit will eat the carrots available on the square that it is on,
and then move up, down, left, or right, choosing the square that has the most carrots. If there are no carrots left
on any of the adjacent squares, the rabbit will go to sleep. You may assume that the rabbit will never have to choose
between two squares with the same number of carrots.
Write a function which takes a garden matrix and returns the number of carrots the rabbit eats. You may assume the
matrix is rectangular with at least 1 row and 1 column, and that it is populated with non-negative integers.


## Example

Running the code with the following matrix should return 27:
[[5, 7, 8, 6, 3],
 [0, 0, 7, 0, 4],
 [4, 6, 3, 4, 9],
 [3, 1, 0, 5, 8]]
"""


class GardenSimulation:
    """
    A class to simulate putting a rabbit in the center of a garden, counting carrots it eats along its path.

    Attributes
    ----------
    A : numpy.array
        Garden, a rectangular $N \times M$ 2D matrix with $1 <= N, M$.
    C : tuple
        Center coordinates of garden.
    N_max : int
        Row index range maximum (inclusive).
    M_max : int
        Column index range maximum (inclusive).
    carrot_count : int
        The number of carrots the rabbit has eaten up to now.

    Methods
    -------
    get_carrot_count():
        Returns the number of carrots the rabbit has eaten up to now.
    get_rabbit_position():
        Returns the rabbit's current position.
    get_rabbit_path():
        Returns the rabbit's position history.
    set_rabbit(N: int, M: int):
        Returns the coordinates of the garden's center.
    sim_rabbit(bool: o):
        Simulates the hops of a rabbit maximizing the number of carrots it eats, recording the path through the garden.
    """
    import numpy as np

    # Garden, a rectangular N x M 2D matrix with 1 <= N, M.
    A = np.array([[0]])

    # Center coordinates of garden
    C = 0, 0

    # Index range maxima (inclusive)
    N_max = 0
    M_max = 0

    # Carrot count
    carrot_count = 0

    # Rabbit's position in the garden + history
    position = C
    path = ""

    def __init__(self, A: list = [[5, 7, 8, 6, 3], [0, 0, 7, 0, 4], [4, 6, 3, 4, 9], [3, 1, 0, 5, 8]]):
        """
        Checks user inputs.

        Parameter
        ---------
        A : list
            A rectangular N x M 2D integer matrix as list of rows (also lists) with 1 <= N, M.
        """
        import numpy as np

        # Creates a copy of user input (default), and specifies the data type that hold the carrot counts of each cell.
        A = np.array(A, dtype=np.uint32)
        self.A = A

        N, M = A.shape
        if N < 1 or M < 1:
            raise NotImplementedError("Garden is too small.")

        self.N_max = N - 1
        self.M_max = M - 1
        self.path = ""
        return

    def get_rabbit_position(self):
        return self.position

    def get_rabbit_path(self):
        return self.path

    def get_carrot_count(self):
        return self.carrot_count

    def set_rabbit(self, N: int, M: int):
        """
        Sets rabbit roughly in the garden's center, then adapts the position if needed, and returns correct coordinates.
        """

        n = N // 2
        m = M // 2

        A = self.A
        v = A[n, m]

        up = A[max(0, n - 1), m]
        left = A[n, max(0, m - 1)]
        if N % 2 and M % 2:  # 1 candidate
            return n, m

        elif N % 2:  # 2 candidates - m might need adaption
            if v < left:
                m -= 1
        elif M % 2:  # 2 candidates - n might need adaption
            if v < up:
                n -= 1
        else:  # 4 candidates - both n, m might need adaption

            diag = A[max(0, n - 1), max(0, m - 1)]
            t = max(v, diag, up, left)

            if left == t:
                m -= 1
            elif up == t:
                n -= 1
            elif diag == t:
                m -= 1
                n -= 1
            else:  # v == t
                "nothing to do"

        return n, m

    def sim_rabbit(self, o: bool = False):
        """
        Simulates the hops of a rabbit maximizing the number of carrots it eats, recording the path through the garden.
        The algorithm assumes, before the rabbit sleeps,
         + a 4-neighborhood (rather than 8-neighborhood), and
         + when reaching borders, the set of neighbors is smaller, i.e., the garden is not a torus.

        Parameters
        ==========
        o : bool
            Switch for additional textual simulation output.
        """

        A = self.A
        N, M = self.N_max, self.M_max

        if o: print(f"The rabbit is put in a {N + 1}x{M + 1}-garden with A:\n{A},")
        n, m = self.set_rabbit(N + 1, M + 1)
        # Start is guaranteed to exist
        self.C = n, m
        self.position = self.C
        if o:
            print(f"at center C = ({n},{m}), as A[{n},{m}] == {A[n, m]} is extremal of all central candidate cells.\n")

        self.path = "C"
        self.carrot_count = 0
        while (0 <= n <= N) and (0 <= m <= M) and A[n, m] > 0:
            # Increment carrot count and reset number of (available) carrots to 0.
            self.carrot_count += A[n, m]
            if o: print(f"nomnom x {A[n, m]}")
            A[n, m] = 0

            down = A[min(n + 1, N), m]
            up = A[max(0, n - 1), m]
            left = A[n, max(0, m - 1)]
            right = A[n, min(m + 1, M)]
            t = max(down, up, right, left)

            if down == t:
                n += 1
                self.path += "↓"
            elif up == t:
                n -= 1
                self.path += "↑"
            elif right == t:
                m += 1
                self.path += "→"
            elif left == t:
                m -= 1
                self.path += "←"

        self.path = self.path[:-1]
        if o: print(f"\nBefore going to sleep, the rabbit ate {self.carrot_count} carrots hopping along: {self.path}.")

        return self.carrot_count


# CONFIG
tests = []

# 4x5-matrix, with c = 27 and C = (1,2), as A[1,2] == 7
A = [[5, 7, 8, 6, 3], [0, 0, 7, 0, 4], [4, 6, 3, 4, 9], [3, 1, 0, 5, 8]]
c = 27
tests.append([A, c])

# 5x5-matrix, with c = 29 and C = (1,2), as A[1,2] == 7
A = [[5, 7, 8, 6, 3], [0, 0, 7, 0, 4], [2, 5, 2, 3, 7], [4, 6, 3, 4, 9], [3, 1, 0, 5, 8]]
c = 29
tests.append([A, c])

# 2x4-matrix, with c = 22 and C = (0,2), as A[0,2] == 9
A = [[5, 8, 9, 6], [0, 0, 7, 0]]
c = 22
tests.append([A, c])

# 1x1-matrix, with c = 5 and C = (0,0), as A[0,0] == 5
A = [[5]]
c = 5
tests.append([A, c])

# 3x2-matrix, with c = 26 and C = (1,0), as A[1,0] == 8
A = [[5, 7], [8, 6], [0, 0]]
c = 26
tests.append([A, c])

# TESTS
for A, c in tests:
    garden = GardenSimulation(A)
    cc = garden.sim_rabbit()
    cc = garden.get_carrot_count()
    if cc != c:
        print(f"Oh no, {cc} = GardenSimulation(A).get_carrot_count() != c = {c}")

# SIMULATION
additional_output = True

# Load example challenge
A, c = tests[0]
garden = GardenSimulation(A)
cc = garden.sim_rabbit(additional_output)
# cc = garden.get_carrot_count()  # alternatively
C = garden.get_rabbit_position()
c == garden.get_carrot_count()

# COMMENTS
"""
## Copy user input
```python
import copy
...
A = copy.deepcopy(A)
```
is superfluous as [default](https://numpy.org/doc/stable/reference/generated/numpy.array.html#numpy.array) is doing it.
"""
