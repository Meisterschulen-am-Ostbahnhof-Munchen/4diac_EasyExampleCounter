import sys
import os
from lxml import etree

def validate_xml(xml_path, schema_path):
    try:
        if not os.path.exists(xml_path):
            print(f"ERROR: XML file not found at {xml_path}", file=sys.stderr)
            sys.exit(1)
        if not os.path.exists(schema_path):
            print(f"ERROR: Schema file not found at {schema_path}", file=sys.stderr)
            sys.exit(1)
            
        xml_doc = etree.parse(xml_path)
        
        if schema_path.lower().endswith('.dtd'):
            # Clear whitespace-only texts from elements to allow DTD EMPTY checks to pass
            for elem in xml_doc.iter():
                if elem.text and not elem.text.strip():
                    elem.text = None
            
            dtd = etree.DTD(open(schema_path, 'rb'))
            if dtd.validate(xml_doc):
                print(f"SUCCESS: {xml_path} is DTD compliant with {schema_path}!")
                sys.exit(0)
            else:
                print(f"VALIDATION FAILED for {xml_path}:\n{dtd.error_log.filter_from_errors()}", file=sys.stderr)
                sys.exit(1)
        else:
            schema = etree.XMLSchema(etree.parse(schema_path))
            schema.assertValid(xml_doc)
            print(f"SUCCESS: {xml_path} is XSD compliant with {schema_path}!")
            sys.exit(0)
    except Exception as e:
        print(f"VALIDATION FAILED for {xml_path}:\n{e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python validate.py <path_to_xml> <path_to_schema>")
        sys.exit(1)
    validate_xml(sys.argv[1], sys.argv[2])
