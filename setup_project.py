# setup_project.py
import os

# Define folder structure and files
structure = {
    "ai-backend": {
        "app": {
            "services": ["parser_pdf.py", "dummy_fill.py"],
            "main.py": "",
            "models.py": ""
        },
        "tests": [],
        "requirements.txt": "",
        "Dockerfile": ""
    }
}

def create_structure(base_path, struct):
    for name, content in struct.items():
        path = os.path.join(base_path, name)
        if isinstance(content, dict):
            os.makedirs(path, exist_ok=True)
            create_structure(path, content)
        elif isinstance(content, list):
            os.makedirs(path, exist_ok=True)
            for f in content:
                open(os.path.join(path, f), 'w').close()
        else:
            open(path, 'w').close()

if __name__ == "__main__":
    create_structure(".", structure)
    print("Project structure created successfully!")
