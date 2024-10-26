import os
import random
import string
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
        return 'xz'
    else:
        raise TypeError('Invalid archive type! Choose one of supported: zip, gzip, bz2, lzma')


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
        new_file_path = os.path.join(out_dir, f'{file_name_without_ext}_{today_date}_{n}{file_ext}.{arch_type}')
        if os.path.exists(new_file_path):
            n += 1
        else:
            break

    return new_file_path


def compress_file(file_path: str, out_file_path: str, arch_type: str) -> str:
    """

    :param file_path:
    :param out_file_path:
    :param arch_type:
    :return:
    """
    if archive_type == "zip":
        with zipfile.ZipFile(out_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))

    elif arch_type == "gz":
        with open(file_path, "rb") as f_in, gzip.open(out_file_path, "wb") as f_out:
            f_out.writelines(f_in)

    elif archive_type == "bz2":
        with open(file_path, "rb") as f_in, bz2.open(out_file_path, "wb") as f_out:
            f_out.writelines(f_in)

    elif archive_type == "xz":
        with open(file_path, "rb") as f_in, lzma.open(out_file_path, "wb") as f_out:
            f_out.writelines(f_in)
    else:
        raise ValueError("Unsupported archive type. Choose zip, gzip, bz2, or lzma.")

    return out_file_path


def fill_file_with_random_chars():
    file_name = "random_text.txt"
    length = int(input("Введіть кількість символів: "))

    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length))

    # Записуємо символи у файл
    with open(file_name, "w") as file:
        file.write(random_chars)

if __name__ == '__main__':
    # fill_file_with_random_chars()
    # source_file = input("Source file: ")
    # output_directory = input("Output directory: ")
    # archive_type = input("Archive type: ")
    source_file = "C:/PycharmProjects/pythonProject/lab1/test.txt"
    output_directory = 'C:/PycharmProjects/pythonProject/lab1/'
    archive_type = 'lzma'

    validate_file_path(file_path=source_file, out_dir=output_directory)
    archive_type = validate_archive_type(archive_type)

    generated_archive_path = generate_archive_name(file_path=source_file, out_dir=output_directory, arch_type=archive_type)
    created_archive_path = compress_file(file_path=source_file, out_file_path=generated_archive_path, arch_type=archive_type)
    print(f'Результат роботи: архів {created_archive_path}')
