"""Entry point for CLI"""
import argparse
import logging
import os
import time
import sys

from .htool import HTool

LOG_LEVELS = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]


def log(verbosity):
    """Setup logger to console and file.

    :param verbosity: Verbosity level from arguments. Range 0 - 3
    :type verbosity: int
    """
    logger = logging.getLogger("htooldeploy")
    logger.setLevel(LOG_LEVELS[verbosity])

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(logging.Formatter("%(message)s"))
    logger.addHandler(console_handler)

    log_dir = "/tmp/htooldeploy/"
    try:
        os.makedirs(log_dir)
    except OSError:
        pass
    log_file = (
        "/tmp/htooldeploy/htooldeploy_{0}.log"
        .format(time.time().__trunc__())
    )
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s: %(levelname)s: [%(name)s]: %(message)s"
        )
    )
    logger.addHandler(file_handler)
    return log_file


def build_argument_parser():
    """Create the argument parser for the command-line utility.

    :return: Argument Parser
    :rtype: :class:`argparse.ArgumentParser`
    """
    parser = argparse.ArgumentParser(
        prog="htooldeploy",
        usage="%(prog)s [options] tool_source [destination_path]",
        description="Deploy Site-Structured Houdini tools.",
        epilog="Author: James Robinson (james@jamesrobinsonvfx.com)"
    )
    mutual_exlusions = parser.add_mutually_exclusive_group(required=False)

    parser.add_argument(
        "source_tool_repo",
        # metavar="PATH",
        type=str,
        action="store",
        help=(
            "Path to the source tool. Typically the tool repo root, "
            "which has a source/ or site/ subdirectory to copy from"
        )
    )
    parser.add_argument(
        "install_destination",
        # metavar="PATH",
        type=str,
        action="store",
        nargs="?",
        help=(
            "Path to target installation directory. Defaults to the "
            "latest in $HOME/houdiniX.Y"
        ),
    )
    mutual_exlusions.add_argument(
        "-d",
        "--develop",
        action="store_true",
        help=(
            "Keep contents where they are and add a Houdini Package in "
            "the target location to modify HOUDINI_PATH"
        )
    )
    mutual_exlusions.add_argument(
        "-c",
        "--cleanup",
        action="store_true",
        help="Remove tool source files after successful installation"
    )
    parser.add_argument(
        "-f",
        "--force",
        action="store_true",
        help="Force creation of target site directories if they do not exist",
    )
    parser.add_argument(
        "-v",
        "--verbosity",
        type=int,
        metavar="LEVEL",
        help=(
            "Logger output to the terminal. Ranges from 0-3, 3 being the most "
            "verbose"
        ),
        default=2,
        choices=range(4)
    )
    parser.add_argument(
        "--hou-version",
        type=str,
        action="store",
        help="When applicable, use this Houdini version intead of the latest",
        metavar="MAJOR.MINOR"
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Run selected functions without creating or removing files"
    )

    return parser


def main():
    """Execute the program"""
    parser = build_argument_parser()
    args = parser.parse_args()

    log_file = log(args.verbosity)
    logger = logging.getLogger("htooldeploy")
    logger.info("Starting htooldeploy")

    logger.debug("Arguments are {0}".format(vars(args)))
    tool = HTool(**vars(args))
    if tool.install():
        logger.info("Installation complete")
    else:
        logger.warning("Installation failed")

    logger.log(100, "See log at {0} for detailed output".format(log_file))
    logger.info("Exiting")
    sys.exit()
