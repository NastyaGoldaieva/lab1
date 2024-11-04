import os        #os — для роботи з файлами і шляхами в операційній системі.
import zipfile
import gzip      #для роботи з архівами zip,gzip,bzip2,lzma
import bz2
import lzma
from datetime import datetime
import argparse    #argparse — для обробки параметрів командного рядка.




def add_timestamp(file_name: str) -> str:
    """Adds a timestamp to the file name.""" #Додає мітку часу до імені файлу.
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S") #створює мітку часу у форматі
    base, ext = os.path.splitext(file_name) #os.path.splitext(file_name) — розбиває ім'я файлу на дві частини:
    # назва файлу (base) та розширення (ext).
    return f"{base}_{timestamp}{ext}" #Повертає нове ім'я файлу у вигляді base_timestamp.ext, де timestamp — наша мітка часу.




def decompress_zip(source_file: str, output_dir: str):#source_file: шлях до GZIP-архіву
                                     #output_dir: папка, куди буде збережений розпакований файл.
    """Decompress ZIP archives with a timestamp added to extracted files.""" #Розпаковує ZIP-архів і додає мітку часу
    # до кожного розпакованого файлу.
    with zipfile.ZipFile(source_file, 'r') as archive: #відкриває ZIP-файл для читання(режим читання r).
        for member in archive.namelist(): #archive.namelist() повертає список всіх файлів та папок у ZIP-архіві.
            original_name = os.path.basename(member)#os.path.basename(member) виділяє лише ім'я файлу з повного шляху.
            # Наприклад, якщо member дорівнює "folder/subfolder/file.txt", то os.path.basename(member) поверне "file.txt".
            if original_name:  # avoid directories   #Якщо original_name містить назву, тоді елемент є файлом, а не папкою.
                new_name = add_timestamp(original_name) #додає мітку пасу до імені файлу
                archive.extract(member, output_dir) #Розпаковка файлу у вказану директорію(output_dir)
                os.rename(os.path.join(output_dir, member), os.path.join(output_dir, new_name))
                #os.path.join(output_dir, member) створює повний шлях до розпакованого файлу у вихідній папці.
#os.path.join(output_dir, new_name) створює новий шлях для файлу з міткою часу.
#os.rename(...) перейменовує файл з оригінальної назви на нову з доданою міткою часу.
                print(f"ZIP file decompressed to {output_dir}")

def decompress_gzip(source_file: str, output_dir: str):
    """Decompress GZIP archives with a timestamp added to extracted file.""" #Розпаковує GZIP-архів і додає мітку часу
    # до імені розпакованого файл
    output_file = os.path.join(output_dir, add_timestamp(os.path.basename(source_file).replace('.gz', '')))
    #os.path.join(output_dir, ...): об'єднує папку output_dir з новим ім'ям файлу, створюючи повний шлях до розпакованого файлу.
    #add_timestamp(...): додає мітку часу до імені файлу.
    #os.path.basename(source_file): отримує тільки ім'я файлу без шляху.
    #.replace('.gz', ''): прибирає розширення .gz
    with gzip.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        #gzip.open(source_file, 'rb'): відкриває архівний файл source_file у режимі читання байтів ('rb' — read binary)
        #open(output_file, 'wb'): створює новий файл у папці output_dir з іменем output_file у режимі запису байтів ('wb' — write binary).
        #as f_in, open(...) as f_out: вказує, що f_in — це вхідний файл (архів), а f_out — вихідний файл (розпакований файл).
        f_out.write(f_in.read())
        #f_in.read(): читає всі дані з архіву source_file.
        #f_out.write(...): записує ці дані у новий файл output_file, розпаковуючи їх.
    print(f"GZIP file decompressed to {output_dir}")




def decompress_bzip2(source_file: str, output_dir: str):
    """Decompress BZIP2 archives with a timestamp added to extracted file."""
    output_file = os.path.join(output_dir, add_timestamp(os.path.basename(source_file).replace('.bz2', '')))
    with bz2.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())
    print(f"BZIP2 file decompressed to {output_dir}")




def decompress_xz(source_file: str, output_dir: str):
    """Decompress LZMA/XZ archives with a timestamp added to extracted file."""
    output_file = os.path.join(output_dir, add_timestamp(os.path.basename(source_file).replace('.xz', '')))
    with lzma.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())
    print(f"LZMA/XZ file decompressed to {output_dir}")




def main():
    parser = argparse.ArgumentParser(description="Decompress different types of archives with a timestamp.")
    #argparse.ArgumentParser(...) створює об’єкт parser, який обробляє параметри, введені в командному рядку.
    #description="..." додає опис до parser
    parser.add_argument("source_file", help="Path to the archive file")
    parser.add_argument("output_dir", help="Directory where files will be extracted")
    #parser.add_argument(...) додає два обов’язкові параметри командного рядка:
    #"source_file": шлях до архівного файлу, який потрібно розпакувати.
    #"output_dir": папка, в яку будуть розпаковані файли.
    #help="..." надає короткий опис для кожного параметра, щоб користувачі розуміли, що саме потрібно ввести.
    args = parser.parse_args()
    #parser.parse_args() зчитує параметри, які ввів користувач, і зберігає їх у об’єкті args.
    source_file = args.source_file
    output_dir = args
    #source_file отримує значення шляху до архіву з args.source_file.
    #output_dir отримує значення папки для розпакованих файлів з args.output_dir.
      # Determine the archive type by its extension
    archive_type = source_file.split('.')[-1].lower()
    # Call the appropriate function based on the archive type
    if archive_type == "zip":
        decompress_zip(source_file, output_dir)
    elif archive_type == "gz":
        decompress_gzip(source_file, output_dir)
    elif archive_type == "bz2":
        decompress_bzip2(source_file, output_dir)
    elif archive_type == "xz":
        decompress_xz(source_file, output_dir)
    else:
        print("Unsupported archive type")

if __name__ == "__main__":
    main()
