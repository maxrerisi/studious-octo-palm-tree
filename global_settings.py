STARTING_BALANCE = 10000
PORTFOLIO_SAVE_DIR = "portfolios"
PORTFOLIO_ID_FILE = "port_id.txt"
PORTFOLIO_ID_PATH = f"{PORTFOLIO_SAVE_DIR}/{PORTFOLIO_ID_FILE}"


# Must run this file to create the appropriate directories and files.
if __name__ == "__main__":
    import os
    if not os.path.exists(PORTFOLIO_SAVE_DIR):
        os.mkdir(PORTFOLIO_SAVE_DIR)
    if not os.path.exists(PORTFOLIO_ID_PATH):
        with open(PORTFOLIO_ID_PATH, "w") as f:
            f.write("0")
