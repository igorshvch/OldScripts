from multiprocessing import Pool, Process, Queue
import os

def f(q):
    q.put([42, None, 'hello'])

def f2(x, q):
    for i in range(10000):
        2**640
    print('done!')
    q.put(sum(x))

def f3(x):
    for i in range(10000):
        2**640
    print('done!', sum(x), os.getpid())
    return sum(x)

data = [[1,2,3],[4,5,6],[7,8,9], [10,11,12]]

if __name__ == '__main__':
    print([1,2,3])
    print(os.getppid(), os.getpid())
    holder = []
    with Pool(processes=4) as pool:
        holder.append(pool.map(f3, data))
        z = pool.apply_async(os.getpid, ())
        print(z.get())
        print(holder)

'''
if __name__ == '__main__':    
    q = Queue()
    print(os.getppid(), os.getpid())
    for i in data:
        p = Process(target=f2, args=(i, q))
        p.start()
        print(os.getppid(), os.getpid(), q.get())    # prints "[42, None, 'hello']"
        p.join()
'''
