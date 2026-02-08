import re
import os

# --- Configuration ---
base_path = r"E:\loicuaducphat\js\New folder"
ebts_path = os.path.join(base_path, "dpd_ebts.js")
i2h_path = os.path.join(base_path, "dpd_i2h.js")
output_path = os.path.join(base_path, "matched.js")

def extract_ebts_definitions(file_path):
    definitions = {}
    print(f"Reading dictionary: {os.path.basename(file_path)}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Matches "headword": ... at the start of lines in ebts
                match = re.search(r'^\s*["\']([^"\']+)["\']\s*:', line)
                if match:
                    key = match.group(1).strip()
                    definitions[key] = line.strip().rstrip(',')
    except Exception as e:
        print(f"Error reading EBTS: {e}")
    return definitions

def extract_i2h_references(file_path):
    references = set()
    print(f"Reading index: {os.path.basename(file_path)}")
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # 1. Find everything between [ and ]
            # The regex \[([^\]]+)\] looks for brackets and captures everything inside
            blocks = re.findall(r'\[([^\]]+)\]', content)
            
            for block in blocks:
                # 2. Inside each block, find all quoted strings
                # This captures "ṭhāna 01", "ṭhāna 02", etc.
                words = re.findall(r'["\']([^"\']+)["\']', block)
                for w in words:
                    references.add(w.strip())
                    
    except Exception as e:
        print(f"Error reading I2H: {e}")
        
    print(f"-> Found {len(references)} unique headwords inside brackets.")
    return references

def write_matched_file(definitions, references, out_path):
    valid_keys = sorted([k for k in references if k in definitions])
    matched_count = len(valid_keys)
    
    print(f"-> Matching: {matched_count} of the requested words exist in the dictionary.")

    with open(out_path, 'w', encoding='utf-8') as f:
        f.write('let matched_entries = {\n')
        for i, key in enumerate(valid_keys):
            line = definitions[key]
            suffix = "," if i < matched_count - 1 else ""
            f.write(f"  {line}{suffix}\n")
        f.write('};\n')
    print(f"Done! Created {out_path}")

if __name__ == "__main__":
    dict_data = extract_ebts_definitions(ebts_path)
    if dict_data:
        ref_keys = extract_i2h_references(i2h_path)
        write_matched_file(dict_data, ref_keys, output_path)