import os
import zipfile
import gzip
import bz2
import lzma
#Цей блок імпортує модулі, які забезпечують роботу з різними типами архівів:
# os — для роботи з операційною системою, зокрема шляхами до файлів.
# zipfile — для розпакування ZIP-архівів.
# gzip — для розпакування GZIP-архівів.
# bz2 — для розпакування BZIP2-архівів.
# lzma — для роботи з LZMA та XZ-архівами.



def decompress_zip(source_file: str, output_dir: str):
    # Відкриваємо ZIP-файл і витягуємо всі файли у вказану директорію
    with zipfile.ZipFile(source_file, 'r') as archive:
        archive.extractall(output_dir)
    print(f"File decompressed to {output_dir}")
    return None
# Ця функція отримує шлях до ZIP-архіву (source_file) і шлях до
# вихідної директорії (output_dir). Відкривається ZIP-архів (with zipfile) у режимі читання
# ('r') і всі файли розпаковуються в задану директорію. Після цього виводиться повідомлення
# про успішне розпакування.




# Функція для розпакування GZIP-архівів
def decompress_gzip(source_file: str, output_dir: str):
    output_file = os.path.join(output_dir, os.path.basename(source_file).replace('.gz', ''))
    #os.path.join(output_dir, ...) об'єднує шлях до вихідної директорії з назвою файлу
    #без розширення, щоб отримати повний шлях до вихідного файлу.
    #(replace)Визначаємо назву вихідного файлу без розширення .gz
    #os.path.basename(source_file) отримує назву файлу з повного шляху(source_file).

    # Відкриваємо вхідний GZIP-файл для читання і вихідний файл для запису
    with gzip.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        #gzip.open(source_file, 'rb') відкриває архів source_file у режимі читання байтів
        #f_in.read() читає всі байти з вхідного архівного файлу.
        #open(output_file, 'wb') відкриває файл output_file у режимі запису байтів
        f_out.write(f_in.read())  #f_out.write(...) записує ці байти у вихідний файл
    # Повідомляємо користувача про успішне розпакування
    print(f"File decompressed to {output_dir}")
    return None
#(Ця функція розпаковує файл формату .bz2 до вказаної директорії.
# Спочатку вона визначає ім’я вихідного файлу без розширення .bz2,
# відкриває архів для читання, створює новий файл для запису та копіює вміст із
# архіву у вихідний файл. Потім повідомляє користувача про успішну операцію.)




# Функція для розпакування BZIP2-архівів
def decompress_bzip2(source_file: str, output_dir: str):
    # Визначаємо назву вихідного файлу без розширення .bz2
    output_file = os.path.join(output_dir, os.path.basename(source_file).replace('.bz2', ''))
    # Відкриваємо вхідний BZIP2-файл для читання і вихідний файл для запису
    with bz2.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())  # Записуємо вміст у вихідний файл
    # Повідомляємо користувача про успішне розпакування
    print(f"File decompressed to {output_dir}")
    return None
#теж саме що і у попередній функції але обробляється файл із
#розширенням .bz2 за допомогою бібліотеки bz2.




# Функція для розпакування LZMA/XZ-архівів
def decompress_xz(source_file: str, output_dir: str):
    # Визначаємо назву вихідного файлу без розширення .xz
    output_file = os.path.join(output_dir, os.path.basename(source_file).replace('.xz', ''))
    # Відкриваємо вхідний LZMA/XZ-файл для читання і вихідний файл для запису
    with lzma.open(source_file, 'rb') as f_in, open(output_file, 'wb') as f_out:
        f_out.write(f_in.read())  # Записуємо вміст у вихідний файл
    # Повідомляємо користувача про успішне розпакування
    print(f"File decompressed to {output_dir}")
    return None
#Виконує аналогічні операції, але використовує бібліотеку
# lzma для роботи з архівами формату LZMA та XZ.



# Основна функція, що визначає тип архіву і викликає відповідну функцію розпакування
def main():
    # Отримуємо шлях до архіву і вихідної директорії від користувача
    source_file = input("Source file: ")
    output_dir = input("Output directory: ")
    # Визначаємо тип архіву за його розширенням
    archive_type = source_file.split('.')[-1].lower()

    # Викликаємо відповідну функцію залежно від типу архіву
    if archive_type == "zip":
        decompress_zip(source_file, output_dir)
    elif archive_type == "gz":
        decompress_gzip(source_file, output_dir)
    elif archive_type == "bz2":
        decompress_bzip2(source_file, output_dir)
    elif archive_type == "xz":
        decompress_xz(source_file, output_dir)
    else:
        # Виводимо повідомлення, якщо формат архіву не підтримується
        print("Unsupported archive type")

# Точка входу в програму
if __name__ == "__main__":
    main()
