import os

from lxml import etree
from typing import List, Set


def load_xml(path: str) -> etree._ElementTree:
    """Load and parse the XML file from the given path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"XML file not found: {path}")
    with open(path, "rb") as f:
        return etree.parse(f)


def load_schema(path: str) -> etree.XMLSchema:
    """Load and parse the XML schema from the given path."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Schema not found: {path}")
    with open(path, "rb") as f:
        schema_doc = etree.parse(f)
    return etree.XMLSchema(schema_doc)


def validate(xml_path: str, schema: etree.XMLSchema) -> int:
    """Validate the XML file at xml_path against the provided schema."""

    doc = load_xml(xml_path)
    valid = schema.validate(doc)

    if valid:
        print(f"VALID: {xml_path} conforms to schema")
        return 0
    else:
        print(f"INVALID: {xml_path} does not conform to schema")
        for error in schema.error_log:
            print(f"  Line {error.line}: {error.message}")
        return 1


def get_project_objects(xml_path: str, type=str | List[str]) -> Set[str]:
    """Extract project parameters from the .m1cfg file."""

    doc = load_xml(xml_path)
    params = set()

    if isinstance(type, str):
        type = [type]

    for t in type:
        for tag in doc.xpath(f"//Component[@Classname='BuiltIn.{t}']"):
            name = tag.get("Name")
            params.add(name.replace("Root.", "", 1))

    return params


def get_config_params(xml_path: str) -> Set[str]:
    """Extract configuration parameters from the .m1cfg file."""
    doc = load_xml(xml_path)
    params = set()

    for param in doc.xpath("//Parameter"):
        params.add(param.get("Name"))

    for table in doc.xpath("//Table"):
        params.add(table.get("Name"))

    return params
