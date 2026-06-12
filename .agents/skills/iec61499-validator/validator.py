import sys
import os
import re
from lxml import etree

RESERVED_KEYWORDS = {
    # Control flow & structure keywords
    'if', 'then', 'else', 'elsif', 'end_if',
    'case', 'of', 'end_case',
    'for', 'to', 'by', 'do', 'end_for',
    'while', 'end_while',
    'repeat', 'until', 'end_repeat',
    'exit', 'return',
    'var', 'end_var', 'var_input', 'var_output', 'var_in_out', 'var_temp', 'var_external', 'var_global',
    'true', 'false', 'constant',
    'algorithm', 'end_algorithm',
    
    # Operators
    'and', 'or', 'xor', 'not', 'mod',
    
    # Built-in standard functions
    'abs', 'sqrt', 'ln', 'log', 'exp', 'sin', 'cos', 'tan', 'asin', 'acos', 'atan',
    'add', 'mul', 'sub', 'div', 'expt', 'move',
    'limit', 'mux', 'sel', 'max', 'min',
    'adr', 'sizeof',
    
    # String functions
    'left', 'right', 'mid', 'concat', 'insert', 'delete', 'replace', 'find', 'len',
    
    # Standard data types
    'bool', 'sint', 'int', 'dint', 'lint', 'usint', 'uint', 'udint', 'ulint',
    'real', 'lreal', 'time', 'date', 'tod', 'time_of_day', 'dt', 'date_and_time',
    'string', 'wstring', 'byte', 'word', 'dword', 'lword',
    
    # IEC 61499 standard block names or types
    'e_delay', 'e_cycle', 'e_start', 'e_stop', 'e_restart', 'e_split', 'e_join',
    'e_rendezvous', 'e_merge', 'e_f_trig', 'e_r_trig', 'e_sr', 'e_rs', 'e_select',
    'e_switch', 'e_table', 'e_d_ff', 'e_t_ff'
}

DEPRECATED_TYPES = {
    'BOOL2BOOL', 'INT2INT', 'DINT2DINT', 'REAL2REAL', 'BYTE2BYTE',
    'WORD2WORD', 'DWORD2DWORD', 'LWORD2LWORD', 'SINT2SINT',
    'USINT2USINT', 'UINT2UINT', 'UDINT2UDINT', 'ULINT2ULINT',
    'LREAL2LREAL', 'STRING2STRING'
}

# Type Compatibility Matrix from meisterschulen documentation
COMPATIBILITY_MAP = {
    'SINT': {'SINT'},
    'INT': {'SINT', 'INT'},
    'DINT': {'SINT', 'INT', 'DINT'},
    'LINT': {'SINT', 'INT', 'DINT', 'LINT'},
    
    'USINT': {'USINT'},
    'UINT': {'USINT', 'UINT'},
    'UDINT': {'USINT', 'UINT', 'UDINT'},
    'ULINT': {'USINT', 'UINT', 'UDINT', 'ULINT'},
    
    'REAL': {'SINT', 'INT', 'USINT', 'UINT', 'REAL'},
    'LREAL': {'SINT', 'INT', 'DINT', 'USINT', 'UINT', 'UDINT', 'REAL', 'LREAL'},
    
    'BOOL': {'BOOL'},
    'BYTE': {'BOOL', 'BYTE'},
    'WORD': {'BOOL', 'BYTE', 'WORD'},
    'DWORD': {'BOOL', 'BYTE', 'WORD', 'DWORD'},
    'LWORD': {'BOOL', 'BYTE', 'WORD', 'DWORD', 'LWORD'},
    
    'CHAR': {'CHAR'},
    'WCHAR': {'WCHAR'},
    'STRING': {'CHAR', 'STRING'},
    'WSTRING': {'WCHAR', 'WSTRING'},
    
    'TIME': {'TIME'},
    'LTIME': {'TIME', 'LTIME'},
    'DATE': {'DATE'},
    'LDATE': {'DATE', 'LDATE'},
    'TOD': {'TOD'},
    'LTOD': {'TOD', 'LTOD'},
    'DT': {'DT'},
    'LDT': {'DT', 'LDT'}
}

def normalize_type_name(t):
    if not t:
        return ""
    return t.replace("::", ":").split(":")[-1]

def is_assignable_from(target, source):
    if not target or not source:
        return False
    t = target.upper()
    s = source.upper()
    if t == s:
        return True
    if t == 'ANY' or s == 'ANY':
        return True
    if t in COMPATIBILITY_MAP:
        return s in COMPATIBILITY_MAP[t]
    return False

def extract_interface_info(root_elem):
    """
    Extracts input variables, output variables, and event names from an interface element.
    Returns a tuple of (inputs, outputs, events) where:
      - inputs: dict mapping name to type
      - outputs: dict mapping name to type
      - events: set of event names
    """
    inputs = {}
    outputs = {}
    events = set()
    
    for ivar in root_elem.xpath('.//InterfaceList/InputVars/VarDeclaration | .//SubAppInterfaceList/InputVars/VarDeclaration'):
        v_name = ivar.attrib.get('Name')
        v_type = ivar.attrib.get('Type')
        if v_name and v_type:
            inputs[v_name] = v_type
            
    for ovar in root_elem.xpath('.//InterfaceList/OutputVars/VarDeclaration | .//SubAppInterfaceList/OutputVars/VarDeclaration'):
        v_name = ovar.attrib.get('Name')
        v_type = ovar.attrib.get('Type')
        if v_name and v_type:
            outputs[v_name] = v_type

    for iovar in root_elem.xpath('.//InterfaceList/InOutVars/VarDeclaration | .//SubAppInterfaceList/InOutVars/VarDeclaration'):
        v_name = iovar.attrib.get('Name')
        v_type = iovar.attrib.get('Type')
        if v_name and v_type:
            inputs[v_name] = v_type
            outputs[v_name] = v_type
            
    for ev in root_elem.xpath('.//InterfaceList/EventInputs/Event | .//InterfaceList/EventOutputs/Event | .//SubAppInterfaceList/SubAppEventInputs/SubAppEvent | .//SubAppInterfaceList/SubAppEventOutputs/SubAppEvent | .//SubAppInterfaceList/EventInputs/Event | .//SubAppInterfaceList/EventOutputs/Event'):
        ev_name = ev.attrib.get('Name')
        if ev_name:
            events.add(ev_name)
            
    return inputs, outputs, events

def build_interface_db(lib_dirs=None):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    repo_root = os.path.abspath(os.path.join(script_dir, "..", "..", ".."))
    
    if lib_dirs is None:
        lib_dirs = [repo_root]
        
    db = {}
    extensions = ('.fbt', '.adp', '.sub', '.SUB', '.dtp')
    
    for d in lib_dirs:
        if not os.path.exists(d):
            continue
        for root, dirs, files in os.walk(d):
            # Prune version control, agents, metadata and scripts, but preserve user/library hidden folders like .lib
            dirs[:] = [name for name in dirs if name not in ('.git', '.agents', '.metadata', '.vscode', 'scripts')]
            for file in files:
                if file.endswith(extensions):
                    path = os.path.join(root, file)
                    try:
                        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True, load_dtd=False)
                        tree = etree.parse(path, parser)
                        root_elem = tree.getroot()
                        name = root_elem.attrib.get('Name')
                        if not name:
                            continue
                        name = normalize_type_name(name)
                            
                        if file.endswith('.dtp'):
                            members = {}
                            for var in root_elem.xpath('.//StructuredType/VarDeclaration'):
                                v_name = var.attrib.get('Name')
                                v_type = var.attrib.get('Type')
                                if v_name and v_type:
                                    members[v_name] = v_type
                            db[name] = {
                                'type': 'struct',
                                'members': members
                            }
                        else:
                            inputs, outputs, events = extract_interface_info(root_elem)
                            db[name] = {
                                'inputs': inputs,
                                'outputs': outputs,
                                'events': events
                            }
                    except (OSError, etree.XMLSyntaxError) as exc:
                        print(
                            f"WARNING: Skipping interface definition '{path}': {exc}",
                            file=sys.stderr,
                        )
    return db

def infer_expression_type(expr, symbol_table):
    expr = expr.strip()
    
    # 1. Type conversion check: e.g. UDINT_TO_REAL(...)
    conversion_match = re.match(r'\b(?:[a-zA-Z0-9_]+)_TO_([a-zA-Z0-9_]+)\s*\(', expr)
    if conversion_match:
        return conversion_match.group(1)
        
    # Typed literals: e.g. INT#123, UINT#16#FF, REAL#1.2, T#5s
    typed_literal_match = re.match(r'^([a-zA-Z_][a-zA-Z0-9_]*)#', expr)
    if typed_literal_match:
        type_prefix = typed_literal_match.group(1).upper()
        return 'TIME' if type_prefix == 'T' else type_prefix
        
    # 2. Boolean literals
    if expr.lower() in ('true', 'false'):
        return 'BOOL'
        
    # 3. String literals
    if (expr.startswith("'") and expr.endswith("'")) or (expr.startswith(chr(34)) and expr.endswith(chr(34))):
        return 'STRING' if expr.startswith("'") else 'WSTRING'
        
    # 4. Numeric literals
    if re.match(r'^[-+]?\d+\.\d+(?:[eE][+-]?\d+)?$', expr):
        return 'ANY_REAL_LITERAL'
    if re.match(r'^[-+]?\d+$', expr) or re.match(r'^\d+#_?[0-9a-fA-F_]+$', expr):
        return 'ANY_INT_LITERAL'
        
    # 5. Single variable
    if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', expr):
        return symbol_table.get(expr)
        
    return None

def parse_local_st_variables(st_text, symbol_table):
    lines = st_text.splitlines()
    in_var_block = False

    for line in lines:
        line = line.strip()
        if '//' in line:
            line = line.split('//', 1)[0].strip()

        lower_line = line.lower()
        if re.match(r'^(var|var_temp|var_input|var_output|var_in_out)\b', lower_line):
            in_var_block = True
            continue
        if re.match(r'^end_var\b', lower_line):
            in_var_block = False
            continue

        if in_var_block:
            # Support multiple identifiers before the colon, e.g. "x, y, z : INT;"
            match = re.match(
                r'\b([a-zA-Z_][a-zA-Z0-9_]*(?:\s*,\s*[a-zA-Z_][a-zA-Z0-9_]*)*)\s*:\s*([^;:=]+?)\s*(?::=[^;]+)?\s*;',
                line
            )
            if match:
                names_part = match.group(1)
                v_type = match.group(2).strip()
                for raw_name in names_part.split(','):
                    v_name = raw_name.strip()
                    if v_name and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', v_name):
                        symbol_table[v_name] = v_type

def check_st_code(st_text, symbol_table, line_offset=0):
    errors = []
    lines = st_text.splitlines()
    
    # Parse local variables to populate symbol table
    parse_local_st_variables(st_text, symbol_table)
    
    if_stack = []
    case_stack = []
    for_stack = []
    while_stack = []
    repeat_stack = []
    
    clean_lines = []
    in_block_comment = False
    
    for idx, line in enumerate(lines):
        orig_line = line
        if '//' in line:
            line = line.split('//', 1)[0]
        
        while '(*' in line or '*)' in line:
            if not in_block_comment:
                if '(*' in line:
                    before, rest = line.split('(*', 1)
                    if '*)' in rest:
                        after = rest.split('*)', 1)[1]
                        line = before + " " + after
                    else:
                        line = before
                        in_block_comment = True
                else:
                    break
            else:
                if '*)' in line:
                    line = line.split('*)', 1)[1]
                    in_block_comment = False
                else:
                    line = ""
                    break
                    
        clean_lines.append((line.strip(), orig_line, idx + 1))

    in_var_block = False
    for clean_line, orig_line, line_num in clean_lines:
        lower_line = clean_line.lower()
        if not clean_line:
            continue
            
        if re.match(r'^(var|var_temp|var_input|var_output|var_in_out)\b', lower_line):
            in_var_block = True
            continue
        if re.match(r'^end_var\b', lower_line):
            in_var_block = False
            continue
        if in_var_block:
            continue
            
        tokens = re.findall(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', lower_line)
        if not tokens:
            continue

        first_word = tokens[0]

        # 1. Zuweisungs-Validierung (Assignment checking & type compatibility)
        if ':=' in clean_line:
            parts = clean_line.split(':=', 1)
            target_expr = parts[0].strip()
            source_expr = parts[1].strip()
            if source_expr.endswith(';'):
                source_expr = source_expr[:-1].strip()
                
            # Extract target variable
            target_match = re.match(r'\b[a-zA-Z_][a-zA-Z0-9_]*\b', target_expr)
            if target_match:
                target_var = target_match.group(0)
                target_type = symbol_table.get(target_var)
                
                # Check reserved keywords usage
                if target_var.lower() in RESERVED_KEYWORDS:
                    errors.append((line_num + line_offset, f"Assignment target '{target_var}' is a reserved keyword in ST."))
                
                # Verify type compatibility
                if target_type and re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', target_expr):
                    source_type = infer_expression_type(source_expr, symbol_table)
                    if source_type:
                        if source_type == 'ANY_INT_LITERAL':
                            all_int_real_types = {
                                'SINT', 'INT', 'DINT', 'LINT', 'USINT', 'UINT', 'UDINT', 'ULINT',
                                'REAL', 'LREAL', 'BYTE', 'WORD', 'DWORD', 'LWORD'
                            }
                            if target_type.upper() not in all_int_real_types:
                                errors.append((line_num + line_offset, f"Type mismatch: cannot assign integer literal to '{target_var}' of type '{target_type}'."))
                        elif source_type == 'ANY_REAL_LITERAL':
                            if target_type.upper() not in {'REAL', 'LREAL'}:
                                errors.append((line_num + line_offset, f"Type mismatch: cannot assign real literal to '{target_var}' of type '{target_type}'."))
                        else:
                            if not is_assignable_from(target_type, source_type):
                                # Suggest explicit conversion
                                hint = f" Use explicit conversion: {source_type.upper()}_TO_{target_type.upper()}({source_expr})"
                                errors.append((line_num + line_offset, f"Type mismatch in ST assignment: cannot assign type '{source_type}' to '{target_var}' of type '{target_type}'.{hint}"))
        control_keywords_start = {'if', 'elsif', 'else', 'case', 'for', 'while', 'repeat', 'until', 'end_if', 'end_case', 'end_for', 'end_while', 'end_repeat', 'exit', 'return', 'algorithm', 'end_algorithm', 'var', 'var_temp', 'var_input', 'var_output', 'var_in_out', 'end_var', 'then', 'do', 'of'}
        # 2. Check for '=' instead of ':=' for assignment
        if clean_line.endswith(';') and '=' in clean_line and ':=' not in clean_line:
            if re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*(?:\s*\[[^\]]+\])?\s*=\s*[^=].*;$', clean_line):
                errors.append((line_num + line_offset, f"Possible incorrect assignment. Use ':=' instead of '=': '{clean_line}'"))

        # 3. Check semicolons & track structures
        control_keywords_start = {'if', 'elsif', 'else', 'case', 'for', 'while', 'repeat', 'until', 'end_if', 'end_case', 'end_for', 'end_while', 'end_repeat', 'exit', 'return', 'algorithm', 'end_algorithm', 'var', 'var_temp', 'var_input', 'var_output', 'var_in_out', 'end_var'}
        
        if first_word == 'if':
            if_stack.append(line_num)
        elif first_word == 'end_if':
            if if_stack:
                if_stack.pop()
            else:
                errors.append((line_num + line_offset, "Mismatched 'END_IF' (no matching 'IF' found)."))
                
        elif first_word == 'case':
            case_stack.append(line_num)
        elif first_word == 'end_case':
            if case_stack:
                case_stack.pop()
            else:
                errors.append((line_num + line_offset, "Mismatched 'END_CASE' (no matching 'CASE' found)."))
                
        elif first_word == 'for':
            for_stack.append(line_num)
        elif first_word == 'end_for':
            if for_stack:
                for_stack.pop()
            else:
                errors.append((line_num + line_offset, "Mismatched 'END_FOR' (no matching 'FOR' found)."))
                
        elif first_word == 'while':
            while_stack.append(line_num)
        elif first_word == 'end_while':
            if while_stack:
                while_stack.pop()
            else:
                errors.append((line_num + line_offset, "Mismatched 'END_WHILE' (no matching 'WHILE' found)."))
                
        elif first_word == 'repeat':
            repeat_stack.append(line_num)
        is_control = first_word in control_keywords_start
        if is_control:
            if first_word in {'if', 'elsif', 'else', 'while', 'repeat', 'for', 'case', 'until', 'var', 'var_temp', 'var_input', 'var_output', 'var_in_out', 'end_var', 'then', 'do', 'of'}:
                repeat_stack.pop()
            else:
                errors.append((line_num + line_offset, "Mismatched 'END_REPEAT' (no matching 'REPEAT' found)."))

        # Verify semicolon usage
        block_openers = {'if', 'elsif', 'else', 'case', 'for', 'while', 'repeat', 'until'}
        block_closers = {'end_if', 'end_case', 'end_for', 'end_while', 'end_repeat'}

        if first_word in block_openers:
            if clean_line.endswith(';'):
                errors.append((line_num + line_offset, f"Control statement line should not end with a semicolon: '{orig_line.strip()}'"))
        elif first_word in block_closers:
            if not clean_line.endswith(';'):
                errors.append((line_num + line_offset, f"Structure closing statement should end with a semicolon: '{orig_line.strip()}'"))
        else:
            if not clean_line.endswith(';'):
                errors.append((line_num + line_offset, f"Statement missing semicolon ';': '{orig_line.strip()}'"))
                
    for line_num in if_stack:
        errors.append((line_num + line_offset, "Unclosed 'IF' statement (missing 'END_IF;')."))
    for line_num in case_stack:
        errors.append((line_num + line_offset, "Unclosed 'CASE' statement (missing 'END_CASE;')."))
    for line_num in for_stack:
        errors.append((line_num + line_offset, "Unclosed 'FOR' statement (missing 'END_FOR;')."))
    for line_num in while_stack:
        errors.append((line_num + line_offset, "Unclosed 'WHILE' statement (missing 'END_WHILE;')."))
    for line_num in repeat_stack:
        errors.append((line_num + line_offset, "Unclosed 'REPEAT' statement (missing 'END_REPEAT;')."))

    return errors



def resolve_pin_type(fb_name, pin_path, fb_types, interface_db, current_inputs, current_outputs, f_move_data_types):
    if '.' in pin_path:
        pin_name, member_path = pin_path.split('.', 1)
    else:
        pin_name = pin_path
        member_path = None
        
    base_type = None
    
    if fb_name:
        fb_type = fb_types.get(fb_name)
        if not fb_type:
            return None
        base_fb_type = normalize_type_name(fb_type)
        
        if base_fb_type == 'F_MOVE':
            if pin_name in ('IN', 'OUT'):
                base_type = f_move_data_types.get(fb_name)
        elif base_fb_type in interface_db:
            if pin_name in interface_db[base_fb_type]['outputs']:
                base_type = interface_db[base_fb_type]['outputs'].get(pin_name)
            elif pin_name in interface_db[base_fb_type]['inputs']:
                base_type = interface_db[base_fb_type]['inputs'].get(pin_name)
    else:
        if pin_name in current_inputs:
            base_type = current_inputs.get(pin_name)
        elif pin_name in current_outputs:
            base_type = current_outputs.get(pin_name)
            
    if not base_type:
        return None
        
    if member_path:
        struct_name = normalize_type_name(base_type)
        if struct_name in interface_db and 'members' in interface_db[struct_name]:
            curr_struct = struct_name
            for part in member_path.split('.'):
                if curr_struct in interface_db and 'members' in interface_db[curr_struct]:
                    base_type = interface_db[curr_struct]['members'].get(part)
                    if base_type:
                        curr_struct = normalize_type_name(base_type)
                    else:
                        return None
                else:
                    return None
            return base_type
        else:
            return None
            
    return base_type

def validate_iec61499_file(filepath, interface_db):
    errors = []
    try:
        parser = etree.XMLParser(remove_blank_text=True, resolve_entities=False, no_network=True, load_dtd=False)
        tree = etree.parse(filepath, parser)
        root = tree.getroot()
    except Exception as e:
        print(f"ERROR: XML parsing failed for {filepath}: {e}", file=sys.stderr)
        return False

    # Build symbol table for current file's variables
    current_inputs, current_outputs, current_events = extract_interface_info(root)
    symbol_table = {}
    symbol_table.update(current_inputs)
    symbol_table.update(current_outputs)

    # Internal vars
    for ivar in root.xpath('.//InternalVars/VarDeclaration'):
        v_name = ivar.attrib.get('Name')
        v_type = ivar.attrib.get('Type')
        if v_name and v_type:
            symbol_table[v_name] = v_type

    # 1. Check XML Identifiers
    for elem in root.iter():
        name_val = elem.attrib.get('Name')
        if name_val:
            if name_val.lower() in RESERVED_KEYWORDS:
                line = elem.sourceline or 0
                errors.append((line, f"Element '{elem.tag}' has name attribute '{name_val}', which is a reserved keyword."))

    # 2. Check ST Syntax & Assignments
    for elem in root.iter('ST'):
        st_text = elem.text or ""
        line_offset = elem.sourceline or 0
        st_errors = check_st_code(st_text, symbol_table.copy(), line_offset=line_offset)
        for err_line, err_msg in st_errors:
            errors.append((err_line, f"ST Syntax Error: {err_msg}"))

    # 3. Check App/Sub-App Connection Types and FB Configurations
    fb_types = {}
    f_move_data_types = {}
    
    for fb in root.xpath('.//FB'):
        fb_name = fb.attrib.get('Name')
        fb_type = fb.attrib.get('Type', '')
        if fb_name and fb_type:
            fb_types[fb_name] = fb_type
            
        base_type = normalize_type_name(fb_type)
        line = fb.sourceline or 0
        
        # Check if type is deprecated
        if base_type in DEPRECATED_TYPES:
            errors.append((line, f"FB '{fb_name}' has deprecated type '{fb_type}'. Use F_MOVE instead."))
            
        # Check F_MOVE configuration
        if base_type == 'F_MOVE':
            dt_attr = fb.xpath('./Attribute[@Name="DataType"]')
            if not dt_attr:
                errors.append((line, f"F_MOVE block '{fb_name}' is not configured. It must contain an Attribute child with Name='DataType' (e.g., <Attribute Name='DataType' Value='BOOL'/>)."))
            else:
                val = dt_attr[0].attrib.get('Value')
                if not val:
                    errors.append((line, f"F_MOVE block '{fb_name}' has empty DataType attribute Value."))
                else:
                    val = val.strip("'")
                    f_move_data_types[fb_name] = val
                    
    for subapp in root.xpath('.//SubApp'):
        sa_name = subapp.attrib.get('Name')
        sa_type = subapp.attrib.get('Type')
        if sa_name and sa_type:
            fb_types[sa_name] = sa_type

    for conn in root.xpath('.//Connection'):
        source = conn.attrib.get('Source')
        dest = conn.attrib.get('Destination')
        line = conn.sourceline or 0
        
        if not source or not dest:
            continue
            
        is_source_event = False
        if '.' in source:
            src_fb, src_pin_path = source.split('.', 1)
            src_pin = src_pin_path.split('.')[0]
            src_fb_type = fb_types.get(src_fb)
            if src_fb_type:
                base_fb = normalize_type_name(src_fb_type)
                if base_fb in interface_db and src_pin in interface_db[base_fb]['events']:
                    is_source_event = True
        else:
            if source in current_events:
                is_source_event = True
                
        is_dest_event = False
        if '.' in dest:
            dst_fb, dst_pin_path = dest.split('.', 1)
            dst_pin = dst_pin_path.split('.')[0]
            dst_fb_type = fb_types.get(dst_fb)
            if dst_fb_type:
                base_fb = normalize_type_name(dst_fb_type)
                if base_fb in interface_db and dst_pin in interface_db[base_fb]['events']:
                    is_dest_event = True
        else:
            if dest in current_events:
                is_dest_event = True

        if is_source_event or is_dest_event:
            continue
            
        source_type = None
        if '.' in source:
            src_fb, src_pin_path = source.split('.', 1)
            source_type = resolve_pin_type(src_fb, src_pin_path, fb_types, interface_db, current_inputs, current_outputs, f_move_data_types)
        else:
            source_type = resolve_pin_type(None, source, fb_types, interface_db, current_inputs, current_outputs, f_move_data_types)
            
        dest_type = None
        if '.' in dest:
            dst_fb, dst_pin_path = dest.split('.', 1)
            dest_type = resolve_pin_type(dst_fb, dst_pin_path, fb_types, interface_db, current_inputs, current_outputs, f_move_data_types)
        else:
            dest_type = resolve_pin_type(None, dest, fb_types, interface_db, current_inputs, current_outputs, f_move_data_types)

        if source_type and dest_type:
            if not is_assignable_from(dest_type, source_type):
                errors.append((line, f"Type compatibility error: connection from '{source}' ({source_type}) to '{dest}' ({dest_type}) is invalid."))

    # Print results
    if errors:
        print(f"VALIDATION FAILED for {filepath}:", file=sys.stderr)
        for line, msg in sorted(errors, key=lambda x: x[0]):
            print(f"  Line {line}: {msg}", file=sys.stderr)
        return False
    else:
        print(f"SUCCESS: {filepath} passed all IEC 61499 keyword, syntax, and type checks.")
        return True

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Validate IEC 61499 XML files.")
    parser.add_argument("--lib-dir", action="append", help="Specify library directories to scan. Can be specified multiple times.")
    parser.add_argument("filepath", help="The XML file to validate.")
    
    args = parser.parse_args()
    
    filepath = args.filepath
    if not os.path.exists(filepath):
        print(f"ERROR: File not found at {filepath}", file=sys.stderr)
        sys.exit(1)
        
    print("Building block interface database...")
    interface_db = build_interface_db(lib_dirs=args.lib_dir)
    
    success = validate_iec61499_file(filepath, interface_db)
    sys.exit(0 if success else 1)
