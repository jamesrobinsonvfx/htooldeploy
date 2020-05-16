Creating a Tool from a Template
===============================

If you're starting a tool from scratch, or migrating an existing one, consider
creating the directories with ``htooldeploy`` and the ``--template`` flag. A
wizard will prompt you for a few details about the project, and create a
directory structure in the given location.

.. code-block:: bash

   cd ~/dev
   htooldeploy --template .

You can press "enter" to quickly create blast through the options, or provide
you own settings.

::

    Starting htooldeploy
    Welcome to the Template Tool Wizard
    Press 'enter' to use default value from brackets
    Tool Name  [my_tool]: furball_generator
    Author  [None]: JJ Abrams
    Version  [0.0.1]:
    Will furball_generator need its own Python library? (y/n) [y]:
    Include blank shelf? (y/n) [y]:
    Do you plan on using furball_generator with Git? (y/n) [y]:
    See log at /tmp/htooldeploy/htooldeploy_1589583158.log for detailed output
    Exiting

Git Option
**********

If you choose ``y`` at the last line regarding Git, check the ``otls/``
directory. You'll find a couple of shell scripts: ``bin_to_ascii.sh`` and
``ascii_to_bin.sh``. These are useful for converting your hdas between ascii
and binary format. ASCII hdas allow for useful diffing when using version
control like Git.

There is also a basic ``.gitignore`` at the root level, along with
a ``README.md``.

.. note::
   Unfortunately, SESI has locked these features to paid licenses of Houdini.
   Apprentice users are unable to convert hdas.