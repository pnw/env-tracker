"""
Functions for managing the temp directories
needed for the tests to run.
"""

from pathlib import Path
import shutil
import tempfile

test_workspace = Path(tempfile.gettempdir() + '/io.ptrck.env-tracker')


def create_test_workspace() -> Path:
    """
    Creates a namespace in the tempfile directory to be used
    for any temp files or dirs these tests create
    """
    if not test_workspace.exists():
        test_workspace.mkdir(exist_ok=True)

    return test_workspace


def flush_test_workspace():
    """
    Clears out the contents of the temp dir namespace
    created by create_test_dir
    """

    def remove_folder(path: Path):
        # check if folder exists
        if path.exists():
            # remove if exists
            shutil.rmtree(str(path))

    remove_folder(test_workspace)
