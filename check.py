import os
from utils import extract_entities


def main():
    q = "Nhung is very stupid. JAVA"
    print("Kết quả:", extract_entities(q))

if __name__ == "__main__":
    main()