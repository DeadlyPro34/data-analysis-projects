import nbformat

with open('Football_Analysis.ipynb', 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

code = ""
for cell in nb.cells:
    if cell.cell_type == 'code':
        source = cell.source
        filtered_source = "\n".join([line for line in source.split('\n') if not line.startswith('%')])
        code += filtered_source + "\n\n"

with open('run_analysis.py', 'w', encoding='utf-8') as f:
    f.write(code)
print("Code extracted to run_analysis.py")
