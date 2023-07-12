import os


def find_project_root():
    current_dir = os.getcwd()

    # Iteratively ascend through directories until a file or directory indicating the project root is found.
    while True:
        if os.path.isfile(os.path.join(current_dir, "README.md")) or os.path.isdir(
            os.path.join(current_dir, ".git")
        ):
            return current_dir

        parent_dir = os.path.dirname(current_dir)
        if parent_dir == current_dir:
            raise Exception("Could not find project root directory")

        current_dir = parent_dir
