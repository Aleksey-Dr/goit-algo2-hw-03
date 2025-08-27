# -*- coding: utf-8 -*-

import csv
from BTrees.OOBTree import OOBTree
import timeit

# Функції для додавання елементів
def add_item_to_tree(tree, item):
    """Додає елемент до OOBTree."""
    # Використання 'Price' як ключа для увімкнення діапазонних запитів за цінами
    tree[item['Price']] = item

def add_item_to_dict(d, item):
    """Додає елемент до словника dict."""
    d[item['ID']] = item

# Функції для діапазонних запитів
def range_query_tree(tree, min_price, max_price):
    """Виконує діапазонний запит на OOBTree."""
    results = []
    # OOBTree забезпечує ефективну ітерацію по діапазону
    for item in tree.values(min_price, max_price):
        results.append(item)
    return results

def range_query_dict(d, min_price, max_price):
    """Виконує діапазонний запит на словнику dict за допомогою лінійного пошуку."""
    results = []
    # Стандартний словник dict вимагає ітерації по всіх значеннях для пошуку збігів
    for item in d.values():
        if min_price <= item['Price'] <= max_price:
            results.append(item)
    return results

# Головний скрипт
if __name__ == "__main__":
    file_path = 'generated_items_data.csv'
    
    # Ініціалізація структур даних
    oobtree = OOBTree()
    product_dict = {}
    
    # Завантаження даних з CSV
    print("Завантаження даних...")
    items_list = []
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row['ID'] = int(row['ID'])
            row['Price'] = float(row['Price'])
            items_list.append(row)
    
    # Заповнення структур даних
    print("Заповнення OOBTree та dict...")
    for item in items_list:
        add_item_to_tree(oobtree, item)
        add_item_to_dict(product_dict, item)

    # Визначення діапазону для запиту
    min_price_query = 150.0
    max_price_query = 250.0

    # Вимірювання продуктивності для OOBTree
    print("Вимірювання продуктивності для OOBTree...")
    total_time_oobtree = timeit.timeit(
        lambda: range_query_tree(oobtree, min_price_query, max_price_query),
        number=100
    )

    # Вимірювання продуктивності для словника dict
    print("Вимірювання продуктивності для словника dict...")
    total_time_dict = timeit.timeit(
        lambda: range_query_dict(product_dict, min_price_query, max_price_query),
        number=100
    )

    # Відображення результатів
    print("\n--- Результати продуктивності ---")
    print(f"Загальний час для діапазонного запиту (OOBTree): {total_time_oobtree:.6f} секунд")
    print(f"Загальний час для діапазонного запиту (Dict): {total_time_dict:.6f} секунд")

    # Додатково: Перевірка результатів
    print("\n--- Перевірка ---")
    results_oobtree = range_query_tree(oobtree, min_price_query, max_price_query)
    results_dict = range_query_dict(product_dict, min_price_query, max_price_query)
    print(f"Кількість знайдених елементів (OOBTree): {len(results_oobtree)}")
    print(f"Кількість знайдених елементів (Dict): {len(results_dict)}")

    # Перевірка, чи є результати ідентичними
    if sorted(results_oobtree, key=lambda x: x['ID']) == sorted(results_dict, key=lambda x: x['ID']):
        print("Результати з обох структур ідентичні.")
    else:
        print("Результати з обох структур різні.")