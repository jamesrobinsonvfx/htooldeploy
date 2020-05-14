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
# Press 'enter' to use default value from brackets
# Tool Name: (snake_case or PascalCase preferred) [my_tool].
# Author Name: [none]
# Version Number: (Semantic versioning preferred) [0.0.1]
# Will {} use its own Python library? (y/n) [y]:
# Include shelf? (y/n) [y]

# README.md >
# [Tool Name] [version]
# Created by [Author]
import os
import re


class TemplateTool(object):

    def __init__(
            self,
            parent_dir,
            name="my_tool",
            author=None,
            version="0.0.1",
            pythonlib=True,
            shelf=True
    ):
        super(TemplateTool, self).__init__()
        self.parent_dir = parent_dir
        self.name = self._sanitize_name(name)
        self.author = author
        self.version = version
        self.pythonlib = pythonlib
        self.shelf = shelf

    def __repr__(self):
        return (
            "Tool Template for {0} at {1}, Created by {2}"
            .format(self.name, self.parent_dir, self.author)
        )

    def create(self):
        root = self.root()
        self._create_readme()
        self._create_version_file()

    def _create_readme(self):
        contents = (
            "# {0} {1}".format(self._tool_title(), self.version)
        )
        icodf self.author:
            contents = "{0}\nCreated by {1}".format(contents, self.author)

        with open(os.path.join(self.root(), "README.md"), "w") as file_:
            file_.write(contents)

    def _create_version_file(self):
        with open(os.path.join(self.root(), "_version"), "w") as file_:
            file_.write(self._version_str())

    def _version_str(self):
        return "__version__ = \"{0}\"".format(self.version)

    def _tool_title(self):
        pattern = r"[-_+]"
        title = re.sub(pattern, " ", self.name).title()
        return title

    def _create_directories(self):
        # Make sure root is there
        # Create source folder
        # Create otls
        # optional shelf
        # pythonlibs
        root = self.root()
        source = self._source_dir()
        try:
            os.makedirs(os.path.join(source, "otls"))
        except OSError as error:
            pass

        mapping = {
            "shelf": self._create_shelf,
            "pythonlib": self._create_pythonlib
        }
        for k, v in mapping.items():
            if getattr(self, key):
                v()

    def _create_pythonlib(self):
        parent_dir = os.path.join(self._source_dir(), "python2.7libs")
        package_root = os.path.join(parent_dir, self.name)
        try:
            os.makedirs(package_root)
        except OSError as error:
            pass
        with open(os.path.join(package_root, "__init__.py"), "w") as file_:
            file_.write()

    def _create_shelf(self):
        toolbar_dir = os.path.join(self._source_dir(), "toolbar")
        try:
            os.makedirs(toolbar_dir)
        except:
            pass
        shelf_name = "{0}.shelf".format(self.name)
        with open(os.path.join(toolbar_dir, shelf_name), "w") as file_:
            file_.write()

    def _source_dir(self):
        source_dir = os.path.join(self.root, "source")
        try:
            os.makedirs(source_dir)
        except OSError as error:
            pass
        return source_dir

    @staticmethod
    def _sanitize_name(name):
        scrubbed_name = name
        return scrubbed_name

    def root(self):
        root_path = os.path.join(self.parent_dir, self.name)
        try:
            os.makedirs(root_path)
        except OSError:
            pass
        return root_path


def template_wizard(template_location):

    tool = TemplateTool(template_location)
    # Ask questions


if __name__ == "__main__":
    tool = TemplateTool("/tmp")
    tool.name = "sweet_tool"
    tool.author = "Starlord"
    tool.create()
