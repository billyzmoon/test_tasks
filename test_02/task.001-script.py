import pandas as pd
import os


def read_csv_with_sep_detection(file_path):
    with open(file_path, 'r', encoding='windows-1251') as file:
        first_line = file.readline().strip()
        skip_rows = 1 if first_line.startswith("sep=;") else 0  # Пропуск строки "sep = ;", если нужно

    return pd.read_csv(file_path, sep=';', skiprows=skip_rows, encoding='windows-1251', dtype='str')


def compare_catalogs(our_catalog_path, competitors_catalog_folder, output_path='matched_products.csv'):
    try:
        our_catalog = read_csv_with_sep_detection(our_catalog_path)
    except Exception as e:
        print(f"Ошибка при загрузке нашего каталога: {e}")
        return

    # Убедимся, что необходимые столбцы присутствуют
    if not {'Бренд', 'Артикул', 'Код товара', 'Наименование'}.issubset(our_catalog.columns):
        print("Каталог наших товаров должен содержать столбцы: 'Бренд', 'Артикул', 'Код товара', 'Наименование'.")
        return

    # Список для хранения совпавших товаров
    matched_products = []

    # Обработка всех файлов из папки конкурентов
    for file_name in os.listdir(competitors_catalog_folder):
        competitor_file_path = os.path.join(competitors_catalog_folder, file_name)

        if not competitor_file_path.endswith('.csv'): # Пропустим, если не CSV
            continue

        try:
            competitor_catalog = read_csv_with_sep_detection(competitor_file_path)
        except Exception as e:
            print(f"Ошибка при загрузке каталога конкурентов {file_name}: {e}")
            continue

        if not {'Бренд', 'Артикул', 'Код', 'Название'}.issubset(competitor_catalog.columns):
            print(f"Каталог конкурентов {file_name} должен содержать столбцы: 'Бренд', 'Артикул', 'Код', 'Название'.")
            print(competitor_catalog)
            continue

        # Сравнение по <Бренд, Артикул>
        merged = pd.merge(
            our_catalog,
            competitor_catalog,
            on=['Бренд', 'Артикул'],
            suffixes=('', '_конкурента')
        )

        # Выбор нужных столбцов
        matched = merged[['Код товара', 'Код', 'Наименование', 'Бренд', 'Артикул']]
        matched_products.append(matched)

    # Объединяем все совпадения из разных файлов конкурентов
    if matched_products:
        final_matched = pd.concat(matched_products, ignore_index=True)
        final_matched = final_matched.rename(columns={'Код':'Код товара у конкурента', 'Наименование':'Наименование товара'})
        final_matched = final_matched.drop_duplicates()
        final_matched.to_csv(output_path, index=False, encoding='utf-8-sig')
        print(f"Совпавшие товары сохранены в файл: {output_path}")
    else:
        print("Совпадений не найдено.")


our_catalog_path = input('Введите путь до файла каталога наших товаров: ')
competitors_catalog_folder = input('Введите путь до папки каталога конкурентов: ')

compare_catalogs(
    our_catalog_path,
    competitors_catalog_folder,
    output_path='matched_products.csv'
)