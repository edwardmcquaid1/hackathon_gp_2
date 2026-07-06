from pathlib import Path

class FilePaths:
    BASE_DIR = Path(__file__).resolve().parent.parent
    INPUT_DIR = BASE_DIR / "input"
    OUTPUT_DIR = BASE_DIR / "output"
    SRC_DIR = BASE_DIR / "src"
