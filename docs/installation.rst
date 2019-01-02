============
Installation
============

gastop can either be install from PyPI, or directly by cloning the git repository and installing manually.

From PyPI
*********

The easiest way to install gastop is to use pip to install from PyPI:

.. code-block:: bash

	$ pip install gastop

This will install the base package, and shortcuts to use gastop from the command line. However, this will not install additional components such as the test suite and sample config files.

From GitHub
***********

gastop can also be built from source by cloning the git repository.

.. code-block:: bash

	$ git clone https://github.com/f0uriest/GASTOp.git

Once cloned, it can be installed by running

.. code-block:: bash

	$ python setup.py install
	
from within the repository home folder. This will install the base package and command line shortcut. The git repository also contains the test suite and sample config files. The test suite can be run from the main folder with

.. code-block:: bash

	$ python -m pytest

Please note that the tests may take several minutes to run.
