import argparse






if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", type=str, default="DP",choices=["DP", "A*", "genetic"])
    args = parser.parse_args()
    data_root = "./data"
    