import sys
import utils
import generator


def main():
    base_path = "/"
    if len(sys.argv) > 1:
        base_path = sys.argv[1]
    utils.copy_folder("static", "docs")
    generator.generate_pages_recursive("content", "template.html", "docs", base_path)


if __name__ == "__main__":
    main()
