Overview
========

``htooldeploy`` is a simple commandline tool for quick & easy installation of
your slightly more "robust" tools.

Motivation
**********
Houdini's HDAs are are really great in that they are super easy to toss around
between projects, users, machines, etc. But when tools start to get a little
more involved, and you start adding shelves, custom python libraries, maybe
some viewer states, vex includes...It can get a bit messy keeping track of all
of it and making sure everything gets installed and loaded up how it should on
your next Houdini launch, especially if you're sharing a tool and don't want
the end user to have to worry about which folder to copy where.

How it Works
************
``htooldeploy`` expects a path to the tool's root level. Inside, there should
be a ``source/`` directory. ``htooldeploy`` will find that source directory and
either copy its contents to the desired installation location, or when running
in :ref:`Development Mode`, create a new Houdini Package and link to the tool's
current location on disk.

Luckily, the great people over at SideFX have made it really easy. By
structuring our tools in a consistent way and following a couple of easy rules,
the process is really straightforward.

1. Your tool should follow a pre-determined structure mirroring the one SESI
   uses everywhere: The ``HOUDINI_PATH`` format found in ``$HFS/houdini``.
   :ref:`Houdini Site Folders` has a more detailed list.

2. If the tool is to be installed somewhere other than your predetermined
   HSITE, or Houdini User Preferences directory, make sure that that location
   is included in your ``HOUDINI_PATH``.

.. note::
  Facilities will usually have a "wrapper" that loads a custom environment
  for each shot. These will typically be added to the ``HOUDINI_PATH`` for
  you, but you can check with your TDs to make sure, or run ``hconfig`` in
  the terminal to inspect relevant Houdini environment variables.

.. seealso::
  Check out `Houdini Packages <https://www.sidefx.com/docs/houdini/
  ref/plugins.html>`_ for more information on how to add to your own
  ``HOUDINI_PATH``

.. seealso::
  `hconfig <https://www.sidefx.com/docs/houdini/basics/config_env.html>`_



Limitations
***********

- This is not a package management tool. It does not check for conflicting
  or existing tools, nor does it check for conflicting or redundant python
  packages
- Does not have uninstall function (but maybe in the future)
- Development Mode Houdini Packages must be manually deleted before doing a
  real install

.. warning::
  ``htooldeploy`` does not currently backup otls if they already exist in the
  installation directory. This will be addressed in a future release.



Contact
*******
If you do decide to use ``htooldeploy``, and have any questions about how to
use it, any bugs to report, or feature requests, please feel free to email me
at james@jamesrobinsonvfx.com, or head over to the `Git Repository.
<https://github.com/jamesrobinsonvfx/htooldeploy/tree/master>`_