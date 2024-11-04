import os
import zipfile
import gzip
import bz2
import lzma
import tarfile
from datetime import datetime
import argparse
import random
import string


def validate_archive_type(arch_type: str) -> str:
    supported_types = ['zip', 'gzip', 'bz2', 'lzma', 'tar']
    if arch_type not in supported_types:
        raise TypeError(f'Invalid archive type! Choose one of supported: {", ".join(supported_types)}')
    return arch_type

def validate_file_path(file_path: str, out_dir: str):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f'File does not exist: {file_path}')
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

# Компресія файлу
def compress_file(file_path: str, out_file_path: str, arch_type: str) -> str:
    if arch_type == "zip":
        with zipfile.ZipFile(out_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            zipf.write(file_path, arcname=os.path.basename(file_path))

    elif arch_type == "gz":
        with open(file_path, "rb") as f_in, gzip.open(out_file_path, "wb") as f_out:
            f_out.writelines(f_in)

    elif arch_type == "bz2":
        with open(file_path, "rb") as f_in, bz2.open(out_file_path, "wb") as f_out:
            f_out.writelines(f_in)

    elif arch_type == "xz":
        with open(file_path, "rb") as f_in, lzma.open(out_file_path, "wb") as f_out:
            f_out.writelines(f_in)

    elif arch_type == "tar":
        with tarfile.open(out_file_path, "w") as tarf:
            tarf.add(file_path, arcname=os.path.basename(file_path))
    else:
        raise ValueError("Unsupported archive type. Choose zip, gzip, bz2, lzma, or tar.")

    return out_file_path

# Функції декомпресії
def add_timestamp(file_name: str) -> str:
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    base, ext = os.path.splitext(file_name)
    return f"{base}_{timestamp}{ext}"

def decompress_zip(source_file: str, output_dir: str):
    with zipfile.ZipFile(source_file, 'r') as archive:
        for member in archive.namelist():
            original_name = os.path.basename(member)
            if original_name:
                new_name = add_timestamp(original_name)
                archive.extract(member, output_dir)
                os.rename(os.path.join(output_dir, member), os.path.join(output_dir, new_name))
    print(f"ZIP file decompressed to {output_dir}")

def decompress_gzip(source_file: str, output_dir: str):
    output_file = os.path.join(output_dir, add_timestamp(os.path.basename(source_file).replace('.gz', '')))
    with gzip.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())
    print(f"GZIP file decompressed to {output_dir}")

def decompress_bzip2(source_file: str, output_dir: str):
    output_file = os.path.join(output_dir, add_timestamp(os.path.basename(source_file).replace('.bz2', '')))
    with bz2.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())
    print(f"BZIP2 file decompressed to {output_dir}")

def decompress_xz(source_file: str, output_dir: str):
    output_file = os.path.join(output_dir, add_timestamp(os.path.basename(source_file).replace('.xz', '')))
    with lzma.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())
    print(f"LZMA/XZ file decompressed to {output_dir}")

def decompress_tar(source_file: str, output_dir: str):
    with tarfile.open(source_file, 'r') as archive:
        for member in archive.getmembers():
            original_name = os.path.basename(member.name)
            if original_name:
                new_name = add_timestamp(original_name)
                member.name = new_name
                archive.extract(member, output_dir)
    print(f"TAR file decompressed to {output_dir}")

# Основна функція
def main():
    parser = argparse.ArgumentParser(description="Compress or decompress files.")
    parser.add_argument("operation", choices=["compress", "decompress"], help="Operation to perform")
    parser.add_argument("source", help="Source file or folder path")
    parser.add_argument("output_dir", help="Output directory")
    parser.add_argument("archive_type", help="Archive type (zip, gzip, bz2, lzma, tar)")
    args = parser.parse_args()

    if args.operation == "compress":
        validate_file_path(args.source, args.output_dir)
        arch_type = validate_archive_type(args.archive_type)
        archive_path = generate_archive_name(args.source, args.output_dir, arch_type)
        compress_file(args.source, archive_path, arch_type)
        print(f"File compressed to {archive_path}")

    elif args.operation == "decompress":
        archive_type = args.source.split('.')[-1].lower()
        if archive_type == "zip":
            decompress_zip(args.source, args.output_dir)
        elif archive_type == "gz":
            decompress_gzip(args.source, args.output_dir)
        elif archive_type == "bz2":
            decompress_bzip2(args.source, args.output_dir)
        elif archive_type == "xz":
            decompress_xz(args.source, args.output_dir)
        elif archive_type == "tar":
            decompress_tar(args.source, args.output_dir)
        else:
            print("Unsupported archive type")

if __name__ == "__main__":
    main()
