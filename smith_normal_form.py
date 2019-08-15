import numpy as np


def smith_normal_form(arr):
    """Calculate the Smith normal form of an n times m matrix.

    The algorithm is from the book "Elements of Algebraic Topology" by James R.
    Munkres.

    Parameters
    ----------
    arr : np.array
        The matrix as a numpy matrix.

    Returns
    -------
    np.array
        Smith normal form of the matrix.
    """
    def divides_row(i, j):
        # Make sure that the smallest element divides every other element in the same row
        for k in range(arr.shape[1]):
            if arr[i, k] == 0:
                continue
            elif arr[i, k] % arr[i, j] == 0:
                continue
            else:
                q = arr[i, k] // arr[i, j]
                arr[:, k] = arr[:, k] - q * arr[:, j]
                if abs(arr[i, k]) < abs(arr[i, j]):
                    return (i, k)
        return True

    def divides_column(i, j):
        # Make sure that the smallest element divides every other element in the same column
        for k in range(arr.shape[0]):
            if arr[k, j] == 0:
                continue
            elif arr[k, j] % arr[i, j] == 0:
                continue
            else:
                q = arr[k, j] // arr[i, j]
                arr[k] = arr[k] - q * arr[i]
                if abs(arr[k, j]) < abs(arr[i, j]):
                    return (k, j)
        return True

    def divides_every_element(i, j, top_left_index):
        # Make sure that the minimal entry divides every element in the matrix
        for s in range(top_left_index, arr.shape[0]):
            for t in range(top_left_index, arr.shape[1]):
                if arr[s, t] == 0:
                    continue
                elif arr[s, t] % arr[i, j] == 0:
                    continue
                else:
                    q = arr[s, j] / arr[i, j]
                    if arr[s, j] + q * arr[i, j] != 0:
                        q = -q
                    arr[s] = arr[s] + q * arr[i]
                    arr[i] = arr[i] + arr[s]
                    return False
        return True

    def find_minimal_entry(top_left_index):
        minimal_entry_index = None
        minimal_entry = np.infty
        for i in range(top_left_index, arr.shape[0]):
            for j in range(top_left_index, arr.shape[1]):
                if arr[i, j] == 0:
                    continue
                elif abs(arr[i, j]) < abs(minimal_entry):
                    minimal_entry = arr[i, j]
                    minimal_entry_index = (i, j)
        return minimal_entry_index


    for top_left_index in range(len(arr)):
        if top_left_index == arr.shape[1]:
            break

        # Step 1
        # Find the minimal entry and make sure it divides all of the other elements in the matrix.
        while True:
            out = find_minimal_entry(top_left_index)
            if out is None:
                return arr
            i, j = out
            out = divides_column(i, j)
            if out != True:
                continue
            out = divides_row(i, j)
            if out != True:
                continue
            if divides_every_element(i, j, top_left_index):
                break

        # Step 2
        # Move the minimal entry to top left corner
        if i != top_left_index:
            tmp = arr[top_left_index].copy()
            arr[top_left_index] = arr[i]
            arr[i] = tmp
        if j != top_left_index:
            tmp = arr[:, top_left_index].copy()
            arr[:, top_left_index] = arr[:, j]
            arr[:, j] = tmp

        # Make the minimal entry positive
        if arr[top_left_index, top_left_index] < 0:
            arr[top_left_index] = -arr[top_left_index]

        # Make the elements in the same column as the minimal entry zeros
        for i in range(top_left_index + 1, arr.shape[0]):
            if arr[i, top_left_index] == 0:
                continue
            arr[i] = arr[i] - arr[i, top_left_index] // arr[top_left_index, top_left_index] * arr[top_left_index]

        # Make the elements in the same row as the minimal entry zeros
        arr[top_left_index, top_left_index + 1:] = 0
    return arr
