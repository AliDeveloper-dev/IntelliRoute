import os

folders = [
    "core",
    "agents",
    "simulator",
    "visualization",
    "data",
    "tests"
]

files = {
    "core/__init__.py": "",
    "core/graph.py": "",
    "core/router.py": "",
    "agents/__init__.py": "",
    "agents/vehicle.py": "",
    "simulator/__init__.py": "",
    "simulator/simulation.py": "",
    "visualization/__init__.py": "",
    "visualization/map_visualizer.py": "",
    "tests/test_router.py": "",
    "main.py": "",
    "README.md": "# IntelliRoute Project\n",
    ".gitignore": ".venv/\n__pycache__/\n*.pyc\n",
}

for folder in folders:
    os.makedirs(folder, exist_ok=True)

for filepath, content in files.items():
    with open(filepath, "w", encoding="utf8") as f:
        f.write(content)

print("Project structure created successfully!")
