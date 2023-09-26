import pandas as pd
import os


def list_files(dir: str = "./data"):
    for path, subdirs, files in os.walk(dir):
        for name in files:
            yield os.path.join(path, name)

def main():
    for file in list_files():
        print(file)
        df = pd.read_csv(file)
        print(df)
        

if __name__ == "__main__":
    main()