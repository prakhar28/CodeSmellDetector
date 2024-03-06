# Code Smell Detector and Refactoring Tool

## Overview

This tool provides a graphical user interface (GUI) for detecting and refactoring code smells in Python files. The application uses Python's `ast` module to parse the abstract syntax tree of the code for analysis.

## Features

1. **Code Smell Detection:**
   - **Long Method/Function:** Detects functions/methods with a line count exceeding a specified threshold.
   - **Long Parameter List:** Highlights functions with parameter lists containing more than a specified number of parameters.
   - **Exact Duplicated Code:** Finds functions with exact duplicated code.
   - **Semantic Duplicated Code:** (Placeholder) Planned feature for detecting semantic code duplicates.

2. **Refactoring:**
   - The tool provides an option to refactor exact duplicated code.

## How It Works

### Code Smell Detection

1. **Select File:**
   - Users can select a Python file for analysis using the "Browse" button in the GUI.

2. **Detect Code Smells:**
   - Clicking the "Detect Code Smells" button initiates the code smell analysis process.
   - The application analyzes the selected Python file for the specified code smells.

3. **Display Results:**
   - The results of the code smell analysis are displayed in the GUI.
   - If code smells are detected, the names of functions with those code smells are printed.

### Refactoring

1. **Refactor Duplicated Code:**
   - After detecting exact duplicated code, users can click the "Refactor Duplicated Code" button.
   - The tool prompts the user for confirmation before proceeding with the refactoring.

2. **Refactoring Process:**
   - The tool identifies and removes exact duplicated functions from the code.
   - It creates a refactored version of the file with the duplicated functions removed.

3. **Refactoring Complete:**
   - A message is displayed indicating the completion of the refactoring process.
   - The user is informed about the location of the newly created refactored file.

## Usage

1. **Run the Application:**
   - Execute the script, and the GUI will appear.
   - Select a Python file for analysis.

2. **Detect Code Smells:**
   - Click the "Detect Code Smells" button.
   - View the results of the code smell analysis in the text area.

3. **Refactor Duplicated Code:**
   - If exact duplicated code is detected, click the "Refactor Duplicated Code" button.
   - Confirm the refactoring when prompted.

4. **Review Results:**
   - Examine the updated code and the refactored file as needed.

## Requirements

- Python 3.x
- Tkinter (usually included with Python installations)

## Dependencies

No additional dependencies are required beyond the standard Python libraries.
