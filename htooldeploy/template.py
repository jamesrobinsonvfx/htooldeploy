"""Template

When running ``htooldeploy`` with the ``--template`` flag, the user can
create a simple tool development structure ready for version control
and deployment.

htooldeploy --template .

::

  tool_name/
    _version
    README.md
    source/
      python2.7libs/
        test_tool/
          __init__.py
      otls/
      toolbar/
        test_tool.shelf
"""
import logging
import os
import re
import shutil
import xml.etree.cElementTree as ET
from xml.dom import minidom

# pylint: disable=superfluous-parens
logger = logging.getLogger("htooldeploy")


class TemplateTool(object):
    """Template tool object for creating Tool directories"""
    # pylint: disable=too-many-arguments

    def __init__(
            self,
            parent_dir,
            name="my_tool",
            author=None,
            version="0.0.1",
            pythonlib=True,
            shelf=True,
            git=True
    ):
        super(TemplateTool, self).__init__()
        self.parent_dir = parent_dir
        self._name = self._sanitize_name(name)
        self.author = author
        self.version = version
        self.pythonlib = pythonlib
        self.shelf = shelf
        self.git = git

    def __repr__(self):
        return (
            "Tool Template for {0} at {1}, Created by {2}"
            .format(self._name, self.parent_dir, self.author)
        )

    def create(self):
        """Create template files and directories"""
        self.exists()
        self._create_directories()
        self._create_readme()
        self._create_version_file()

    def exists(self):
        """Determine if the tool already exists.

        :raises error: Tool already exists
        :return: Existence of tool
        :rtype: bool
        """
        try:
            os.makedirs(os.path.join(self.parent_dir, self._name))
        except OSError as error:
            if "File exists" in error:
                logger.error(
                    "This tool already exists in {0}".format(self.parent_dir)
                )
                raise error
        return False

    @property
    def name(self):
        """Name of the tool.

        :return: Tool name
        :rtype: str
        """
        return self._name

    @name.setter
    def name(self, name):
        self._name = self._sanitize_name(name)

    def _create_readme(self):
        """Create README.md and fill its Heading 1"""
        contents = (
            "# {0} {1}".format(self._tool_title(), self.version)
        )
        if self.author:
            contents = "{0}\nCreated by {1}".format(contents, self.author)

        with open(os.path.join(self.root(), "README.md"), "w") as file_:
            file_.write(contents)

    def _create_version_file(self):
        """Create version tracker file"""
        with open(os.path.join(self.root(), "_version"), "w") as file_:
            file_.write(self._version_str())

    def _git_prep(self):
        resource = os.path.join(os.path.dirname(__file__), "resource")
        gitignore = os.path.join(resource, "gitignore")
        shell_scripts = ["bin_to_ascii.sh", "ascii_to_bin.sh"]
        try:
            shutil.copy2(gitignore, os.path.join(self.root(), ".gitignore"))
        except OSError as error:
            if "File exists" in error:
                print("exist")
                # pass
        for file_ in shell_scripts:
            filepath = os.path.join(resource, file_)
            shutil.copy2(
                filepath, os.path.join(
                    self._source_dir(), "otls", file_
                )
            )

    def _version_str(self):
        """Create a Version String to save in the _version file.

        :return: Version string
        :rtype: str
        """
        return "__version__ = \"{0}\"".format(self.version)

    def _tool_title(self):
        """Nice name for the tool.

        .. todo::
           Add CamelCase conversion

        :return: A nice, titled name without underscores
        :rtype: str
        """
        pattern = r"[-_+]"
        title = re.sub(pattern, " ", self._name).title()
        # name = re.sub(r'(?<!^)(?=[A-Z0-9])', ' ', oldname).title()
        return title

    def _create_directories(self):
        """Create child directories"""
        self.root()
        source = self._source_dir()
        self._makedir(os.path.join(source, "otls"))
        mapping = {
            "shelf": self._create_shelf,
            "pythonlib": self._create_pythonlib,
            "git": self._git_prep
        }
        for key, value in mapping.items():
            if getattr(self, key):
                value()

    def _create_pythonlib(self):
        """Create Python Library

        Includes tool's name, as well as an ``__init__.py``
        """
        parent_dir = os.path.join(self._source_dir(), "python2.7libs")
        package_root = self._makedir(os.path.join(parent_dir, self._name))
        with open(os.path.join(package_root, "__init__.py"), "w") as file_:
            file_.write("")

    def _create_shelf(self):
        """Create toolbar folder and dummy shelf file"""
        toolbar_dir = self._makedir(
            os.path.join(self._source_dir(), "toolbar")
        )
        shelf_file = os.path.join(toolbar_dir, "{0}.shelf".format(self._name))
        sesi_comment = (
            "This file contains definitions of shelves, toolbars, and tools.\n"
            "It should not be hand-edited when it is being used by the\n"
            "application. Note, that two definitions of the same element are\n"
            "not allowed in a single file. "
        )
        doc = ET.Element("shelfDocument")
        ET.SubElement(
            doc, "toolshelf", name=self._name, label=self._tool_title()
        )
        comment = ET.Comment(sesi_comment)
        doc.insert(0, comment)
        # declaration = """<?xml version="1.0" encoding="UTF-8"?>"""
        xmlstr = minidom.parseString(ET.tostring(doc)).toprettyxml(indent="  ")
        with open(shelf_file, "w") as file_:
            file_.write(xmlstr)

    def root(self):
        """Get the root directory for the tool.

        :return: Tool root
        :rtype: str
        """
        root_path = self._makedir(os.path.join(self.parent_dir, self._name))
        return root_path

    def _source_dir(self):
        """Create directory for the :ref:`Houdini Site Folders`"""
        source_dir = self._makedir(os.path.join(self.root(), "source"))
        return source_dir

    @staticmethod
    def _sanitize_name(name):
        """Conform name to standard.

        Replace all non-word and whitespace characters with "_".

        : param name: Name to sanitize
        : type name: str
        : return: Sanitized name
        : rtype: str
        """
        pattern = r"[\W\s+]"
        scrubbed_name = re.sub(pattern, "_", name)
        return scrubbed_name

    @staticmethod
    def _makedir(path):
        """EAFP directory creation.

        :param path: Directory to create
        :type path: str
        :return: Directory path, None if not created
        :rtype: str, None
        """
        try:
            os.makedirs(path)
            logger.debug("Created {0}".format(path))
        except OSError as error:
            if "File exists" not in error:
                logger.error("Unable to create {0}".format(path))
        return path if os.path.isdir(path) else None


class WizardLine(object):
    """Prompt line to retrieve user input with"""

    def __init__(
            self,
            prompt_str,
            valid_input=("y", "n"),
            default="None"
    ):
        """Constructor for Wizard Line.

        :param prompt_str: Prompt to user
        :type prompt_str: str
        :param valid_input: Valid responses. ["*"] to accept any
        :type valid_input: list
        :param default: Default value if none provided by user
        :type default: str
        """
        super(WizardLine, self).__init__()
        self.valid_input = valid_input
        self.default = default
        self._prompt = self._format_prompt(prompt_str)
        self.value = None

    def __str__(self):
        return self._prompt

    def __repr__(self):
        return self._prompt

    def show_prompt(self):
        """Prompt the user for :meth:`raw_input`"""
        user_input = None
        if self.valid_input == "*":
            pattern = r"(\w+)"
        else:
            pattern = "(^[{0}])".format("".join(self.valid_input))
        while not user_input:
            user_input = raw_input(self._prompt)
            match = re.match(pattern, user_input)
            if match:
                if match.groups()[0] == user_input:
                    break
            elif user_input == "":
                user_input = self.default
        self.value = self._check_value(user_input)
        return self

    @property
    def prompt(self):
        """Prompt string.

        :return: Prompt string with options and defaults
        :rtype: str
        """
        return self._prompt

    @prompt.setter
    def prompt(self, prompt):
        self._prompt = self._format_prompt(prompt)

    def _format_prompt(self, prompt):
        """Format prompt into a nice string.

        :param prompt: Question for user
        :type prompt: str
        :return: Prompt string with options and defaults
        :rtype: str
        """
        if "*" not in self.valid_input:
            valid_input_display = "({0})".format(
                "/".join(self.valid_input))
        else:
            valid_input_display = str()

        return "{0} {1} [{2}]: ".format(
            prompt,
            valid_input_display,
            self.default
        )

    @staticmethod
    def _check_value(value):
        """Check value for common remappings.

        :param value: Value to check
        :type value: str
        :return: Remapped response
        :rtype: bool/str
        """
        common_responses = {
            "y": True,
            "n": False
        }
        return common_responses.get(value, value)


def template_wizard(template_location):
    """Command-line tool to gather information from the user and create
    a tool template.

    :param template_location: Directory in which to create the tool.
    :type template_location: str
    """
    template_location = os.path.abspath(template_location)
    tool = TemplateTool(template_location)
    print("Welcome to the Template Tool Wizard")
    print("Press 'enter' to use default value from brackets")

    tool.name = WizardLine(
        "Tool Name", valid_input="*", default="my_tool"
    ).show_prompt().value
    tool.author = WizardLine("Author", valid_input="*").show_prompt().value
    tool.version = WizardLine(
        "Version", valid_input="*", default="0.0.1").show_prompt().value
    tool.pythonlib = WizardLine(
        "Will {0} need its own Python library?".format(tool.name), default="y"
    ).show_prompt().value
    tool.shelf = WizardLine(
        "Include blank shelf?", default="y"
    ).show_prompt().value
    tool.git = WizardLine(
        "Do you plan on using {0} with Git?".format(tool.name), default="y"
    ).show_prompt().value
    tool.create()


if __name__ == "__main__":
    MOD = __import__("htooldeploy.__main__", fromlist=["log"])
    LOG = MOD.log(3)

    template_wizard("/tmp")
