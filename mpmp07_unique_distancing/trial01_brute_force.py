import numpy as np
import matplotlib.pyplot as plt

# Flatten grid

def encode_point(x, y, num_rows, num_cols):
    return y*num_cols + x

def decode_point(i, num_rows, num_cols):
    y = i // num_cols
    x = i - y*num_cols
    return (x, y)

def decode_markers(case):
    bin_string = f"{case:b}"
    # The 1s in this string correspond to where the markers are
    # The bin_string needs to be reversed because the least significant bit
    # corresponds to the board position (0, 0)
    return [i for i, c in enumerate(reversed(bin_string)) if c == '1']

def euclidean_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return np.sqrt((x1 - x2) ** 2. + (y1 - y2) ** 2.)

def manhattan_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def chebyshev_distance(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return max(abs(x1 - x2), abs(y1 - y2))

def valid(markers, num_rows, num_cols, metric, verbose=False):
    # Loop over points pairwise to find distances.
    # If any pairwise distance is the same, the case is invalid. Return False.
    # Otherwise, return the list of distances.
    # Otherwise, the
    distances_seen = []
    for i, p1 in enumerate(markers):
        # Decode the point
        p1 = decode_point(p1, num_rows, num_cols)
        for p2 in markers[i+1:]:
            # Decode the point
            p2 = decode_point(p2, num_rows, num_cols)
            # Find the distance and check if it's been seen
            d = metric(p1, p2)
            if d in distances_seen:
                distances_seen.append(d)
                if verbose:
                    print(distances_seen)
                return False
            distances_seen.append(d)
    return distances_seen

def plot_case(markers, nrows, ncols, title=None, filename=None):
    # Convert markers to points
    points = [decode_point(i, nrows, ncols) for i in markers]
    # Create a list of non-marker points
    non_marker_points = [decode_point(i, nrows, ncols) for i in range(nrows*ncols) if i not in markers]
    # Plot markers as x's and non-markers as dots
    plt.figure()
    plt.plot([p[0] for p in points], [p[1] for p in points], 'ro')
    plt.plot([p[0] for p in non_marker_points], [p[1] for p in non_marker_points], 'bx')
    if title:
        plt.title(title)
    if filename:
        plt.savefig(filename)
        plt.close('all')
    else:
        plt.show()

def brute_force(n, metric_list, break_on_first=True):
    # Represent the markers as a binary string
    start_case = ''.join(['1', ] * n)
    # This is equivalent to 2**n - 1
    # Convert this binary string to an int
    start_case = int(start_case, 2)
    # Now we can use the decode_markers function to convert this to marker
    # positions. And we can move markers around the grid by incrementing
    # the case number.
    # Before that, what is the maximum case number that can fit on this grid?
    max_case_num = ''.join(['1', ] * n) + ''.join(['0', ] * (n*n - n))
    # This is four 1's in the four MSBs
    # Convert this to a binary string to an int as well
    max_case_num = int(max_case_num, 2)
    # Now iterate
    for case in range(start_case, max_case_num+1):
        markers = decode_markers(case)
        # The number of markers should equal n
        # If not, skip this case
        if len(markers) != n:
            continue
        print(f"{case} / {max_case_num}: {markers}")
        # Check against all metrics and print valid cases
        for metric in metric_list:
            distances = valid(markers, n, n, metric)
            if distances:
                print(f"*** {n}|{metric.__name__}|{case}|{case:b}|{markers}|{distances}")
                plot_case(
                    markers, n, n,
                    title=f"Case {case} ({case:b}) on {n} x {n} using {metric.__name__}",
                    filename=f"markers_{n}_{case}_{metric.__name__}",
                )
                if break_on_first:
                    break


if __name__ == "__main__":
    for n in range(3, 8):
        brute_force(n, [euclidean_distance, manhattan_distance, ], break_on_first=False)

