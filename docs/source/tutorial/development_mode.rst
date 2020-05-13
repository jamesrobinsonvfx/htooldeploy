Install :ref:`Test Tool` Using :ref:`Development Mode`
======================================================

Now that we're all set with the example tool repo and understand its
structure, let's install it!

If you try running ``htooldeploy`` with the ``--help`` flag, you can see the
help card.
::

    htooldeploy -h

::

    usage: htooldeploy [options] tool_source [destination_path]

The only required argument is ``tool_source``, which is the the path to the
root of the tool you want to install. We'll cover the rest of the options a
little later.

Development Mode
^^^^^^^^^^^^^^^^
First let's install :ref:`Test Tool` in :ref:`Development Mode`. This will keep
all the source files in place, but create a Houdini Package and add the tool's
source to the ``HOUDINI_PATH``. We can keep editing the source code in the
``~/dev/tools`` directory until we want to install :ref:`Test Tool` for real.
::

    htooldeploy --develop ~/dev/htooldeploy-test_tool

The output should look something like this

.. code-block:: bash

    Starting htooldeploy
    htooldeploy-test_tool is installable
    Installing in Development Mode
    htooldeploy-test_tool version: 0.0.1
    Installation complete
    See log at /tmp/htooldeploy/htooldeploy_1589309230.log for detailed output
    Exiting

What exactly happened? We called ``htooldeploy`` with the ``--develop`` flag,
and supplied the path to our :ref:`Test Tool`. So where did it go? If you
navigate to your Houdini User Preferences folder, and dive into the ``packages``
directory, you'll find the result.

.. code-block:: bash

    ls ~/houdini18.0/packages

Which shows a new Houdini Package::

    htooldeploy-test_tool-0.0.1.json

We can inspect the package with any text editor::

    vim ~/houdini18.0/packages/htooldeploy-test_tool-0.0.1.json

.. note::
   ``:q`` then ``enter`` will return you to the commandline.

.. code-block:: json

    {
        "path": "/Users/james/dev/htooldeploy-test_tool/source"
    }


``htooldeploy`` added a super simple Houdini Package that adds our tool's source
in its dev space to ``HOUDINI_PATH``. Since this package lives in our User
Preferences, it is sure to get picked up by Houdini on the next launch.

Since the package is just pointing to the dev location, we can continue to
easily make tweaks to the source, and push/pull changes using Git.

OTL Scan Path
*************
It's possible that in some setups, OTLs/HDAs are being loaded explicitly using
the ``HOUDINI_OTLSCAN_PATH`` variable. This can cause issues when installing
in :ref:`Development Mode`. If you find that everything but your otls are
showing up, try running the ``--develop`` flag with the optional argument
``--append-otlscan`` This will modify the Houdini Package to also append
``otls/`` (and/or ``hda/`` if you're using that convention) to the
``HOUDINI_OTLSCAN_PATH``.

.. code-block:: bash

   htooldeploy --develop --append-otlscan ~/dev/htooldeploy-test_tool

.. code-block:: json

    {
        "path": "/Users/james/dev/htooldeploy-test_tool/source",
        "env": [
            {
                "HOUDINI_OTLSCAN_PATH": {
                    "value": "/Users/james/deb/htooldeploy-test_tool/source/otls",
                    "method": "append"
                }
            }
        ]
    }

Destination
^^^^^^^^^^^
But how did it know to install to our home directory? Since no argument was
supplied for ``[destination_path]``, the default behaviour is to locate the user's
Houdini User Preferences directory, and use that. Of course, if you wanted to
install elsewhere, you can always add that path instead.

.. note::
   Just make sure any custom installation locations will be picked up by
   Houdini!


.. seealso::
   `Houdini Packages <https://www.sidefx.com/docs/houdini/ref/plugins.html>`_