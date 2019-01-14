==========
Quickstart
==========

GASTOp is a **G**\ enetic **A**\ lgorithm for **S**\ tructural design and **T**\ opological **Op**\ timization.
Given a set of boundary conditions such as applied loads and fixtures, it will design a structure to support those loads while minimizing weight and deflections and maximize factor of safety. 


Installation
************

Install gastop by running:

.. code-block:: bash
		
    $ pip install gastop
	

Usage
*****

Look how easy it is to use:

.. code-block:: python
		
   import gastop
   config_file_path = "./path_to_config_file.txt"
   ga = gastop.GenAlg(config_file_path)
   ga.initialize_population(pop_size=1e4)
   best_truss, history = ga.run(num_generations=100, progress_display=1, num_threads=4)


Contribute
**********

- Issue Tracker: `<https://github.com/f0uriest/GASTOp/issues>`_
- Source Code: `<https://github.com/f0uriest/GASTOp/>`_
- Documentation: `<https://gastop.readthedocs.io/>`_
  

License
*******

The project is licensed under the GNU GPLv3 license.
