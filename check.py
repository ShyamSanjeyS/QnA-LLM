import os

# Allowed file extensions (only manually created types)
allowed_exts = {'.js', '.css', '.html', '.json', '.py', '.env'}

# Folders to ignore (auto-generated or package folders)
ignored_folders = {
    '__pycache__', 'node_modules', '.git', '.idea', 'venv', 'env',
    'dist', 'build', '.next', '.vscode', '.eggs', '.mypy_cache'
}

def print_tree(path, indent=''):
    try:
        items = sorted(os.listdir(path))
    except PermissionError:
        return

    for item in items:
        if item.startswith('.'):
            continue  # Skip hidden files/folders

        full_path = os.path.join(path, item)

        if os.path.isdir(full_path):
            if item in ignored_folders:
                continue
            print(indent + "|-- " + item)
            print_tree(full_path, indent + "    ")
        else:
            _, ext = os.path.splitext(item)
            if ext in allowed_exts or item in allowed_exts:
                print(indent + "|-- " + item)

# 🔧 Replace with your folder path


folder_path = "D:\Placements\projects\llmpdfQA\QnA-LLM"
print_tree(folder_path)
