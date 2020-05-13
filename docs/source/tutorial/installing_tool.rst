Installing :ref:`Test Tool` to Home Directory
=============================================
Now that we are done making changes to :ref:`Test Tool`, it's time we install it
for real. Let's go ahead and remove the Houdini Package that was added when we
installed using :ref:`Development Mode`::

    cd ~/houdini18.0/packages
    rm htooldeploy-test_tool-0.0.1.json

Great, now we can go ahead and install just like we did before, only we can
omit the ``--develop`` flag.

Dry Run
^^^^^^^
Before we do anything for real though, let's first do a dry run. Using the
``--dry-run`` flag, we can run the installation and see if it's successful
without actually creating any new directories or copying anything just yet.

Let's also turn up the verbosity (``-v``) so we can watch what's happening a
little more closely::

    htooldeploy -v 3 --dry-run ~/dev/htooldeploy-test_tool/

Missing folders
^^^^^^^^^^^^^^^
Whoops! There's been an error!::

    Missing the following site directories in installation target:
        python2.7libs/
        otls/
    Try running again with the "--force" flag

If the source tool's folders don't exist in the target installation directory,
you either need to make them yourself, or run ``htooldeploy`` with the
``--force`` flag. This tells ``htooldeploy`` to make the missing directories
for you. Let's run it one more time, this time using the ``--force`` flag. We
can skip the ``--dry-run`` this time too::

    htooldeploy -v 3 --force ~/dev/htooldeploy-test_tool

Installed
^^^^^^^^^
Success! Now if we launch Houdini again, we'll see all of the :ref:`Test Tool`
components just like before, only now they've been copied to our home User
Preferences directory::

    cd ~/houdini18.0
    ls otls python2.7libs toolbar

::

    otls:
    example_testtool.hda

    python2.7libs:
    test_tool

    toolbar:
    default.shelf           shelf_tool_assets.json  test_tool.shelf


Installing Test Tool to Project
===============================

So far, we have left the installation target blank. Without a value,
``htooldeploy`` will always default to the highest Houdini Version in your
Houdini User Preferences folder.

.. note::
   Try using the ``--hou-version`` flag to specify a different ``MAJOR.MINOR``
   version, ie. ``--hou-version 17.5`` if you need to install to an earlier
   version.

We can also install anywhere on our ``HOUDINI_PATH``. For this example, I have
a project called **coolproject**. Inside, there there is a ``houdini`` folder,
which has all the typical Houdini folders you'd expect for a shot. Let's
install :ref:`Test Tool` there.

Cleanup
^^^^^^^
Since this is the last time we'll be using this tool in this location, let's
also try out the ``--cleanup`` flag::

   htooldeploy -f --cleanup ~/dev/htooldeploy-test_tool ~/Projects/coolproject/houdini

.. warning::
    The ``--cleanup`` flag attempts to delete the source tool repo's root
    after installation. Only use it if you're okay with blasting the source
    away!
