import os.path
from dataclasses import dataclass
from typing import Optional

from hana04.base.util.path_util import relativize_second_to_first_dir, normalize_path_separator


@dataclass(eq=True, frozen=True)
class FilePath:
    save_as_relative: bool
    stored_path: str

    def __post_init__(self):
        assert self.stored_path is not None
        assert len(self.stored_path) > 0

    @staticmethod
    def absolute(path: str):
        return FilePath(False, path)

    @staticmethod
    def relative(path: str):
        return FilePath(True, path)

    def get_serialized_path(self, file_name: Optional[str]):
        if not self.save_as_relative or file_name is None:
            return self.stored_path
        else:
            return relativize_second_to_first_dir(file_name, self.stored_path)

    @staticmethod
    def compute_path_to_store(raw_path: str, file_name: Optional[str]):
        if file_name is None:
            return raw_path
        else:
            dir = os.path.dirname(file_name)
            return normalize_path_separator(os.path.normpath(dir + "/" + raw_path))
