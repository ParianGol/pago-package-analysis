from enum import Enum


class SpdxFiles(Enum):
    licenses = 'licenses'
    exceptions = 'exceptions'

    def __str__(self):
        return self.value

    def __repr__(self):
        return str(self.value)


def get_spdx_file(file_name: str) -> SpdxFiles:
    str_to_enum = {
        'licenses': SpdxFiles.licenses,
        'exceptions': SpdxFiles.exceptions,
    }

    return str_to_enum[file_name]
