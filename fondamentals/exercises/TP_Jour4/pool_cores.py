import multiprocessing as mp
import numpy as np
from multiprocessing import Pool


def f(x):
    return x * x


cores = mp.cpu_count()
print(cores)
arr = np.random.randint(5, size=(100, 100))
arr_list = np.array_split(arr, cores, axis=0)

if __name__ == '__main__':
    
    with Pool(cores) as p:
        arr_list = p.map(f, arr_list)
        print(np.vstack(arr_list).shape)
