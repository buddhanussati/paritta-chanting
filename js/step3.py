import re
import os

# --- Configuration: Update these paths if necessary ---
# Using raw strings (r"...") to handle Windows backslashes correctly
dict_path = r"E:\loicuaducphat\js\New folder\dpd_deconstructor.js"
doc_path = r"E:\loicuaducphat\js\New folder\parritta.txt"
output_path = r"E:\loicuaducphat\js\New folder\matched.js"

def main():
    print("--- Starting Processing ---")
    
    # 1. Parse the Dictionary File (dpd_ebts.js)
    # We map the 'key' (word) to the 'full line'
    dictionary_map = {}
    
    try:
        with open(dict_path, 'r', encoding='utf-8') as f:
            for line in f:
                # Regex explanation:
                # ^\s* -> Start of line, allow whitespace
                # "     -> Opening quote
                # (.+?) -> Capture the word (key) inside
                # "     -> Closing quote
                # \s*:  -> Followed by colon
                match = re.search(r'^\s*"(.+?)"\s*:', line)
                if match:
                    key = match.group(1)
                    # Store the key and the raw line (stripped of trailing newline)
                    dictionary_map[key] = line.rstrip()
        
        print(f"Loaded {len(dictionary_map)} entries from dictionary.")

    except FileNotFoundError:
        print(f"Error: Could not find file: {dict_path}")
        return

    # 2. Parse the Document File (document.html)
    doc_words = set()
    
    try:
        with open(doc_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            # Normalize: Convert to lowercase to match dictionary keys
            content = content.lower()
            
            # Replace common punctuation with spaces to isolate words
            # This keeps Pali characters (ā, ī, etc.) intact but removes symbols
            # We remove: . , ? ! " ' “ ” ( ) ; :
            punctuation = r'[.,?!"\'“”;:()\[\]]' 
            clean_content = re.sub(punctuation, ' ', content)
            
            # Split by whitespace to get individual words
            words = clean_content.split()
            
            # Add to a set to ensure uniqueness (we don't need to match "the" twice)
            doc_words.update(words)
            
        print(f"Found {len(doc_words)} unique words in document.")

    except FileNotFoundError:
        print(f"Error: Could not find file: {doc_path}")
        return

    # 3. Find Matches and Write to Output
    matched_lines = []
    
    for word in doc_words:
        if word in dictionary_map:
            matched_lines.append(dictionary_map[word])

    # Sort the output (optional, but makes it cleaner)
    matched_lines.sort()

    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            # We add the variable declaration to make it valid JS
            f.write('let matched_ebts = {\n')
            
            for line in matched_lines:
                f.write(line + '\n')
            
            f.write('};\n')
            
        print(f"Success! {len(matched_lines)} matches written to: {output_path}")

    except Exception as e:
        print(f"Error writing output: {e}")

if __name__ == "__main__":
    main()