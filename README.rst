######
GASTOp
######

|PyPI-Version| |Python-Version|

|Build-Status| |Coveralls| |Codacy|

|Doc-Status| |License|


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


.. |Build-Status| image:: https://travis-ci.org/f0uriest/GASTOp.svg?branch=dev
    :target: https://travis-ci.org/f0uriest/GASTOp
    :alt: Build Status
.. |Coveralls| image:: https://coveralls.io/repos/github/f0uriest/GASTOp/badge.svg?branch=dev
    :target: https://coveralls.io/github/f0uriest/GASTOp?branch=dev
    :alt: Code Coverage
.. |Codacy| image:: https://api.codacy.com/project/badge/Grade/a0d2ec5d32e948db8076596c7af69995
    :target: https://www.codacy.com/app/f0uriest/GASTOp?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=f0uriest/GASTOp&amp;utm_campaign=Badge_Grade   
    :alt: Code Quality
.. |Doc-Status| image:: https://readthedocs.org/projects/gastop/badge/?version=latest
    :target: https://gastop.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
.. |License| image:: https://img.shields.io/badge/License-GPLv3-blue.svg
    :target: https://github.com/f0uriest/GASTOp/blob/master/LICENSE
    :alt: License: GPL v3
.. |Python-Version| image:: https://img.shields.io/pypi/pyversions/gastop.svg
    :target: https://pypi.org/project/gastop
    :alt: Python versions supported
.. |PyPI-Version| image:: https://img.shields.io/pypi/v/gastop.svg
    :target: https://pypi.org/project/gastop/
    :alt: Current Release
