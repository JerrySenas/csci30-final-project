#!/usr/bin/env python3

from picture import Picture
import math

class SeamCarver(Picture):
    ## TO-DO: fill in the methods below
    def energy(self, i: int, j: int) -> float:
        '''
        Return the energy of pixel at column i and row j

        Milestone 1 (pytest -m m1)
        '''
        if i < 0 or j < 0 or i >= self.width() or j >= self.height():
            raise IndexError("Pixel out of bounds.")

        # x-gradients
        if i + 1 == self.width():
            right_pixel = self[0, j]
        else:
            right_pixel = self[i + 1, j]

        if i - 1 < 0:
            left_pixel = self[self.width() - 1, j]
        else:
            left_pixel = self[i - 1, j]

        # y-gradients
        if j + 1 == self.height():
            bottom_pixel = self[i, 0]
        else:
            bottom_pixel = self[i, j + 1]

        if j - 1 < 0:
            top_pixel = self[i, self.height() - 1]
        else:
            top_pixel = self[i, j - 1]

        delta_x = (
            (right_pixel[0] - left_pixel[0])**2 +
            (right_pixel[1] - left_pixel[1])**2 +
            (right_pixel[2] - left_pixel[2])**2
        )

        delta_y = (
            (bottom_pixel[0] - top_pixel[0])**2 +
            (bottom_pixel[1] - top_pixel[1])**2 +
            (bottom_pixel[2] - top_pixel[2])**2
        )

        return math.sqrt(delta_x + delta_y)

    def find_vertical_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        vertical seam

        Milestone 2 (pytest -m m2)
        '''
        M = [[0] * self.width() for x in range(self.height())]
        parent = [[0] * self.width() for x in range(self.height())] # tracks parent indices

        for i in range(self.width()):
            M[0][i] = self.energy(i, 0)

        for j in range(1, self.height()):
            for i in range(self.width()):
                # min() compares the energy, then the column index itself if the energies are equal, which should be fine
                candidates = [(M[j-1][i], i)]
                if i > 0:
                    candidates.append((M[j-1][i-1], i-1))
                if i < self.width()-1:
                    candidates.append((M[j-1][i+1], i+1))

                cheapest_candidate = min(candidates)
                M[j][i] = self.energy(i, j) + cheapest_candidate[0]
                parent[j][i] = cheapest_candidate[1]

        bottom_row = []
        for i in range(self.width()):
            bottom_row.append((M[(self.height()-1)][i], i))

        cheapest_end = min(bottom_row)
        current_col = cheapest_end[1]
        seam = [current_col]

        for j in range(self.height()-1, 0, -1):
            current_col = parent[j][current_col]
            seam.append(current_col)

        seam.reverse()
        return seam

    def transpose(self):
        '''
        Transpose the picture by rotating it 90 degrees clockwise.
        The picture's width will now be the original height and its height its original width.
        '''

        original_width = self._width
        original_height = self._height
        original_picture = [ [self[i, j] for i in range(self._width)] for j in range(self._height) ]
        # Note that the list is indexed with [j][i]

        self.clear()

        self._width = original_height
        self._height = original_width

        for j in range(self._height):
            for i in range(self._width):
                self[i, j] = original_picture[i][j]

    def find_horizontal_seam(self) -> list[int]:
        '''
        Return a sequence of indices representing the lowest-energy
        horizontal seam

        Milestone 3 (pytest -m m3)
        '''
        self.transpose()
        seam = self.find_vertical_seam()
        self.transpose()

        return seam

    def remove_vertical_seam(self, seam: list[int]):
        '''
        Remove a vertical seam from the picture

        Milestone 4 (pytest -m m4)
        '''
        raise NotImplementedError

    def remove_horizontal_seam(self, seam: list[int]):
        '''
        Remove a horizontal seam from the picture

        Milestone 5 (pytest -m m5)
        '''
        raise NotImplementedError

class SeamError(Exception):
    pass
