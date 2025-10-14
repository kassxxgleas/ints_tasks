
import math

def minimax(depth, node_index, is_max, values, max_depth):
    if depth == max_depth:
        return values[node_index]
    if is_max:
        return max(
            minimax(depth + 1, node_index * 2, False, values, max_depth),
            minimax(depth + 1, node_index * 2 + 1, False, values, max_depth)
        )
    else:
        return min(
            minimax(depth + 1, node_index * 2, True, values, max_depth),
            minimax(depth + 1, node_index * 2 + 1, True, values, max_depth)
        )

leaf_values = [2, -1, 2, 3, -1, 5, 2, -4, 3, 10, -1, -2, 0, 2, 5, 10]
max_depth = int(math.log2(len(leaf_values)))
result = minimax(0, 0, True, leaf_values, max_depth)
print("Best value", result)