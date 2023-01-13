from multiprocessing import Pool,Process, TimeoutError
import time
import os
import math

def f(x):
    return x*x

def run3():
    start = time.perf_counter()
    # start 4 worker processes
    with Pool() as pool:
        p1=pool.apply_async(useless_function, (3,))
        p2=pool.apply_async(useless_function, (3,))
        p3=pool.apply_async(useless_function, (3,))
        p4=pool.apply_async(useless_function, (3,))
        print(p1.get())
        print(p2.get())
        print(p3.get())
        print(p4.get())


        # launching multiple evaluations asynchronously *may* use more processes
        #multiple_results = [pool.apply_async(useless_function, (3,)) for i in range(40)]
        #print([res.get() for res in multiple_results])
        print('Done')
        end = time.perf_counter()
        print(f'Finished in {round(end-start, 2)} second(s)') 
    #start = time.perf_counter()
    #useless_function, (3,)
    # useless_function, (3,)
    # useless_function, (3,)
    # useless_function, (3,)
    # print('Done')
    #end = time.perf_counter()
    #print(f'Finished in {round(end-start, 2)} second(s)') 

def square(x):
    return x * x

def useless_function(sec = 1):
    print(f'Sleeping for {sec} second(s)')
    time.sleep(sec)
    print(f'Done sleeping')

def run():
    print('cambiado2')
    start = time.perf_counter()
    inputs = [0,1,2,3,4]
    print('Start')
    with Pool() as pool:
        p1 = pool.apply_async(square,(3,) )
        p2 = pool.apply_async(square,(2,))
        val1, val2 = p1.get(), p2.get()
        print('Done')
        end = time.perf_counter()
        print(f'Finished in {round(end-start, 2)} second(s)') 
        print (val1)
        print (val2)

def run2():
    start = time.perf_counter()
    process1 = Process(target=useless_function,args = [2])
    process2 = Process(target=useless_function,args = [2])
    process1.start()
    process2.start()
    end = time.perf_counter()
    print(f'Finished in {round(end-start, 2)} second(s)') 

from multiprocessing import Process

def bubble_sort(array):
    check = True
    while check == True:
      check = False
      for i in range(0, len(array)-1):
        if array[i] > array[i+1]:
          check = True
          temp = array[i]
          array[i] = array[i+1]
          array[i+1] = temp
    return array

def run_sort():
    start = time.perf_counter()
    items=[[1,9,4,5,2,6,8,4],[1,9,9,5,2,6,8,4],[1,9,4,5,2,6,8,4],[1,9,4,5,2,6,8,4],[1,9,4,5,2,6,8,4],[1,9,4,5,2,6,8,4]]
    resp=[]
    with Pool() as pool:
      for result in pool.map(bubble_sort,items):
        resp.append(result)
    print(resp)
    end = time.perf_counter()
    print(f'Finished in {round(end-start, 3)} second(s)')

def run_sort2():
    start = time.perf_counter()
    items=[[1,9,4,5,2,6,8,4],[1,9,9,5,2,6,8,4],[1,9,4,5,2,6,8,4],[1,9,4,5,2,6,8,4],[1,9,4,5,2,6,8,4],[1,9,4,5,2,6,8,4]]
    resp=[]
    for item in items:
        result=bubble_sort(item)
        resp.append(result)
    print(resp)
    end = time.perf_counter()
    print(f'Finished in {round(end-start, 3)} second(s)')

def cube(x):
    return math.sqrt(x)

def run_cube():
    N = 1000
    start_time = time.perf_counter()
    result=[]
    with Pool() as pool:
      result = pool.map(cube, range(10,N),chunksize=10)
    print(result)
    finish_time = time.perf_counter()
    print("Program finished in {} seconds - using multiprocessing".format(finish_time-start_time))
    print("---")
    # second way, serial computation
    start_time = time.perf_counter()
    result = []
    for x in range(10,N):
      result.append(cube(x))
    print(result)
    finish_time = time.perf_counter()
    print("Program finished in {} seconds".format(finish_time-start_time))

