from multiprocessing import Pool

def func(x):
    return(a+x)
a = 2
with Pool(10) as pool:
    b = pool.map(func,range(10))

print(b)
