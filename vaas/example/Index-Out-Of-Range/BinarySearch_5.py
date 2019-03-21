def binarySearch(arr, first, last, element):
    mid = first + last / 2
    print(mid)
    print(arr[mid])
    if last >= first:
        if (element == arr[mid]):
            print(element)
        else:
            if (element > arr[mid]):
                return binarySearch(arr, mid + 1, last, element)
            else:
                return binarySearch(arr, first, mid - 1, element)
    else:
        print("Element is not present in array")
from ontology.builtins import *

def Main():
    arr = [2,3,4,5,6]
    element = 5
    binarySearch(arr, 0, len(arr) - 1, element)
