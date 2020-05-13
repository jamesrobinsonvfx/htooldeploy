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


class TestHtool(unittest.TestCase):
    """Unit tests"""

    @classmethod
    def setUpClass(cls):
        if os.path.isdir(TEST_PROJECT):
            shutil.rmtree(TEST_PROJECT)
        if os.path.isdir(TEST_TOOL_REPO):
            shutil.rmtree(TEST_TOOL_REPO)

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
        if os.path.isdir(TEST_PROJECT):
            print "Removing Test Project"
            shutil.rmtree(TEST_PROJECT)
        # if os.path.isdir(TEST_TOOL_REPO):
            # print "Removing Test Tool Repo"
            # shutil.rmtree(TEST_TOOL_REPO)

    def test_user_prefs(self):
        """Something is returned for User Preferences"""
        ht = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT
        )
        self.assertIsNotNone(ht._find_user_prefs_dir())

    def test_installable(self):
        """Test Tool is always an installable tool"""
        ht = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT
        )
        self.assertTrue(ht.installable())

    def test_install_develop_mode(self):
        """Add a package to project packages"""
        package_path = os.path.join(
            TEST_PROJECT, "packages", "tool_repo-0.0.1.json"
        )
        ht = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT,
            develop=True,
            force=True
        )
        self.assertTrue(ht.install())
        self.assertTrue(os.path.isfile(package_path))

    def test_install(self):
        """A normal installation"""
        ht = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT,
            force=True
        )
        self.assertTrue(ht.install())
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

    # def test_tool_cleanup(self):
    #     """Remove source tool repo after successful install"""
    #     print("TESTING")
    #     self.htool.force = True
    #     self.htool.cleanup = True
    #     self.assertTrue(self.htool.install())
    #     self.assertFalse(os.path.exists(TEST_TOOL_REPO))

    def test_z_another_install(self):
        """Another normal installation"""
        ht = HTool(
            source_tool_repo=TEST_TOOL_REPO,
            install_destination=TEST_PROJECT,
            force=True
        )
        self.assertTrue(ht.install())

# Multiple installs in the same test suite cause failure....
