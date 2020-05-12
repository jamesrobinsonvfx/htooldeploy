Installing
==========


It's always good practice to create a `Virtual Environment
<https://virtualenv.pypa.io/en/latest/>`_ when installing new tools.

.. code-block:: bash

    cd ~
    mkdir .virtualenv
    virtualenv -p /usr/bin/python .virtualenvs htooldeploy

Then installation is easy with ``pip``. Navigate to the cloned
repository. In my case, it is located in ``/Users/james/dev``.

.. code-block:: bash

    cd ~/dev/htooldeploy
    pip install -r .


To quickly build and open the docs, use the shell script

.. code-block:: bash

    chmod +x docs.sh
    ./docs.sh


If you plan on editing the source code while using ``htooldeploy``, you
can ``pip install`` in development mode using the ``install.sh``
installation shell script.

.. code-block:: bash

    chmod +x install.sh
    ./install.sh