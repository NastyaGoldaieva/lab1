import os
import random
import string
import zipfile
import gzip
import bz2
import lzma
from datetime import datetime

# оголошує функцію validate_archive_type (перевіряє чи є вхідний параметр arch_type
# підтримуваним типом архіву),
# перевіряємо чи користувач ввів той тип роширееня, який підтримує archive_type
def validate_archive_type(arch_type: str) -> str:
    if arch_type == 'zip':  # Якщо користувач ввів "zip" ми повертаємо "zip"
        return 'zip'
    elif arch_type == 'gzip': # Якщо користувач ввів "gzip" ми повертаємо "gz"
        return 'gz'
    elif arch_type == 'bz2': # Якщо користувач ввів "bz2" ми повертаємо "bz2"
        return 'bz2'
    elif arch_type == 'lzma': # Якщо користувач ввів "lzma" ми повертаємо "xz"
        return 'xz'
    else:
        raise TypeError('Invalid archive type! Choose one of supported: zip, gzip, bz2, lzma')
        # Якщо користувач ввів тип розширення, який не підтимує в archive_type ми виводимо помилку

# Оголошуємо функцію validate_file_path (validate - перевірити)
# exists виводить значення тільки Nrue або False
def validate_file_path(file_path: str, out_dir: str):
    if not os.path.exists(file_path):  # Якщо os.path.exists(file_path) не існує за шляхом file_path,
        raise Exception(f'File does not exists: {file_path}') # то ми виводимо помилку
    if not os.path.exists(out_dir): # Якщо файлу немає ми його створюємо
        os.mkdir(out_dir)

# Оголошуємо функцію generate_archive_name
def generate_archive_name(file_path: str, out_dir: str, arch_type: str) -> str:
    file_name = os.path.basename(file_path) # Повернтаємо тільки назву файлу з його розширенням, без шляху
    file_name_without_ext, file_ext = os.path.splitext(file_name)  # splitext - розбиває на назву файла та розширення
    today_date = datetime.today().strftime('%Y%m%d') # Сьогоднішня дата
    n = 1 # Число N = 1

    while True: # Поки True
        new_file_path = os.path.join(out_dir, f'{file_name_without_ext}_{today_date}_{n}{file_ext}.{arch_type}')
        if os.path.exists(new_file_path):
            n += 1
        else:
            break

    return new_file_path


# Оголошуємо функцію, яка виконує стиснення файлу
def compress_file(file_path: str, out_file_path: str, arch_type: str) -> str:
    if archive_type == "zip":
        with zipfile.ZipFile(out_file_path, "w", zipfile.ZIP_DEFLATED) as zipf:
            # Cтворює новий ZIP-архів за шляхом out_file_path. "w" означає, що архів відкривається для запису,
            # а zipfile.ZIP_DEFLATED вказує на використання алгоритму стиснення
            zipf.write(file_path, arcname=os.path.basename(file_path)) # Додає file_path у ZIP-архів як arcname
            # (ім’я файлу в архіві), яке отримується за допомогою os.path.basename(file_path).

    elif arch_type == "gz": # якщо arch_type дорівнює "gz", використовується формат GZIP
        with open(file_path, "rb") as f_in, gzip.open(out_file_path, "wb") as f_out:
            # Відкриває file_path для читання в бінарному режимі ("rb") як f_in, а out_file_path для запису у форматі
            # GZIP ("wb") як f_out.
            f_out.writelines(f_in) # Записує вміст f_in у f_out, створюючи GZIP-архів.

    elif archive_type == "bz2": # Якщо arch_type дорівнює "bz2", використовується формат BZIP2.
        with open(file_path, "rb") as f_in, bz2.open(out_file_path, "wb") as f_out: # відкриває file_path для
            # читання як f_in, а out_file_path для запису у форматі BZIP2 як f_out.
            f_out.writelines(f_in) #записує вміст f_in у f_out, створюючи BZIP2-архів.

    elif archive_type == "xz": # якщо arch_type дорівнює "xz", використовується формат LZMA (XZ).
        with open(file_path, "rb") as f_in, lzma.open(out_file_path, "wb") as f_out: #відкриває file_path для
            # читання як f_in, а out_file_path для запису у форматі LZMA як f_out.
            f_out.writelines(f_in) # записує вміст f_in у f_out, створюючи LZMA-архів.
    else: # якщо arch_type не дорівнює жодному із зазначених значень ("zip", "gz", "bz2", або "xz"),
        # викликається помилка ValueError.
        raise ValueError("Unsupported archive type. Choose zip, gzip, bz2, or lzma.")

    return out_file_path

#  назва функції, яка створює файл і заповнює його випадковими символами.
def fill_file_with_random_chars():
    file_name = "random_text.txt" #file_name — назва файлу, в який будуть записані випадкові символи.
    # У цьому випадку, назва файлу — "random_text.txt".
    length = int(input("Введіть кількість символів: ")) #Виконується запит на введення кількості символів, які потрібно згенерувати.
    # input("Введіть кількість символів: ") — показує повідомлення і приймає введення від користувача.
    # int(...) — перетворює введене значення на ціле число і зберігає його у змінній length.

    random_chars = ''.join(random.choices(string.ascii_letters + string.digits, k=length)) #функція random.choices
    # генерує список випадкових символів. string.ascii_letters + string.digits об’єднує всі латинські букви (великі та малі)
    # і цифри, з яких буде обрано символи, а k=length задає кількість символів для генерації. ''.join(...) об’єднує всі
    # згенеровані символи в один рядок і зберігає цей рядок у змінній random_chars.

    # Записуємо символи у файл
    with open(file_name, "w") as file: # відкриває файл із назвою file_name у режимі запису ("w"). Якщо файл із такою
        # назвою не існує, він буде створений; якщо існує — його вміст буде перезаписано
        file.write(random_chars) # записує рядок random_chars (з випадковими символами) у файл.

#  Оголошуємо функцію compress_folder
def compress_folder(folder_path: str, out_file_path: str, arch_type: str):
    if arch_type != "zip": # Функція перевіряє чи параметр arch_type є рядком zip
        raise ValueError("File is not a zip file") # Якщо тип розширення не zip,то викликаємо помилку

    with zipfile.ZipFile(out_file_path, 'w', zipfile.ZIP_DEFLATED) as zipf: # Цей рядок створює або відкриває
        # ZIP-архів для запису за вказаним шляхом out_file_path і визначає змінну zipf для роботи з архівом. Використовується
        # режим 'w' (write), який дозволяє записувати дані, та zipfile.ZIP_DEFLATED, який вмикає стиснення файлів.
        for root, dirs, files in os.walk(folder_path):
            for file in files: #Цикл for перебирає кожен файл у списку files. Для кожного файлу виконується таке:
# file_path = os.path.join(root, file): створюється повний шлях до файлу.
#arcname = os.path.relpath(file_path, folder_path): визначається відносний шлях arcname від кореня folder_path до file_path. Цей шлях зберігається в архіві для збереження структури папок.
#zipf.write(file_path, arcname): файл додається до архіву з вказаним відносним шляхом arcname.
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, folder_path)
                zipf.write(file_path, arcname)

    print(f"Folder '{folder_path}' has been compressed into '{out_file_path}'") # Після завершення архівації функція
    # виводить повідомлення про успішне стиснення папки.
    return out_file_path # Функція повертає шлях до створеного архіву out_file_path, щоб результат можна було використати
    # в подальшому коді.


if __name__ == '__main__':
    fill_file_with_random_chars()  # заповнує певний файл випадковими символами
    source_file = input("Source file: ")
    output_directory = input("Output directory: ")
    archive_type = input("Archive type: ")
    # source_file = "C:/PycharmProjects/pythonProject/lab1/test.txt" # Шлях до файла
    # output_directory = 'C:/PycharmProjects/pythonProject/lab1/' # Папка для збереження архіву
    # archive_type = 'lzma' # Тип розширення

    validate_file_path(file_path=source_file, out_dir=output_directory)
    archive_type = validate_archive_type(archive_type)

    generated_archive_path = generate_archive_name(file_path=source_file, out_dir=output_directory, arch_type=archive_type)
    created_archive_path = compress_file(file_path=source_file, out_file_path=generated_archive_path, arch_type=archive_type)
    print(f'Результат роботи: архів {created_archive_path}')
