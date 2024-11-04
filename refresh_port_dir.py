from global_settings import PORTFOLIO_JSON_SAVE_DIR, PORTFOLIO_ID_PATH, PORTFOLIO_PICKLE_SAVE_DIR
import os
import shutil


if __name__ == "__main__":
    if os.path.exists(PORTFOLIO_JSON_SAVE_DIR):
        shutil.rmtree(PORTFOLIO_JSON_SAVE_DIR)
    if os.path.exists(PORTFOLIO_PICKLE_SAVE_DIR):
        shutil.rmtree(PORTFOLIO_PICKLE_SAVE_DIR)
    os.mkdir(PORTFOLIO_JSON_SAVE_DIR)
    os.mkdir(PORTFOLIO_PICKLE_SAVE_DIR)
    with open(PORTFOLIO_ID_PATH, "w") as f:
        f.write("0")
