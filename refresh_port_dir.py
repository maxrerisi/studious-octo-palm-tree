from global_settings import PORTFOLIO_SAVE_DIR, PORTFOLIO_ID_PATH
import os
import shutil

if os.path.exists(PORTFOLIO_SAVE_DIR):
    shutil.rmtree(PORTFOLIO_SAVE_DIR)
os.mkdir(PORTFOLIO_SAVE_DIR)
with open(PORTFOLIO_ID_PATH, "w") as f:
    f.write("0")
