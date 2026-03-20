# import os
import utils
import generator


def main():
    # root_dir = os.path.join(os.path.dirname(__file__), "..")
    utils.copy_folder("static", "public")
    generator.generate_pages_recursive("content", "template.html", "public")


if __name__ == "__main__":
    main()
