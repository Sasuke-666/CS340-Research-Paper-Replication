"""Publish derived files without following existing file links into raw evidence."""
from contextlib import contextmanager
from pathlib import Path
import tempfile


@contextmanager
def staged_summary(output, names):
    """Finish serialization off to the side before replacing any existing tables."""
    output = Path(output)
    output.mkdir(parents=True, exist_ok=True)
    for name in names:
        target = output / name
        if target.is_symlink() or (target.exists() and not target.is_file()):
            raise ValueError("Expected an ordinary summary file: " + str(target))
    with tempfile.TemporaryDirectory(prefix=".summary-", dir=output) as directory:
        stage = Path(directory)
        yield stage
        if any(not (stage / name).is_file() for name in names):
            raise ValueError("Incomplete derived file set")
        for name in names:
            # Replacing a directory entry also leaves any hard-linked raw file intact.
            (stage / name).replace(output / name)
