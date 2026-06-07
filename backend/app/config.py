from pathlib import Path

BASE_DIR = Path(__file__).resolve().parents[2]
MODEL_PATH = BASE_DIR / "weights" / "best.pt"

CLASS_NAMES = {
    0: "crack",
    1: "spalling"
}

CONF_THRESHOLD = 0.25
IOU_THRESHOLD = 0.45
IMAGE_SIZE = 640