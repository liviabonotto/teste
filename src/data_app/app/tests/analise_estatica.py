import os
import subprocess

def run_pylint_on_project(project_path):
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                print(f"Running pylint on {file_path}")
                
                result = subprocess.run(['pylint', file_path], capture_output=True, text=True)
                
                print(result.stderr)


project_directory = 'src/data_app'  
run_pylint_on_project(project_directory)
