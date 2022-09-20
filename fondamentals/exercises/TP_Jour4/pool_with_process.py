from multiprocessing import Process


def f1(name):
    print('hello', name)


def f2(name):
    print('hello', name)


if __name__ == '__main__':
    
    procs = []
    p1 = Process(target=f1, args=('bob',))
    p1.start()
    procs.append(p1)
    p2 = Process(target=f2, args=('jerry',))
    p2.start()
    procs.append(p2)


    for p in procs:
        p.join()
        p.close()
