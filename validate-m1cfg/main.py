"""
Validate a MoTeC .m1cfg
=======================

Validate a MoTeC .m1cfg XML file against the provided XML schema, and check that it
matches the parameters found in the corresponding .m1prj file.

Usage
-----
>>> python validate_m1cfg path/to/Project.m1cfg path/to/Project.m1prj

Requirements
------------
- lxml: `pip install lxml`
"""

import os
import sys
import argparse

# Set python path to include the action directory for imports
action_dir = os.path.dirname(os.path.abspath(__file__))
repo_root = os.path.dirname(action_dir)

if repo_root not in sys.path:
    sys.path.insert(0, repo_root)

from util import load_schema, validate, get_project_objects, get_config_params


def compare_project_config(project_path: str, config_path: str) -> int:
    """Compare parameters between project and configuration files."""

    parameters = [
        "Parameter",
        "Table",
        "IOResourceConstant",
        "Calibration",
        "IOResourceParameter",
    ]

    project_params = get_project_objects(project_path, parameters)
    config_params = get_config_params(config_path)

    missing_in_config = project_params - config_params
    extra_in_config = config_params - project_params

    code = 0

    if missing_in_config:
        print(f"INVALID: Missing parameters in {config_path}:")
        for param in sorted(missing_in_config):
            print(f"  {param}")
        code = 1

    if extra_in_config:
        print(f"INVALID: Extra parameters in {config_path}:")
        for param in sorted(extra_in_config):
            print(f"  {param}")
        code = 1

    return code


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate MoTeC .m1cfg files")
    parser.add_argument("cfgpath", help="Path to the .m1cfg file to validate")
    parser.add_argument(
        "prjpath",
        nargs="?",
        default="",
        help=(
            "Path to the corresponding .m1prj file to compare against. If not "
            "provided, only schema validation will be performed."
        ),
    )
    args = parser.parse_args()

    schema_path = os.path.join(os.path.dirname(__file__), "../schemas/m1cfg.xsd")
    schema = load_schema(schema_path)

    exit_code = validate(args.cfgpath, schema)

    if args.prjpath:
        exit_code |= compare_project_config(args.prjpath, args.cfgpath)

    sys.exit(exit_code)
