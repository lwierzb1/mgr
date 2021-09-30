__author__ = "Łukasz Wierzbicki"
__version__ = "1.0.0"
__maintainer__ = "Łukasz Wierzbicki"
__email__ = "01113202@pw.edu.pl"

from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.affinity_optimized_solver import \
    AffinityOptimizedSolver
from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.neighbor_optimized_solver import \
    NeighborOptimizedSolver
from colorization_program.src.colorization_algorithm.colorization_using_optimization.image.weights_solver import WeightsSolver
from colorization_program.src.toolkit.mathematical import to_seq


class WeightsOptimizedSolver(WeightsSolver):
    def __init__(self):
        super().__init__(NeighborOptimizedSolver(), AffinityOptimizedSolver())

    def compute_wrs(self, has_hints, y_channel):
        height = has_hints.shape[0]
        width = has_hints.shape[1]
        image_coordinates, neighbors_coordinates, wrs = [], [], []

        for row in range(height):
            for col in range(width):
                if not has_hints[row][col]:
                    neighbors = self._neighbor_solver.find_neighbors((row, col), y_channel)
                    weights = self._affinity_solver.compute_affinity(y_channel[(row, col)], neighbors[:, 2])
                    for idx in range(len(weights)):
                        image_coordinates.append(to_seq(row, col, height))
                        neighbors_coordinates.append(to_seq(neighbors[idx][0], neighbors[idx][1], height))
                        wrs.append(weights[idx])
                image_coordinates.append(to_seq(row, col, height))
                neighbors_coordinates.append(to_seq(row, col, height))
                wrs.append(1.)
        return image_coordinates, neighbors_coordinates, wrs
