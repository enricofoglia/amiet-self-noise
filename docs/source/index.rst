Welcome to amiet-self-noise
===========================

``amiet-self-noise`` is a library built to help researchers and engineers to predict airfoil self-noise from experimental or simulation data using the Amiet model. 

.. note::

   This project is being developed as a final project for the course GMC729 (Aeroacoustics) at the University of Sherbrooke, under the supervision of Prof. S. Moreau.


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   usage
   theory
   modules

Quickstart: running the example code 
------------------------------------

If you wish to use ``amiet_self_noise`` as a standalone to quickly analyze some existing data, you can do so by running the script ``main.py`` which is included with the rest of the code. Here's how to do it:

1. Download the code from github. If you have git installed on your machine, you can simply clone the repository as:

.. code-block:: bash

   git clone https://github.com/enricofoglia/amiet-self-noise.git

Otherwise, at the same link, it is possible to download a zipped version of the package. Unzip it where you need your code to be run.

2. Once the package has been copied on your machine, open a terminal and navigate to the ``amiet_self_noise`` directory, where the ``main.py`` file is located.

3. Modify the ``config.yaml`` file in your preferred text editor.

4. Make sure you have all the required packages installed (check the ``pyproject.toml`` file, under "dependencies").

5. Run:

.. code-block:: bash

   python main.py


Usage example
-------------

Using ``amiet_self_noise`` in your own python projects is as easy as writing four lines of code:

.. code-block:: python
   
   # 1. import the module
   import amiet_self_noise as asn
   # 2. read the data from the configuration file
   input_data = asn.io_utils.InputData("config.yaml", normalize=True)
   # 3. initialize the model
   model = asn.amiet_model.AmietModel(input_data)
   # 4. compute the PSD
   f, psd = model.compute_psd()

Read more about the configuration files in the :ref:`dedicated page <target-to-input-files>`.
