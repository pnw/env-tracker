
def find(arr, fn):
    return next((i for i in arr if fn(i)), None)
