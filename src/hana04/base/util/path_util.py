import os.path


def normalize_path_separator(path: str):
    if os.sep != '/':
        return path.replace(os.sep, "/")
    else:
        return path


def relativize_second_to_first(first_dir: str, second_file: str):
    first_dir = os.path.abspath(first_dir)
    second_file = os.path.abspath(second_file)
    relative_path = os.path.relpath(second_file, first_dir)
    return normalize_path_separator(relative_path)


def relativize_second_to_first_dir(first_file: str, second_file: str):
    first_file = os.path.abspath(first_file)
    second_file = os.path.abspath(second_file)
    first_dir = os.path.dirname(first_file)
    relative_path = os.path.relpath(second_file, first_dir)
    return normalize_path_separator(relative_path)


def get_normalized_absolute_path(path: str):
    return normalize_path_separator(os.path.abspath(path))


if __name__ == "__main__":
    print(relativize_second_to_first("a/b/d", "a/c/p.txt"))
    print(get_normalized_absolute_path("a/b/c.txt"))
