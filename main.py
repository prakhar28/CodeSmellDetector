import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import ast

LONG_FUNCTION_THRESHOLD = 16
LONG_PARAMETER_THRESHOLD = 3
DUPLICATE_CODE_THRESHOLD = 0.75


class CodeSmellDetectorRefactor:
    def __init__(self, master):
        self.master = master
        master.title("Code Smell Detector and Refactoring")

        self.label = tk.Label(master, text="Select a file:")
        self.label.pack()

        self.browse_button = tk.Button(master, text="Browse", command=self.browse_file)
        self.browse_button.pack()

        self.detect_button = tk.Button(master, text="Detect Code Smells", command=self.detect_code_smells)
        self.detect_button.pack()

        self.refactor_button = tk.Button(master, text="Refactor Duplicated Code", command=self.refactor_code)
        self.refactor_button.pack()

        self.text_output = tk.Text(master, height=20, width=80)
        self.text_output.pack()

    def browse_file(self):
        try:
            file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
            self.file_path = file_path
            self.label.config(text=f"Selected file: {file_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to browse file: {e}")

    def detect_code_smells(self):
        if hasattr(self, 'file_path'):
            self.text_output.delete(1.0, tk.END)
            threading.Thread(target=self.perform_code_smell_analysis).start()
        else:
            messagebox.showinfo("Info", "Please select a file first.")

    def perform_code_smell_analysis(self):
        try:
            params, long_function = analyze_file(self.file_path)
            exact_duplicates, semantic_duplicates = detect_duplicates(self.file_path)

            code_smells = []

            if long_function:
                code_smells.append(("Code Smell: Long Method/Function", long_function))
            if params:
                code_smells.append(("Code Smell: Long Parameter List", params))
            if exact_duplicates:
                code_smells.append(("Code Smell: Exact Duplicate Code Detected", None))
            if semantic_duplicates:
                code_smells.append(("Code Smell: Semantic Duplicated Code", None))

            if not code_smells:
                code_smells.append(("No code smells detected.", None))

            self.master.after(0, self.update_code_smell_results, code_smells)
        except Exception as e:
            self.master.after(0, self.update_code_smell_results, [f"Failed to analyze code smells: {e}"])

    def update_code_smell_results(self, code_smells):
        for smell, function_names in code_smells:
            self.text_output.insert(tk.END, f"{smell}\n")
            if function_names:
                for func_name in function_names:
                    self.text_output.insert(tk.END, f"\tFunction with Code Smell: {func_name}\n")

    def refactor_code(self):
        if not hasattr(self, 'file_path'):
            messagebox.showinfo("Error", "Please select a file first.")
            return

        try:
            confirmation = messagebox.askyesno("Refactor Code", "Do you want to refactor the code?")
            if not confirmation:
                messagebox.showinfo("", "Refactoring Cancelled")
                return

            content, tree = read_and_parse(self.file_path)
            functions = extract_functions(tree)

            exact_duplicates = find_exact_duplicates(functions)
            if exact_duplicates:
                duplicate_names = [dup[1] for dup in exact_duplicates]
                content = remove_duplicate_functions(content, duplicate_names, exact_duplicates)
                refactored_file_path = write_refactored_file(self.file_path, content)
                messagebox.showinfo("Refactoring Complete", f"Refactored file created: {refactored_file_path}")
            else:
                messagebox.showinfo("No Refactoring", "No Duplicates found")

        except Exception as e:
            messagebox.showerror("Error", f"Failed to refactor code: {e}")


def analyze_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    tree = ast.parse(content)
    long_function = []
    long_parameter_functions = []

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_lines = len(ast.unparse(node).splitlines())
            if len(node.args.args) > LONG_PARAMETER_THRESHOLD:
                long_parameter_functions.append(node.name)
            if function_lines > LONG_FUNCTION_THRESHOLD:  # Adjust the threshold as needed
                long_function.append(node.name)

    return long_parameter_functions, long_function


def jaccard_similarity(set1, set2):
    intersection = len(set1.intersection(set2))
    union = len(set1.union(set2))
    if union != 0:
        return intersection / union
    return 0


def detect_duplicates(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
        tree = ast.parse(content)
        functions = extract_functions(tree)
        exact_duplicates = find_exact_duplicates(functions)
        semantic_duplicates = find_semantic_duplicates(functions)
        return exact_duplicates, semantic_duplicates


def find_exact_duplicates(functions):
    duplicates = []
    function_names = list(functions.keys())
    for i in range(len(function_names)):
        for j in range(i + 1, len(function_names)):
            function1 = functions[function_names[i]]
            function2 = functions[function_names[j]]
            similarity = jaccard_similarity(set(function1.split()), set(function2.split()))
            if similarity >= DUPLICATE_CODE_THRESHOLD:
                duplicates.append((function_names[i], function_names[j], similarity))

    return duplicates


# Semantic code still needs to fix this
def find_semantic_duplicates(functions):
    # code here
    return


def read_and_parse(file_path):
    with open(file_path, 'r') as file:
        content = file.read()
    tree = ast.parse(content)
    return content, tree


def extract_functions(tree):
    functions = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_code = ast.unparse(node)
            filtered_code = ' '.join(line.strip() for line in function_code.splitlines() if line.strip())
            functions[node.name] = filtered_code
    return functions


def remove_duplicate_functions(content, duplicate_names, exact_duplicates):
    for name in duplicate_names:
        start = content.find(f"def {name}")
        if start != -1:
            end = content.find('\n\n', start)
            end = len(content) if end == -1 else end
            code = content[start:end]
            content = content.replace(code, '', 1)

    for name in duplicate_names:
        content = content.replace(name + '(', exact_duplicates[0][0] + '(', 1)
    return content


def write_refactored_file(original_file_path, content):
    refactored_file_path = original_file_path.replace('.py', '_refactored.py')
    with open(refactored_file_path, 'w') as refactored_file:
        refactored_file.write(content)
    return refactored_file_path


def main():
    root = tk.Tk()
    CodeSmellDetectorRefactor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
