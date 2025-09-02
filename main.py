import os

from dotenv import load_dotenv

load_dotenv()


def main():
    print(os.getenv("DATABASE_URL"))


if __name__ == "__main__":
    main()
