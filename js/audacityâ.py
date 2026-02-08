# Notepad++ PythonScript (Python 2.7)
# Fill each [] in the current document with values from a separate list file.

def main():
    # 1. Load the values from another file (each line = one number)
    # Change the path below to where your values file is saved
    values_file = r"E:\Test\output.txt"
    values = []
    try:
        with open(values_file, "r") as f:
            for line in f:
                line = line.strip()
                if line:
                    values.append(line)
    except Exception as e:
        notepad.messageBox("Could not read values file:\n" + str(e), "Error")
        return

    # 2. Get the text from the current document
    text = editor.getText()
    out = ""
    idx = 0
    i = 0

    # 3. Walk through the text and fill [] with values
    while i < len(text):
        if text[i:i+2] == "[]":
            if idx < len(values):
                out += "[" + values[idx] + "]"
                idx += 1
            else:
                out += "[]"
            i += 2
        else:
            out += text[i]
            i += 1

    # 4. Show result in a new tab
    notepad.new()
    editor.setText(out)

main()
