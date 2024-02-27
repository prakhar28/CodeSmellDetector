import threading
import tkinter as tk
from tkinter import filedialog, messagebox
import ast
from collections import defaultdict

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

        self.refactor_button = tk.Button(master, text="Refactor Duplicated Code", command=refactor_code)
        self.refactor_button.pack()

        self.text_output = tk.Text(master, height=20, width=80)
        self.text_output.pack()

    def browse_file(self):
        file_path = filedialog.askopenfilename(filetypes=[("Python files", "*.py")])
        self.file_path = file_path
        self.label.config(text=f"Selected file: {file_path}")

    def detect_code_smells(self):
        if hasattr(self, 'file_path'):
            # Clear the text output before starting analysis
            self.text_output.delete(1.0, tk.END)

            # Start the analysis in a separate thread
            threading.Thread(target=self.perform_code_smell_analysis).start()

    def perform_code_smell_analysis(self):
        # Code analysis logic goes here
        lines, params, long_function_names = analyze_file(self.file_path)
        exact_duplicates = detect_duplicates(self.file_path)

        code_smells = []

        if lines > LONG_FUNCTION_THRESHOLD:
            code_smells.append("Code Smell: Long Method/Function")
        if long_function_names:
            code_smells.append("Code Smell: Long Function Name")
        if params:
            code_smells.append("Code Smell: Long Parameter List")
        if exact_duplicates:
            code_smells.append("Code Smell: Exact Duplicated Code")
        # if semantic_duplicates:
        #     code_smells.append("Code Smell: Semantic Duplicated Code")

        if not code_smells:
            code_smells.append("No code smells detected.")

        # Update the GUI from the main thread
        self.master.after(0, self.update_code_smell_results, code_smells)

    def update_code_smell_results(self, code_smells):
        # Update the text output in the main GUI thread
        for smell in code_smells:
            self.text_output.insert(tk.END, smell + "\n")


def analyze_file(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    tree = ast.parse(content)
    max_function_lines = 0
    long_function_names = []
    params = False

    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            function_lines = len(ast.unparse(node).splitlines())
            max_function_lines = max(max_function_lines, function_lines)
            if len(node.args.args) > LONG_PARAMETER_THRESHOLD:
                params = True
            if len(node.name) > LONG_FUNCTION_THRESHOLD:  # Adjust the threshold as needed
                long_function_names.append(node.name)

    return max_function_lines, params, long_function_names


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
        functions = {}  # Dictionary to store function names and their filtered code
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                function_code = ast.unparse(node)
                # Filter and clean the function code
                filtered_code = ' '.join(line.strip() for line in function_code.splitlines() if line.strip())
                functions[node.name] = filtered_code

        exact_duplicates = find_exact_duplicates(functions)
        # semantic_duplicates = find_semantic_duplicates(functions)
        return exact_duplicates


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
# def find_semantic_duplicates(functions):
#     duplicates = []
#     function_names = list(functions.keys())
#     for i in range(len(function_names)):
#         for j in range(i + 1, len(function_names)):
#             function1_code = functions[function_names[i]]
#             function2_code = functions[function_names[j]]
#             similarity = jaccard_similarity(set(function1_code.split()), set(function2_code.split()))
#             if similarity >= DUPLICATE_CODE_THRESHOLD:
#                 duplicates.append((function_names[i], function_names[j], similarity))
#
#     return duplicates


def refactor_code():
    # Still needs to implement
    print("Needs to implement")
    return True


def main():
    root = tk.Tk()
    CodeSmellDetectorRefactor(root)
    root.mainloop()


if __name__ == "__main__":
    main()
