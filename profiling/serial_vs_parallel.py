import gastop
import timeit
import numpy as np

a = np.array([100, 500, 1000, 5000, 10000, 50000, 100000])
t_serial = np.zeros(shape=a.shape)
t_parallel = np.zeros(shape=a.shape)


for i in range(len(a)):
    setup = '''
import gastop
init_file_path = 'gastop-config/struct_making_test_init.txt'
ga = gastop.GenAlg(init_file_path)
ga.initialize_population(pop_size='''+str(a[i])+''')'''

    test_serial = '''
best,history = ga.run(num_generations=10, progress_fitness=False,progress_truss=False,num_threads=1)
    '''
    t_serial[i] = timeit.timeit(
        stmt=test_serial, setup=setup, number=1, globals=globals())/10

    test_parallel = '''
best,history = ga.run(num_generations=10, progress_fitness=False,progress_truss=False,num_threads=4)
    '''

    t_parallel[i] = timeit.timeit(
        stmt=test_parallel, setup=setup, number=1, globals=globals())/10


# plotting the data
p1 = plt.figure(1)
plt.plot(a, t_serial, 'rs', label='Serial')
plt.plot(a, t_parallel, 'g^', label='Parallel w/ 4 cores')
plt.ylabel('Avg Time/Generation (s)', fontsize=14)
plt.xlabel('Population Size', fontsize=14)
plt.axis([0, 105, 0, 0.225])
plt.legend(prop=dict(size=14))
p1.show()
