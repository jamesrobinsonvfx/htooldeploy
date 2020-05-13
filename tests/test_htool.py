"""Unit Tests"""
# pylint: disable=protected-access,superfluous-parens


import os
import shutil
import tempfile
import unittest
import sys

import htooldeploy.htool


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
        try:
            shutil.rmtree(TEST_PROJECT)
            shutil.rmtree(TEST_TOOL_REPO)
        except OSError:
            pass

        dirs = ["otls", "toolbar"]
        for dir_ in dirs:
            try:
                os.makedirs(os.path.join(TEST_PROJECT, dir_))
            except OSError:
                continue

        tool_source = os.path.join(os.path.abspath("."), "tests", "test_tool")
        print "Copying test_tool repo from {0} to {1}".format(
            tool_source, TEST_TOOL_REPO)
        shutil.copytree(tool_source, TEST_TOOL_REPO)

    @classmethod
    def tearDownClass(cls):
        print("Removing test_project from temp")
        shutil.rmtree(TEST_PROJECT)
        print("Removing test_tool_repo from temp")
        shutil.rmtree(TEST_TOOL_REPO)

    def setUp(self):
        self.test_project = TEST_PROJECT
        self.test_tool_repo = TEST_TOOL_REPO
        self.htool = htooldeploy.htool.HTool(
            source_tool_repo=self.test_tool_repo,
            install_destination=self.test_project,
            verbosity=3
        )

    def tearDown(self):
        dirs = ["otls", "toolbar", "python2.7libs", "packages"]
        for dir_ in dirs:
            dirpath = os.path.join(TEST_PROJECT, dir_)
            if not os.path.isdir(dirpath):
                break
            for item in os.listdir(dirpath):
                itempath = os.path.join(dirpath, item)
                print("Removing {0}".format(itempath))
                try:
                    shutil.rmtree(itempath)
                except OSError:
                    continue

    def test_user_prefs(self):
        """Something is returned for User Preferences"""
        self.assertIsNotNone(self.htool._find_user_prefs_dir())

    def test_installable(self):
        """Test Tool is always an installable tool"""
        self.assertTrue(self.htool.installable())

    def test_install_develop_mode(self):
        """Add a package to project packages"""
        package_path = os.path.join(
            TEST_PROJECT, "packages", "tool_repo-0.0.1.json"
        )
        self.htool.develop = True
        self.htool.force = True
        self.assertTrue(self.htool.install())
        self.assertTrue(os.path.isfile(package_path))

    def test_install(self):
        """A normal installation"""
        self.htool.force = True
        self.assertTrue(self.htool.install())
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
