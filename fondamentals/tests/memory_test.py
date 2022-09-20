from memory_profiler import profile

@profile
def ma_func() :
    a = [1] * (10 ** 6)
    b = [2] * (2 * 10 ** 7)
    del b
    return a

ma_func()