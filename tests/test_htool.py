"""Unit Tests"""
# pylint: disable=protected-access,superfluous-parens


import os
import shutil
import tempfile
import unittest
import sys

# import htooldeploy.htool
from htooldeploy.htool import HTool


if "darwin" not in sys.platform:
    TEMP_DIR = tempfile.gettempdir()
else:
    TEMP_DIR = "/tmp"
TEST_PROJECT = os.path.join(TEMP_DIR, "test_project")
TEST_TOOL_REPO = os.path.join(TEMP_DIR, "tool_repo")


def remove_dirs():
    """Remove testing directories from temp"""
    try:
        shutil.rmtree(TEST_PROJECT)
        print "Removed Test Project"
    except OSError:
        pass
    try:
        shutil.rmtree(TEST_TOOL_REPO)
        print "Removed Test Tool Repo"
    except OSError:
        pass


class TestHtool(unittest.TestCase):
    """Unit tests"""

    @classmethod
    def setUpClass(cls):
        remove_dirs()

    def setUp(self):
        # Only create some, so --force can be tested
        print "\n"
        dirs = ["otls", "toolbar"]
        for dir_ in dirs:
            dirpath = os.path.join(TEST_PROJECT, dir_)
            try:
                os.makedirs(dirpath)
                print "Created ", dirpath
            except OSError:
                continue

        tool_source = os.path.join(os.path.abspath("."), "tests", "test_tool")
        shutil.copytree(tool_source, TEST_TOOL_REPO)
        print "Copied {0} to {1}".format(tool_source, TEST_TOOL_REPO)

    def tearDown(self):
        remove_dirs()

    def test_user_prefs(self):
        """Something is returned for User Preferences"""
        tool = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT
        )
        self.assertIsNotNone(tool._find_user_prefs_dir())

    def test_installable(self):
        """Test Tool is always an installable tool"""
        tool = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT
        )
        self.assertTrue(tool.installable())

    def test_install_develop_mode(self):
        """Add a package to project packages"""
        package_path = os.path.join(
            TEST_PROJECT, "packages", "tool_repo-0.0.1.json"
        )
        tool = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT,
            develop=True,
            force=True
        )
        self.assertTrue(tool.install())
        self.assertTrue(os.path.isfile(package_path))

    def test_install(self):
        """A normal installation"""
        tool = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT,
            force=True
        )
        self.assertTrue(tool.install())
        project_result = {
            "python2.7libs": "test_tool",
            "otls": "example_testtool.hda",
            "toolbar": "test_tool.shelf"
        }
        for dir_, subdir in project_result.items():
            dirpath = os.path.join(TEST_PROJECT, dir_)
            subdirpath = os.path.join(dirpath, subdir)
            self.assertTrue(os.path.exists(dirpath))
            self.assertTrue(os.path.exists(subdirpath))

    def test_no_force(self):
        """Install without force flag"""
        tool = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT
        )
        self.assertFalse(tool.install())
