.. _Development Mode:

Development Mode
================

It is very likely that you will need to actively develop some elements of a
tool during a project, like a python library, and will need to periodically
commit changes to some sort of version control system like Git. This can make
tracking and installing your tool to each project a real chore, especially if
you've got several directories to keep track of.

Instead of copying the source files to their destination like a normal install,
``htooldeploy`` takes advantage of `Houdini Packages <https://www.sidefx.com/
docs/houdini/ref/plugins.html>`_. A JSON file is added to the installation
location's ``packages/`` directory, and appends the working tool source to the
``HOUDINI_PATH``. This allows you to continue working with the tool in your dev
space, while changes are still picked up by the project, or your home folder,
hsite or wherever you decided to install the tool.

When it's time to install the tool for real, just remove the Houdini Package
JSON file that was added to the install destination's ``packages/`` folder, and
run ``htooldeploy`` in its default configuration without the ``--develop``
flag.

.. seealso::

    `Houdini Packages <https://www.sidefx.com/docs/houdini/ref/plugins.html>`_.