import re

# --- Configuration: Update paths here ---
# Using raw strings (r"...") to handle Windows backslashes correctly
path_doc = r"E:\loicuaducphat\js\New folder\parritta.txt"
path_i2h = r"E:\loicuaducphat\js\New folder\dpd_i2h.js"
path_out = r"E:\loicuaducphat\js\New folder\matched.js"

def main():
    print("--- Starting Processing ---")

    # 1. Read Document words
    # ----------------------
    doc_words = set()
    try:
        with open(path_doc, 'r', encoding='utf-8') as f:
            content = f.read().lower()
            # Replace common punctuation with spaces to isolate words
            # Keeping Pali characters intact, removing: . , ? ! " ' “ ” ( ) ; : [ ]
            punctuation = r'[.,?!"\'“”;:()\[\]]' 
            clean_content = re.sub(punctuation, ' ', content)
            doc_words.update(clean_content.split())
            
        print(f"Found {len(doc_words)} unique words in document.")

    except FileNotFoundError:
        print(f"Error: Could not find file {path_doc}")
        return

    # 2. Scan dpd_i2h.js for multi-line matches
    # -----------------------------------------
    matched_blocks = []
    
    try:
        with open(path_i2h, 'r', encoding='utf-8') as f:
            capturing = False
            current_block = []
            
            for line in f:
                # A. Check for START of a block:  "word": [
                start_match = re.search(r'^\s*"(.+?)"\s*:\s*\[', line)
                
                if start_match:
                    key = start_match.group(1)
                    if key in doc_words:
                        capturing = True
                        current_block.append(line.rstrip())
                    continue # Move to next line

                # B. If we are currently inside a matched block
                if capturing:
                    current_block.append(line.rstrip())
                    
                    # C. Check for END of a block:  ],  or  ]
                    # Regex looks for closing bracket at start of line (ignoring whitespace)
                    if re.search(r'^\s*\](?:,)?', line):
                        # Join the list of lines into one string
                        full_block_str = "\n".join(current_block)
                        
                        # Ensure the block ends with a comma for the next item in the list
                        # unless it already has one.
                        if not full_block_str.strip().endswith(','):
                             full_block_str += ','
                             
                        matched_blocks.append(full_block_str)
                        
                        # Reset for next search
                        capturing = False
                        current_block = []

    except FileNotFoundError:
        print(f"Error: Could not find file {path_i2h}")
        return

    # 3. Write to matched.js
    # ----------------------
    try:
        with open(path_out, 'w', encoding='utf-8') as f:
            f.write('let matched_i2h = {\n')
            
            # Write all matched blocks
            for block in matched_blocks:
                f.write(block + '\n')
            
            f.write('};\n')
            
        print(f"Success! {len(matched_blocks)} matches written to: {path_out}")

    except Exception as e:
        print(f"Error writing output: {e}")

if __name__ == "__main__":
    main()