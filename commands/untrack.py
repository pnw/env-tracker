from pathlib import Path

from utils import init_project_from_path


def untrack(filepath: [str, Path]):
    """
    - Check if the file is linked properly
    - remove the symlink in the parent dir
    - move the file back to the parent dir
    """
    parent_file_path = Path(filepath)
    if not parent_file_path.exists():
        raise FileNotFoundError(f'Path does not exist: {filepath}')

    project = init_project_from_path(parent_file_path)

    if not parent_file_path.is_symlink():
        raise Exception('Target must be a symlink')

    if project.child_dir not in parent_file_path.resolve().parents:
        raise Exception(f'Target must symlink to a file under: {project.child_dir}')

    path_source = parent_file_path.resolve()

    parent_dir = project.parent_dir
    child_dir = project.child_dir

    try:
        relative_path = parent_file_path.resolve().relative_to(parent_dir)
    except ValueError:
        # ???
        raise

    child_file_path = child_dir / relative_path

    # delete the symlink in parent dir
    parent_file_path.unlink()
    # move the original file back to the parent dir
    child_file_path.replace(parent_file_path)
