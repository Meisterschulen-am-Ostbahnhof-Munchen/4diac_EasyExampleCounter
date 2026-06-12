import sys
import os
from lxml import etree

STANDARD_ELEMENTS = {
    "Identification": {
        "children": [],
        "attributes": {
            "Standard": False,
            "Classification": False,
            "ApplicationDomain": False,
            "Function": False,
            "Type": False,
            "Description": False
        }
    },
    "VersionInfo": {
        "children": [],
        "attributes": {
            "Organization": True,
            "Version": True,
            "Author": True,
            "Date": True,
            "Remarks": False
        }
    },
    "CompilerInfo": {
        "children": ["Compiler"],
        "attributes": {
            "header": False,
            "classdef": False
        }
    },
    "Compiler": {
        "children": [],
        "attributes": {
            "Language": True,
            "Vendor": True,
            "Product": True,
            "Version": True
        }
    },
    "FBNetwork": {
        "children": ["FB", "EventConnections", "DataConnections", "AdapterConnections"],
        "attributes": {}
    },
    "FB": {
        "children": ["Parameter"],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "EventConnections": {
        "children": ["Connection"],
        "attributes": {}
    },
    "DataConnections": {
        "children": ["Connection"],
        "attributes": {}
    },
    "AdapterConnections": {
        "children": ["Connection"],
        "attributes": {}
    },
    "Connection": {
        "children": [],
        "attributes": {
            "Source": True,
            "Destination": True,
            "Comment": False,
            "dx1": False,
            "dx2": False,
            "dy": False
        }
    },
    "FBType": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "InterfaceList", "BasicFB", "FBNetwork", "Service"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "InterfaceList": {
        "children": ["EventInputs", "EventOutputs", "InputVars", "OutputVars", "Sockets", "Plugs"],
        "attributes": {}
    },
    "EventInputs": {
        "children": ["Event"],
        "attributes": {}
    },
    "EventOutputs": {
        "children": ["Event"],
        "attributes": {}
    },
    "InputVars": {
        "children": ["VarDeclaration"],
        "attributes": {}
    },
    "OutputVars": {
        "children": ["VarDeclaration"],
        "attributes": {}
    },
    "Sockets": {
        "children": ["AdapterDeclaration"],
        "attributes": {}
    },
    "Plugs": {
        "children": ["AdapterDeclaration"],
        "attributes": {}
    },
    "Event": {
        "children": ["With"],
        "attributes": {
            "Name": True,
            "Type": False,
            "Comment": False
        }
    },
    "With": {
        "children": [],
        "attributes": {
            "Var": True
        }
    },
    "VarDeclaration": {
        "children": [],
        "attributes": {
            "Name": True,
            "Type": True,
            "ArraySize": False,
            "InitialValue": False,
            "Comment": False
        }
    },
    "AdapterDeclaration": {
        "children": ["Parameter"],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "BasicFB": {
        "children": ["InternalVars", "ECC", "Algorithm"],
        "attributes": {}
    },
    "InternalVars": {
        "children": ["VarDeclaration"],
        "attributes": {}
    },
    "ECC": {
        "children": ["ECState", "ECTransition"],
        "attributes": {}
    },
    "ECState": {
        "children": ["ECAction"],
        "attributes": {
            "Name": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "ECTransition": {
        "children": [],
        "attributes": {
            "Source": True,
            "Destination": True,
            "Condition": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "ECAction": {
        "children": [],
        "attributes": {
            "Algorithm": False,
            "Output": False
        }
    },
    "Algorithm": {
        "children": ["VarDeclaration", "FBD", "ST", "LD", "Other"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "ST": {
        "children": [],
        "attributes": {
            "Text": False
        }
    },
    "Other": {
        "children": [],
        "attributes": {
            "Language": True
        }
    },
    "Service": {
        "children": ["ServiceSequence"],
        "attributes": {
            "RightInterface": True,
            "LeftInterface": True,
            "Comment": False
        }
    },
    "ServiceSequence": {
        "children": ["ServiceTransaction"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "ServiceTransaction": {
        "children": ["InputPrimitive", "OutputPrimitive"],
        "attributes": {}
    },
    "InputPrimitive": {
        "children": [],
        "attributes": {
            "Interface": True,
            "Event": True,
            "Parameters": False
        }
    },
    "OutputPrimitive": {
        "children": [],
        "attributes": {
            "Interface": True,
            "Event": True,
            "Parameters": False
        }
    },
    "AdapterType": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "InterfaceList", "Service"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "ResourceType": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "FBTypeName", "VarDeclaration", "FBNetwork"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "FBTypeName": {
        "children": [],
        "attributes": {
            "Name": True
        }
    },
    "DeviceType": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "VarDeclaration", "ResourceTypeName", "Resource", "FBNetwork"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "ResourceTypeName": {
        "children": [],
        "attributes": {
            "Name": True
        }
    },
    "Resource": {
        "children": ["Parameter", "FBNetwork"],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "System": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "Application", "Device", "Mapping", "Segment", "Link"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "Application": {
        "children": ["SubAppNetwork"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "Mapping": {
        "children": [],
        "attributes": {
            "From": True,
            "To": True
        }
    },
    "Device": {
        "children": ["Parameter", "Resource", "FBNetwork"],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "SubAppType": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "SubAppInterfaceList", "SubAppNetwork"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "SubAppInterfaceList": {
        "children": ["SubAppEventInputs", "SubAppEventOutputs", "InputVars", "OutputVars"],
        "attributes": {}
    },
    "SubAppEventInputs": {
        "children": ["SubAppEvent"],
        "attributes": {}
    },
    "SubAppEventOutputs": {
        "children": ["SubAppEvent"],
        "attributes": {}
    },
    "SubAppEvent": {
        "children": [],
        "attributes": {
            "Name": True,
            "Type": False,
            "Comment": False
        }
    },
    "SubAppNetwork": {
        "children": ["SubApp", "FB", "EventConnections", "DataConnections", "AdapterConnections"],
        "attributes": {}
    },
    "SubApp": {
        "children": [],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False,
            "x": False,
            "y": False
        }
    },
    "Segment": {
        "children": ["Parameter"],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False,
            "x": False,
            "y": False,
            "dx1": False
        }
    },
    "Link": {
        "children": ["Parameter"],
        "attributes": {
            "CommResource": True,
            "SegmentName": True,
            "Comment": False
        }
    },
    "DataType": {
        "children": ["Identification", "VersionInfo", "CompilerInfo", "ASN1Tag", "DirectlyDerivedType", "EnumeratedType", "SubrangeType", "ArrayType", "StructuredType"],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "ASN1Tag": {
        "children": [],
        "attributes": {
            "Class": False,
            "Number": True
        }
    },
    "DirectlyDerivedType": {
        "children": [],
        "attributes": {
            "BaseType": True,
            "InitialValue": False,
            "Comment": False
        }
    },
    "EnumeratedType": {
        "children": ["EnumeratedValue"],
        "attributes": {
            "InitialValue": False,
            "Comment": False
        }
    },
    "EnumeratedValue": {
        "children": [],
        "attributes": {
            "Name": True,
            "Comment": False
        }
    },
    "SubrangeType": {
        "children": ["Subrange"],
        "attributes": {
            "BaseType": True,
            "InitialValue": False,
            "Comment": False
        }
    },
    "Subrange": {
        "children": [],
        "attributes": {
            "LowerLimit": True,
            "UpperLimit": True
        }
    },
    "ArrayType": {
        "children": ["Subrange"],
        "attributes": {
            "BaseType": True,
            "InitialValues": False,
            "Comment": False
        }
    },
    "StructuredType": {
        "children": ["VarDeclaration", "SubrangeVarDeclaration"],
        "attributes": {
            "Comment": False
        }
    },
    "SubrangeVarDeclaration": {
        "children": ["Subrange"],
        "attributes": {
            "Name": True,
            "Type": True,
            "Comment": False
        }
    },
    "FBD": {
        "children": ["FB", "DataConnections"],
        "attributes": {}
    },
    "LD": {
        "children": ["Rung"],
        "attributes": {}
    },
    "Rung": {
        "children": [],
        "attributes": {
            "Output": True,
            "Expression": True,
            "Comment": False
        }
    }
}

class XSDGenerator:
    def __init__(self):
        self.elements = {}  # tag -> set of child tags
        self.seen_attrs_per_tag = {}  # tag -> dict of (attr_name -> count of occurrences)
        self.tag_counts = {}  # tag -> total occurrences

    def analyze_file(self, filepath):
            parser = etree.XMLParser(resolve_entities=False, no_network=True)
            tree = etree.parse(filepath, parser=parser)
            root = tree.getroot()
            self._analyze_element(root)
        except Exception as e:
            print(f"Skipping {filepath} during schema generation due to parse error: {e}", file=sys.stderr)

    def _analyze_element(self, element):
        tag = element.tag
        self.tag_counts[tag] = self.tag_counts.get(tag, 0) + 1

        if tag not in self.elements:
            self.elements[tag] = {
                'sequences': [],
                'unique_children': set()
            }
        
        child_seq = [child.tag for child in element]
        self.elements[tag]['sequences'].append(child_seq)
        for c_tag in child_seq:
            self.elements[tag]['unique_children'].add(c_tag)

        if tag not in self.seen_attrs_per_tag:
            self.seen_attrs_per_tag[tag] = {}
        
        for attr in element.attrib:
            self.seen_attrs_per_tag[tag][attr] = self.seen_attrs_per_tag[tag].get(attr, 0) + 1

        for child in element:
            self._analyze_element(child)

    def _topological_sort(self, nodes, sequences):
        edges = set()
        for seq in sequences:
            for i in range(len(seq)):
                for j in range(i + 1, len(seq)):
                    if seq[i] in nodes and seq[j] in nodes:
                        if seq[i] != seq[j]:
                            edges.add((seq[i], seq[j]))
                            
        adj = {n: [] for n in nodes}
        for u, v in sorted(edges):
            adj[u].append(v)

        for n in adj:
            adj[n] = sorted(adj[n])

        visited = {}
        order = []

        def dfs(node):
            visited[node] = 1 # visiting
            for neighbor in adj[node]:
                if visited.get(neighbor, 0) == 1:
                    return False # Cycle detected
                elif visited.get(neighbor, 0) == 0:
                    if not dfs(neighbor):
                        return False
            visited[node] = 2 # visited
            order.append(node)
            return True

        for n in sorted(nodes):
            if visited.get(n, 0) == 0:
                if not dfs(n):
                    return None # Cycle detected

        return order[::-1]

    def generate_xsd(self):
        xsd_lines = []
        xsd_lines.append('<?xml version="1.0" encoding="UTF-8"?>')
        xsd_lines.append('<xs:schema xmlns:xs="http://www.w3.org/2001/XMLSchema">')
        xsd_lines.append('')

        # Custom simpleType Name
        xsd_lines.append('  <!-- Custom Types -->')
        xsd_lines.append('  <xs:simpleType name="Name">')
        xsd_lines.append('    <xs:restriction base="xs:string">')
        xsd_lines.append('      <xs:pattern value="[a-zA-Z_][a-zA-Z0-9_:\\-\\.]*"/>')
        xsd_lines.append('    </xs:restriction>')
        xsd_lines.append('  </xs:simpleType>')
        xsd_lines.append('')

        all_tags = set(self.elements.keys()).union(set(STANDARD_ELEMENTS.keys()))

        # 1. Global elements declarations for all tags
        xsd_lines.append('  <!-- Global Elements -->')
        for tag in sorted(list(all_tags)):
            xsd_lines.append(f'  <xs:element name="{tag}" type="{tag}" />')
        xsd_lines.append('')

        # 2. Global complexTypes definitions for all tags
        xsd_lines.append('  <!-- Global Complex Types -->')
        for tag in sorted(list(all_tags)):
            scanned_info = self.elements.get(tag)
            scanned_children = scanned_info['unique_children'] if scanned_info else set()
            std_info = STANDARD_ELEMENTS.get(tag, {})
            std_children = set(std_info.get("children", []))
            all_child_tags = scanned_children.union(std_children)

            attrs = self.seen_attrs_per_tag.get(tag, {})
            std_attrs = std_info.get("attributes", {})
            total_tag_count = self.tag_counts.get(tag, 1)

            xsd_lines.append(f'  <xs:complexType name="{tag}" mixed="true">')

            if all_child_tags:
                all_sequences = list(scanned_info['sequences']) if scanned_info else []
                std_order = std_info.get("children", [])
                if std_order:
                    all_sequences.append(std_order)
                
                ordered_children = self._topological_sort(all_child_tags, all_sequences)
                
                if ordered_children is not None:
                    # Stable order: use xs:sequence
                    xsd_lines.append('    <xs:sequence>')
                    for child in ordered_children:
                        # Compute minOccurs and maxOccurs
                        sequences = all_sequences
                        counts = [seq.count(child) for seq in sequences] if sequences else [0]
                        min_occ = min(counts)
                        max_occ = max(counts)

                        if max_occ == 0:
                            min_occ = 0
                            max_occ_str = "1"
                        else:
                            max_occ_str = "unbounded" if max_occ > 1 else str(max_occ)

                        xsd_lines.append(f'      <xs:element name="{child}" type="{child}" minOccurs="{min_occ}" maxOccurs="{max_occ_str}" />')
                    xsd_lines.append('    </xs:sequence>')
                else:
                    # Unstable order: fallback to choice
                    xsd_lines.append('    <xs:choice minOccurs="0" maxOccurs="unbounded">')
                    for child in sorted(list(all_child_tags)):
                        xsd_lines.append(f'      <xs:element name="{child}" type="{child}" />')
                    xsd_lines.append('    </xs:choice>')

            all_attr_names = set(attrs.keys()).union(set(std_attrs.keys()))
            for attr in sorted(list(all_attr_names)):
                attr_type = "Name" if attr == "Name" else "xs:string"
                if attr in std_attrs:
                    if std_attrs[attr]:
                        # Required by standard. But only demote to optional if scanned and missing in some instances
                        scanned_tag_count = self.tag_counts.get(tag, 0)
                        if scanned_tag_count > 0:
                            count = attrs.get(attr, 0)
                            use_status = "required" if count == scanned_tag_count else "optional"
                        else:
                            use_status = "required"
                    else:
                        use_status = "optional"
                else:
                    count = attrs.get(attr, 0)
                    use_status = "required" if count == total_tag_count else "optional"
                xsd_lines.append(f'    <xs:attribute name="{attr}" type="{attr_type}" use="{use_status}" />')

            xsd_lines.append('  </xs:complexType>')
            xsd_lines.append('')

        xsd_lines.append('</xs:schema>')
        return '\n'.join(xsd_lines)


def validate_xml(xml_path, schema_path):
    if not os.path.exists(xml_path):
        print(f"ERROR: XML file not found at {xml_path}", file=sys.stderr)
        return False
    if not os.path.exists(schema_path):
        print(f"ERROR: Schema file not found at {schema_path}", file=sys.stderr)
        return False

    try:
        if schema_path.endswith('.dtd'):
            parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=True)
            xml_doc = etree.parse(xml_path, parser=parser)
            schema = etree.DTD(file=schema_path)
            if not schema.validate(xml_doc):
                errors = "\n".join([str(err) for err in schema.error_log.filter_from_errors()])
                raise ValueError(f"DTD validation failed:\n{errors}")
        else:
            parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
            xml_doc = etree.parse(xml_path, parser=parser)
            schema = etree.XMLSchema(etree.parse(schema_path, parser=parser))
            schema.assertValid(xml_doc)
            
        print(f"SUCCESS: {xml_path} is compliant with {schema_path}!")
        return True
    except Exception as e:
        print(f"VALIDATION FAILED for {xml_path}:\n{e}", file=sys.stderr)
        return False


def run_bulk_validation():
    # Resolve target folders relative to the repo root
    # Since validate.py is at: repo_root/.agents/skills/xml-validator/validate.py
    # repo_root is 3 levels up
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    
    # We can accept folder path arguments and options via command line.
    target_dirs = []
    allow_empty = False
    for arg in sys.argv[1:]:
        if arg in ("--bulk", "-b"):
            continue
        elif arg == "--allow-empty":
            allow_empty = True
        elif os.path.isdir(arg):
            target_dirs.append(os.path.abspath(arg))
        else:
            rel_path = os.path.join(repo_root, arg)
            if os.path.isdir(rel_path):
                target_dirs.append(rel_path)
                    
    if not target_dirs:
        # Default: fallback to scanning the entire repository root
        target_dirs = [repo_root]
    
    # Extensions of IEC 61499 block types / XML documents to validate
    extensions = ('.fbt', '.adp', '.dev', '.res', '.sub', '.SUB', '.sys')
    
    print(f"Starting bulk validation of {len(target_dirs)} folders...")
    for d in target_dirs:
        print(f"- {d}")
        
    xml_files = []
    for d in target_dirs:
        if not os.path.exists(d):
            print(f"WARNING: Directory does not exist: {d}", file=sys.stderr)
            continue
        for root, dirs, files in os.walk(d):
            # Prune version control, agents, metadata and scripts, but preserve user/library hidden folders like .lib
            dirs[:] = [name for name in dirs if name not in ('.git', '.agents', '.metadata', '.vscode', 'scripts')]
            for file in files:
                if file.endswith(extensions):
                    xml_files.append(os.path.join(root, file))
                    
    print(f"Found {len(xml_files)} XML files to validate.")
    if not xml_files:
        print("No files found to validate.", file=sys.stderr)
        if allow_empty:
            sys.exit(0)
        else:
            sys.exit(1)

    # Generate the clean-room XSD
    print("Generating Clean-Room XSD...")
    generator = XSDGenerator()
    for f in xml_files:
        generator.analyze_file(f)
        
    xsd_content = generator.generate_xsd()
    xsd_path = os.path.join(script_dir, "fbt_clean.xsd")
    
    try:
        with open(xsd_path, "w", encoding="utf-8") as xsd_file:
            xsd_file.write(xsd_content)
        print(f"Generated clean XSD at: {xsd_path}")
    except Exception as e:
        print(f"ERROR: Could not write XSD schema: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Load generated XSD
    parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
    try:
        schema = etree.XMLSchema(etree.parse(xsd_path, parser=parser))
    except Exception as e:
        print(f"ERROR: Failed to load generated XSD: {e}", file=sys.stderr)
        sys.exit(1)
        
    # Validate each file
    failures = []
    success_count = 0
    
    for f in xml_files:
        try:
            parser = etree.XMLParser(resolve_entities=False, no_network=True, load_dtd=False)
            xml_doc = etree.parse(f, parser=parser)
            if schema.validate(xml_doc):
            if schema.validate(xml_doc):
                success_count += 1
            else:
                errs = str(schema.error_log.filter_from_errors())
                failures.append((f, f"XSD Validation Error: {errs}"))
            failures.append((f, f"XML Parsing Error: {e}"))
            
    print("\n--- VALIDATION RESULTS ---")
    print(f"Total files validated: {len(xml_files)}")
    print(f"Successes:            {success_count}")
    print(f"Failures:             {len(failures)}")
    
    if failures:
        print("\nFailed files detail (showing up to 50):", file=sys.stderr)
        for i, (path, err) in enumerate(failures[:50], 1):
            print(f"{i}. {path}\n   Reason: {err}\n", file=sys.stderr)
        sys.exit(1)
    else:
        print("\nAll files successfully validated!")
        sys.exit(0)


if __name__ == "__main__":
    is_bulk = False
    if len(sys.argv) == 1:
        is_bulk = True
    elif sys.argv[1] in ("--bulk", "-b", "--allow-empty"):
        is_bulk = True
    elif len(sys.argv) > 3:
        is_bulk = True
    elif len(sys.argv) == 3 and os.path.isdir(sys.argv[1]) and os.path.isdir(sys.argv[2]):
        is_bulk = True
    elif len(sys.argv) == 2:
        if os.path.isdir(sys.argv[1]) or sys.argv[1] == "--allow-empty":
            is_bulk = True
            
    if is_bulk:
        run_bulk_validation()
    elif len(sys.argv) == 3:
        success = validate_xml(sys.argv[1], sys.argv[2])
        sys.exit(0 if success else 1)
    else:
        print("Usage:")
        print("  Bulk validation:  python validate.py [--bulk] [--allow-empty] [target_dirs...]")
        print("  Single validation: python validate.py <path_to_xml> <path_to_schema>")
        sys.exit(1)
