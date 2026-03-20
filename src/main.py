import os
import utils


def main():
    root_dir = os.path.join(os.path.dirname(__file__), "..")
    utils.copy_folder("static", "public")


if __name__ == "__main__":
    main()
