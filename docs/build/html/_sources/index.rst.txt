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

Usage example
-------------

Using ``amiet_self_noise`` in your projects is as easy as writing four lines of code:

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
