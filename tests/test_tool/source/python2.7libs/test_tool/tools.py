"""Tools

An external python module to help demonstrate the test_tool tutorial.
"""
import hou


def tool_1(message):
    """Shelf tool 1"""
    hou.ui.displayMessage(message)


def tool_2(message):
    """Shelf tool 2"""
    hou.ui.displayConfirmation(message)


def tool_3(message):
    """Shelf tool 3"""
    hou.ui.displayMessage(message, severity=hou.severityType.Warning)


def flippy():
    """Make a flippy"""
    geo = hou.node("/obj").createNode("geo", "Flipster")
    geo.createNode("testgeometry_rubbertoy")


def on_created(kwargs):
    """OnCreated script to use in Test Tool's event handler"""
    node = kwargs["node"]
    color = hou.Color(0.5, 0.5, 0.35)

    node.setColor(color)
    hou.ui.displayMessage(
        "Hey there, I'm the Test Tool!",
        title="Howdy",
        severity=hou.severityType.Message
    )
