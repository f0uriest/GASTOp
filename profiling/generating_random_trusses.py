"""generate_random_trusses.py
This file is a part of the profiling scripts for GASTOp
Authors: Amlan Sinha, Cristian Lacey, Daniel Shaw, Paul Kaneelil, Rory Conlin, Susan Redmond
Licensed under GNU GPLv3.
This module implements tests for generating random trusses

"""

### Generating the random trusses ###
# Try 1: Time: 0.579
# Ranges = domain[1]-domain[0]
# new_nodes = np.random.rand(num_rand_nodes, 3)
#
# for j in range(3):
#     new_nodes[:, j] = new_nodes[:, j]*Ranges[j] + \
#         domain[0][j]*np.ones(num_rand_nodes)

# Try 2: Time: 0.499
# nn1 = np.random.rand(num_rand_nodes, 1)*Ranges[0] + domain[0][0]
# nn2 = np.random.rand(num_rand_nodes, 1)*Ranges[1] + domain[0][1]
# nn3 = np.random.rand(num_rand_nodes, 1)*Ranges[2] + domain[0][2]
# new_nodes = np.concatenate((nn1,nn2,nn3),axis=1)

# Try 3: Time: 0.451
# new_nodes = np.empty([num_rand_nodes,3])
# for j in range(3):
#     new_nodes[:,j] = np.random.rand(num_rand_nodes)*Ranges[j] + domain[0][j]

# Try 4: Time: 0.433!
# new_nodes = np.random.uniform(
#     domain[0], domain[1], (num_rand_nodes, 3))

### Initializing the population ###

# Try 1: t= 0.298
# self.population = []
# for i in tqdm(range(pop_size), total=pop_size, leave=False, desc='Initializing Population', position=0):
#     self.population.append(self.generate_random())

# Try 2: t= 0.352
# pool = Pool()
# result_list = [pool.map_async(self.generate_random, ()) for i in range(pop_size)]
#
# self.population = [res.get() for res in result_list]

# Try 3: t=0.343
# pool = Pool()
# pool.map_async(self.generate_random, range(pop_size),callback=self.population.extend)
# pool.close()
# pool.join()

# Try 4: t=0.232
# pool = Pool()
# self.population = list(tqdm(pool.imap(
#     self.generate_random, range(pop_size), int(np.sqrt(pop_size))), total=pop_size, leave=False, desc='Initializing Population', position=0))
# pool.close()
# pool.join()
