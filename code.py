Here's the implementation of the binary search algorithm in Python:

```python
def binary_search(arr, target):
    """
    Performs a binary search on the given sorted array to find the target element.
    
    Args:
        arr (list): A sorted list of elements.
        target (any): The element to search for in the array.
    
    Returns:
        int: The index of the target element if found, otherwise -1.
    """
    left = 0
    right = len(arr) - 1
    
    while left <= right:
        mid = (left + right) // 2
        
        if arr[mid] == target:
            return mid
        elif arr[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    
    return -1
```

This function takes a sorted list `arr` and a target element `target`, and returns the index of the target element if it is found in the array, or -1 if it is not found.

The algorithm works by repeatedly dividing the search interval in half. It starts by initializing the `left` and `right` pointers to the first and last indices of the array, respectively. Then, it enters a loop that continues as long as `left` is less than or equal to `right`.

In each iteration of the loop, the algorithm calculates the midpoint `mid` of the current search interval. It then compares the element at the midpoint `arr[mid]` to the target element `target`. If they are equal, the function returns the midpoint index. If the midpoint element is less than the target, the algorithm updates the `left` pointer to `mid + 1`, effectively discarding the left half of the search interval. If the midpoint element is greater than the target, the algorithm updates the `right` pointer to `mid - 1`, effectively discarding the right half of the search interval.

If the loop completes without finding the target element, the function returns -1 to indicate that the element was not found in the array.