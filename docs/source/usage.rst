Usage
=====

This page provides the basic usage of the ``amiet_self_noise`` package. 

``amiet_self_noise`` has been built to be used from a terminal, by providing the inputs thought a combination of command line arguments and a configuration file (written in YAML). This allows to easily run the code with multiple parameters throught simple bash scripts. However, it is also possible to use the package as a library, by importing the ``amiet_self_noise`` module in a Python script. This is useful for more complex use cases, such as running the code in a Jupyter notebook or integrating it into a larger Python, or to perform additional pre or postprocessing. For a more detailed description of the available functions, see the ``amiet_self_noise`` :doc:`module <modules>` documentation.

.. _target-to-input-files:

Input files
-----------

The ``amiet_self_noise`` package requires that the user provides all the necessary inputs as a YAML file. This is intented to reduce the necessity to interact directly with the source code itself, but to still allow for a large flexibility in the inputs. The YAML file should contain all the necessary parameters to run the Amiet model, such as the airfoil geometry, the flow conditions, and the desired output parameters.  YAML was developed as a more human-readable version of the JSON format, but it is read similarly in Python. YAML file entries are composed of key-value pairs, where the key is a string and the value can be a string, a number, a list, or another dictionary, for example:

.. code-block:: yaml
    :caption: ``config.yaml``

    L: 1.0 # The span length of the airfoil, in meters
    U: 100.0 # The freestream velocity, in m/s
    data_path: /path/to/data # The path to the input data files

This file will be converted to a Python dictionary as:

.. code-block:: python

    config = {
        'L': 1.0,  
        'U': 100.0,  
        'data_path': '/path/to/data' 
    }

Notice, string do not need to be quoted. The YAML file can also contain comments, which are preceded by a `#` character. Sub-dictionaries are identified using the indentation level (usually 2 spaces):

.. code-block:: yaml
    :caption: ``config.yaml``

    airfoil:
      name: NACA0012 # The name of the airfoil
      thickness: 0.12 # The thickness of the airfoil, in meters
      chord: 1.0 # The chord length of the airfoil, in meters

which will be converted to:

.. code-block:: python

    config = {
        'airfoil': {
            'name': 'NACA0012',  
            'thickness': 0.12,  
            'chord': 1.0  
        }
    }

Finally, lists are represented using the `-` character at the begininng of a line, or using square brackets `[]`:

.. code-block:: yaml
    :caption: ``config.yaml``

    frequencies: [100, 200, 300]
    angles: 
      - 0.0 
      - 5.0
      - 10.0

.. code-block:: python

    config = {
        'frequencies': [100, 200, 300],  
        'angles': [0.0, 5.0, 10.0]  
    }

The ``amiet_self_noise`` package requires the following keys in the YAML file:

.. code-block:: yaml
    :caption: ``config.yaml``

    b: 1.0   # The airfoil semichord, in meters (float)
    L: 1.0   # The span length of the airfoil, in meters (float)
    T: 300.0 # The temperature, in Kelvin (float)
    U: 100.0 # The freestream velocity, in m/s (float)
    #
    data_path: /path/to/data.h5 # The path to the data files
    data_type: dns # Type of the input data, for now can only be 'dns' (string)
    mesh_path: /path/to/mesh.5  # The path to the mesh file, if applicable
    #
    obs:
    - [0.0, 0.0, 0.0] # The cartesian coordinates of the observer, 
    - [0.0, 0.0, 1.0] # w.r.t the trailing edge, in meters (list of lists)
    #
    xprobes: 0 # The index of the probe in the chord-wise direction.
    yprobes: 0 # The index of the probe in the span-wise direction.

The ``xprobes`` and ``yprobes`` are used to select the probes in the input data. They can be a single integer, a list of integers or ``'null'``. In the last two cases, they get converted to slice objects. Passing an int will select a probe at that index. Passing a list ``[a,b]`` will result in secting the probes from ``a`` to ``b`` (``b`` not included), as in ``np.array[a:b]``. Passing ``'null'`` will select all the probes in that direction, as in ``np.array[:]``.

