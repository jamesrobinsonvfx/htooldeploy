Examples
=========

Install a tool to your Houdini User Preferences folder (Home)
*************************************************************
::

    htooldeploy ~/dev/test_tool

Install a tool to you Houdini User Preferences Folder in Development Mode
*************************************************************************
::

    htooldeploy --develop ~/dev/test_tool

Test an Installation
********************
::

    cd project_folder
    htooldeploy -v 3 --develop ~/dev/test_tool .

Install and Remove Source
*************************
::

    htooldeploy -v 3 --cleanup ~/dev/test_tool

.. note::
    Development Mode will ignore the ``--cleanup`` flag


Install into a Different Version of Houdini
*******************************************
::

    htooldeploy --hou-version 17.5 ~/dev/test_tool

