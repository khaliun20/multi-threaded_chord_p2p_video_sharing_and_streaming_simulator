def binarySearch(alist, item):
    """
    binary search given alist and item to search for
    returns is element was found, otherwise return the last midpoint before search failed
    last midpoint is always either the predessecor or succesor to item (if the item is not found)
    """
    first = 0
    last = len(alist) - 1
    found = False

    while first <= last and not found:
        midpoint = (first + last) // 2
        if alist[midpoint] == item:
            found = True
        else:
            if item < alist[midpoint]:
                last = midpoint - 1
            else:
                first = midpoint + 1

    return found, midpoint