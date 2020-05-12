Installing htooldeploy
======================

Setting up a Virtual Environment
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
It's always a good idea to install new tools into a `Virtual Environment
<https://virtualenv.pypa.io/en/latest/>`_. Let's create one now.

.. code-block:: bash

    cd ~
    virtualenv -p /usr/bin/python .virtualenvs/htooldeploy
    source .virtualenvs/htooldeploy/bin/activate

.. note::
   I explicity set the Python interpreter using ``-p`` since my system defaults
   to Python 3.7. Yours may vary.

Installation is super easy using ``pip``::

    pip install htooldeploy

``htooldeploy`` should now be installed into our virtualenv.

.. note::
   You can verify this by looking inside the virtual environment's
   ``site-packages`` directory.

   .. code-block:: bash

        ls ~/.virtualenvs/htooldeploy/lib/python2.7/site-packages

Install ``htooldeploy`` from Source
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you would like to install ``htooldeploy`` and continue to edit the source
code, you can clone the repo and  use the ``install.sh`` script located in the
cloned repo's root directory. Make the file executable and run it ::

    cd ~/dev
    git clone https://github.com/jamesrobinsonvfx/htooldeploy.git
    cd htooldeploy
    chmod +x install.sh
    ./install.sh

Build and Launch Documentation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you'd like to build and launch the documentation in your local browser, you
can run the following ::

    chmod +x docs.sh
    ./docs.sh
