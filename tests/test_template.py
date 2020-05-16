"""Unit Tests"""
# pylint: disable=protected-access,superfluous-parens


import os
import shutil
import sys
import tempfile
import unittest


from htooldeploy.template import TemplateTool

if "darwin" not in sys.platform:
    TEMP_DIR = tempfile.gettempdir()
else:
    TEMP_DIR = "/tmp"

TOOL_NAME = "washed_out"
TOOL_PATH = os.path.join(TEMP_DIR, TOOL_NAME)


def remove_dirs():
    """Remove testing directories from temp"""
    try:
        shutil.rmtree(TOOL_PATH)
        print "Removed Test Project"
    except OSError:
        pass


class TestTemplateTool(unittest.TestCase):
    """Unit tests"""

    def tearDown(self):
        remove_dirs()

    def test_tool_exists(self):
        """Raise an error if the tool exists"""
        os.makedirs(TOOL_PATH)
        template = TemplateTool(TEMP_DIR)
        template.name = TOOL_NAME
        self.assertRaises(OSError, template.create)

    def test_tool_created(self):
        """Create a tool template"""
        template = TemplateTool(
            TEMP_DIR,
            name="washed_out",
            author="Luke Skywalker",
            version="1.1.0",
            pythonlib=True,
            shelf=True,
            help_card=True,
            git=True
        )
        dirs = [
            "/tmp/washed_out",
            "/tmp/washed_out/source",
            "/tmp/washed_out/source/python2.7libs",
            "/tmp/washed_out/source/python2.7libs/washed_out",
            "/tmp/washed_out/source/otls",
            "/tmp/washed_out/source/toolbar",
            "/tmp/washed_out/source/help/nodes"
        ]
        files = [
            "/tmp/washed_out/source/python2.7libs/washed_out/__init__.py",
            "/tmp/washed_out/source/toolbar/washed_out.shelf",
            "/tmp/washed_out/_version",
            "/tmp/washed_out/README.md",
            "/tmp/washed_out/.gitignore",
            "/tmp/washed_out/source/otls/ascii_to_bin.sh",
            "/tmp/washed_out/source/otls/bin_to_ascii.sh"
        ]
        help_categories = ["obj", "sop", "dop", "cop2", "out"]

        template.create()
        for dir_ in dirs:
            self.assertTrue(os.path.isdir(dir_))
        for file_ in files:
            self.assertTrue(os.path.isfile(file_))
        for cat in help_categories:
            dirpath = os.path.join("/tmp/washed_out/source/help/nodes", cat)
            self.assertTrue(os.path.isdir(dirpath))

    def test_sanitized_name(self):
        """Name has no whitespaces or non-word characters"""
        template = TemplateTool(TEMP_DIR)
        name_1 = "my$$$$tool"
        template.name = name_1
        self.assertEqual(template.name, "my____tool")
        name_2 = "superC00l tool"
        template.name = name_2
        self.assertEqual(template.name, "superC00l_tool")

    def test_name_title(self):
        """Titled name has whitespaces and capital letters"""
        template = TemplateTool(TEMP_DIR)
        name_1 = "colorado_avalanche"
        template.name = name_1
        self.assertEqual(template._tool_title(), "Colorado Avalanche")
        # name_2 = "OldMan2"
        # self.assertEqual(template._tool_title(), "Old Man 2")
