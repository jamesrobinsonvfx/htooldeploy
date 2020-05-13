"""Houdini Tool

The :class:`HTool` object is used to deploy Site-Structured Houdini
tools.

Site-Structured?
    Some tools exist simply as otls, which are easily copied and pasted
    around. Other tools act more like suites. Job tools might have a
    whole dedicated python library, a custom 456.py script, a shelf,
    etc. If a tool repo is structured the same as a typical Houdini
    Site, this structure, along with Houdini's new Packages feature,
    makes it really straightforward to install and develop tools quickly
    in new locations.

.. note::
    This format would work well even with simple otls. Each one would
    have a docs page...or actually just a help/ in the source/ folder.

.. seealso::
    `Houdini Packages <https://www.sidefx.com/docs/houdini/ref/
    plugins.html>`_ &
    `Configuring Houdini <https://www.sidefx.com/docs/houdini/basics/
    config.html>`_
"""
import json
import logging
import os
import re
import shutil
import sys

from distutils.dir_util import copy_tree

HOUDINI_SITE_DIRS = [
    "desktop", "dso", "gallery", "geo", "help", "ocio", "otls", "presets",
    "python2.7libs", "python3.7libs", "python_panels", "scripts", "soho",
    "toolbar", "vex", "vop", "viewer_states"
]

logger = logging.getLogger("htooldeploy")


class HTool(object):
    """A basic Houdini Tool object, capable of verifying and installing
    itself.
    """
    # pylint: disable=too-many-instance-attributes,too-many-arguments

    def __init__(
            self,
            source_tool_repo=None,
            install_destination=None,
            develop=False,
            force=False,
            cleanup=False,
            hou_version=None,
            verbosity=3,
            dry_run=False
    ):
        """Constructor for HTool object.

        :param source_tool_repo: Tool repository root, defaults to None
        :type source_tool_repo: str
        :param install_destination: Install directory, defaults to None
        :type install_destination: str, optional
        :param develop: :ref:`Development Mode`, defaults to False
        :type develop: bool, optional
        :param force: Create missing target dirs, defaults to False
        :type force: bool, optional
        :param cleanup: Remove source repository root after install,
            defaults to False
        :type cleanup: bool, optional
        :param hou_version: Houdini ``MAJOR.MINOR`` version to install
            to in User Preferences, defaults to None
        :type hou_version: float or str, optional
        :param verbosity: Console output level from 0-3, 3 being the
            most verbose, defaults to 3
        :type verbosity: int, optional
        :param dry_run: Execute all selected functions without creating
            or removing directories, defaults to False
        :type dry_run: bool, optional
        """

        super(HTool, self).__init__()

        self.source_repo = source_tool_repo
        self._install_destination = install_destination
        self.develop = develop
        self.force = force
        self.cleanup = cleanup
        self.verbosity = verbosity
        self.dry_run = dry_run

        self._user_prefs_dir = self._find_user_prefs_dir(
            version=hou_version
        )

        if dry_run:
            logger.log(100, "{0}Dry Run{0}".format("-"*24))
        self.installable()

    def installable(self):
        """Determine if the tool is installable.

        A tool is considered installable if its source folder contains
        one or more :ref:`Houdini Site Folders`.

        :return: Whether or not the tool can be installed
        :rtype: bool
        """
        for dir_ in os.listdir(self.source_path()):
            dir_path = os.path.join(self.source_path(), dir_)
            if dir_ in HOUDINI_SITE_DIRS and os.path.isdir(dir_path):
                logger.info("{0} is installable".format(self.tool_name()))
                return True

        error_msg = (
            "{0} is uninstallable. No site directories exist. Aborting."
            .format(self.tool_name())
        )
        logger.info(error_msg)
        sys.exit()

    def install(self):
        """Install the tool.

        Install in Development Mode if user input requires.

        :return: Success
        :rtype: bool
        """
        success = False

        logger.debug("Tool source: {0}".format(self.source_path()))
        logger.debug("Install path: {0}".format(self.target_path()))

        if self.develop:
            logger.info("Installing in Development Mode")
            logger.debug("Creating JSON Package")
            logger.debug("Adding package to {0}".format(self.target_path()))
            success = self._add_json_package()
        else:
            logger.info("Installing {0}".format(self.tool_name()))
            success = self._copy_source_to_target()
        return success

    def source_path(self, repo_convention="source"):
        """Infer the source directory to copy from.

        The user inputs a path to a top level tool repo. Inside the repo
        there will typically be either a ``source/`` or ``site/``
        directory that contains the folders to copy. This method points
        us to the folder whose contents will actually be copied over or
        referenced (if using the ``--develop`` flag).

        :source_dir: User-supplied source directory
        :type source_dir: `str`
        :param repo_convention: Where the  :ref:`Houdini Site Folders`
            live in the repo, defaults to "source" for now.
        :type repo_convention: str, optional
        :return: Path to the source site directory
        :rtype: str
        """
        try:
            source_dir = os.path.join(self.source_repo, repo_convention)
        except AttributeError:
            error_msg = ("No tool repo supplied. Aborting.")
            logger.error(error_msg)
            sys.exit()
        if not os.path.isdir(source_dir):
            error_msg = (
                "No {0} directory found in tool {1}. Aborting."
                .format(repo_convention, self.tool_name())
            )
            logger.error(error_msg)
            sys.exit()

        return os.path.abspath(source_dir)

    def target_path(self):
        """Directory to copy source files to.

        Defaults to the user's Houdini User Preferences in their home
        directory if no target path was supplied. If in Development
        Mode, ``packages/`` is appended to the target installation
        directory.

        :return: Directory to copy to
        :rtype: str
        """
        target_dir = self._install_destination
        if not target_dir:
            target_dir = self._user_prefs_dir
        target_dir = os.path.abspath(target_dir)
        if self.develop:
            target_dir = os.path.join(target_dir, "packages")

        return target_dir

    def tool_name(self):
        """Infer a short name for the tool from its repo path.

        :return: Tool name
        :rtype: str
        """
        return os.path.basename(self.source_repo)

    def tool_version(self):
        """Attempt to find the source tool's version.

        If a file in the tool repo's root contains ``__version__ =``
        it will be used as the tool's version in the json package.

        :return: Tool version string
        :rtype: str
        """
        version_str = None
        logger.debug(
            "Searching for version string for {0}".format(self.tool_name())
        )
        root = self.source_repo
        root_files = [
            x for x in os.listdir(root)
            if os.path.isfile(os.path.join(root, x))
        ]
        for item in root_files:
            file_path = os.path.join(root, item)
            with open(file_path, "r") as file_:
                for line in file_.readlines():
                    pattern = r"__version__\s+=\s+[\"\'](.+)[\"\']"
                    match = re.match(pattern, line)
                    if match:
                        version_str = match.groups()[0]
                        logger.debug(
                            "{0} version found in {1}"
                            .format(self.tool_name(), file_path)
                        )
                        logger.info(
                            "{0} version: {1}"
                            .format(self.tool_name(), version_str)
                        )
                        break
        if not version_str:
            logger.debug("No version for {0} found".format(self.tool_name()))

        return version_str

    def _copy_source_to_target(self):
        """Copy dirctories in the repo's ``source/`` to the installation
        target.

        :raises Exception: Missing target directories, no force flag.
        """
        source_dirs = [
            x for x in os.listdir(self.source_path())
            if not x.startswith(".") and x in HOUDINI_SITE_DIRS
        ]
        missing_dirs = [
            x for x in source_dirs
            if x not in os.listdir(self.target_path())
        ]
        if missing_dirs and not self.force:
            error_msg = (
                "Missing the following site directories in installation "
                "target:\n\t{0}\nTry running again with the \"--force\" flag"
                .format(
                    "\n\t".join(["{0}/".format(x) for x in missing_dirs]))
            )
            logger.error(error_msg)
            return False

        for dir_name in source_dirs:
            source = os.path.join(self.source_path(), dir_name)
            target = os.path.join(self.target_path(), dir_name)
            logger.info("Copying {0} to {1}".format(source, target))
            if not self.dry_run:
                copy_tree(source, target)

        if self.cleanup:
            try:
                logger.info("Removing {0}".format(self.source_repo))
                if not self.dry_run:
                    shutil.rmtree(self.source_repo)
            except OSError:
                logger.warning(
                    "Unable to clean up {0}".format(self.source_repo)
                )

        return True

    def _add_json_package(self):
        """Add a Houdini Package entry to the installation target.

        Append the tool's source directory to ``HOUDINI_PATH`` so that
        Houdini can pick up the tool while it still lives in a
        convenient development area.

        :return: Success
        :rtype: bool
        """
        success = False

        package_name = "{0}.json".format(self.tool_name())
        tool_version = self.tool_version()
        if tool_version:
            package_name = "{0}-{1}.json".format(
                self.tool_name(),
                tool_version
            )
        package_file = os.path.join(self.target_path(), package_name)
        if os.path.isfile(package_file) and not self.force:
            logger.warning("A Houdini Package with this name already exists.")
            input_ = None
            responses = {"y": True, "n": False}
            while input_ not in responses.keys():
                input_ = raw_input("Overwrite? (y/n): ").lower()
            confirm = responses[input_]
            if not confirm:
                logger.warning(
                    "Try removing the existing file, or running again "
                    "with the \"--force\" flag"
                )
                return False
        elif not os.path.isdir(self.target_path()):
            if not self.force:
                msg = (
                    "Missing packages directory in installation target "
                    "directory. Try running with the \"--force\" flag"
                )
                logger.error(msg)
                return False
            else:
                logger.debug(
                    "Creating packages directory {0}".format(
                        self.target_path())
                )
                if not self.dry_run:
                    os.makedirs(self.target_path())
        package_entry = {"path": self.source_path()}
        if self.dry_run:
            logger.debug("Package contents: {0}".format(package_entry))
            return True

        with open(package_file, "w") as file_:
            json.dump(package_entry, file_, indent=4)

        with open(package_file, "r") as file_:
            data = json.load(file_)
            if data == package_entry:
                logger.debug("JSON readback successful")
                success = True

        return success

    def _find_user_prefs_dir(self, version=None):
        """Find the user's Houdini Preferences directory.

        Use the version override if provided, otherwise search for
        the latest Houdini version. If no ``HOUDINI_USER_PREF_DIR`` has
        been set, look in ``$HOME``.

        .. seealso ::
            `hconfig <https://www.sidefx.com/docs/houdini/basics/
            config_env.html>`_

        :param version: Houdini ``MAJOR.MINOR`` version to search for,
            defaults to None
        :type version: float, str, optional
        :return: Path to user preferences directory for the given
            Houdini version.
        :rtype: str
        """
        user_prefs = os.getenv("HOUDINI_USER_PREF_DIR")
        version = version if version else self._latest_houdini_version()
        logger.debug("Searching Houdini version: {0}".format(version))
        if not user_prefs:
            user_prefs = os.path.join(
                os.path.expanduser("~"),
                "houdini{0}".format(self._latest_houdini_version())
            )
        elif "__HVER__" in user_prefs:
            user_prefs = user_prefs.replace("__HVER__", version)
        if not os.path.isdir(user_prefs):
            logger.error("{0} does not exist. Aborting.".format(user_prefs))
            sys.exit()

        logger.debug("User Preferences directory: {0}".format(user_prefs))
        return user_prefs

    @staticmethod
    def _latest_houdini_version():
        """Find the latest Houdini version in a user's home directory.

        :return: Highest Houdini ``MAJOR.MINOR`` version available
        :rtype: float
        """
        home = os.path.expanduser("~")
        pattern = r"houdini(\d\d\.\d)"
        versions = list()
        for item in os.listdir(home):
            path = os.path.join(home, item)
            match = re.match(pattern, item)
            if match and os.path.isdir(path):
                versions.append(match.groups()[0])

        return max(versions)
