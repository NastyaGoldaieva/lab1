import os
import zipfile
import gzip
import bz2
import lzma
from datetime import datetime


def validate_archive_type(arch_type: str) -> str:
    if arch_type == 'zip':
        return 'zip'
    elif arch_type == 'gzip':
        return 'gz'
    elif arch_type == 'bz2':
        return 'bz2'
    elif arch_type == 'lzma':
        return 'lzma'
    else:
        raise TypeError('Invalid archive type!')


def validate_file_path(file_path: str, out_dir: str):
    if not os.path.exists(file_path):
        raise Exception(f'File does not exists: {file_path}')
    if not os.path.exists(out_dir):
        os.mkdir(out_dir)


def generate_archive_name(file_path: str, out_dir: str, arch_type: str) -> str:
    file_name = os.path.basename(file_path)
    file_name_without_ext, file_ext = os.path.splitext(file_name)
    today_date = datetime.today().strftime('%Y%m%d')
    n = 1

    while True:
        new_file_name = os.path.join(out_dir, f'{file_name_without_ext}_{today_date}_{n}{file_ext}.{arch_type}')
        if os.path.exists(new_file_name):
            n += 1
        else:
            break

    return new_file_name


def compress_to_zip(filename: str, out_dir: str) -> None:
    ...


if __name__ == '__main__':
    # source_file = input("Source file: ")
    # output_directory = input("Output directory: ")
    # archive_type = input("Archive type: ")
    source_file = "C:/PycharmProjects/pythonProject/lab1/test.txt"
    output_directory = 'C:/PycharmProjects/pythonProject/lab1/test'
    archive_type = 'gzip'

    validate_file_path(file_path=source_file, out_dir=output_directory)
    archive_type = validate_archive_type(archive_type)

    archive_path = generate_archive_name(file_path=source_file, out_dir=output_directory, arch_type=archive_type)
    print(archive_path)
