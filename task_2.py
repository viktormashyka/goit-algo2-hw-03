import timeit
import pandas as pd
from BTrees.OOBTree import OOBTree

# Завантаження даних із файлу
file_path = "generated_items_data.csv"

try:
    df = pd.read_csv(file_path)
except FileNotFoundError:
    print("Файл не знайдено. Переконайтеся, що він завантажений.")
    df = pd.DataFrame()

# Перевірка структури даних
if not df.empty:
    print(df.head())

# Ініціалізація структур даних
tree = OOBTree()
dictionary = {}

# Функція для додавання товару в OOBTree
def add_item_to_tree(item_id, name, category, price):
    tree[item_id] = {"Name": name, "Category": category, "Price": price}

# Функція для додавання товару в dict
def add_item_to_dict(item_id, name, category, price):
    dictionary[item_id] = {"Name": name, "Category": category, "Price": price}

# Заповнення структур даними
if not df.empty:
    for _, row in df.iterrows():
        add_item_to_tree(row["ID"], row["Name"], row["Category"], row["Price"])
        add_item_to_dict(row["ID"], row["Name"], row["Category"], row["Price"])

# Функція для діапазонного запиту в OOBTree
def range_query_tree(min_price, max_price):
    return [item for _, item in tree.items() if min_price <= item["Price"] <= max_price]

# Функція для діапазонного запиту в dict
def range_query_dict(min_price, max_price):
    return [item for item in dictionary.values() if min_price <= item["Price"] <= max_price]

# Визначення діапазону цін для тестування
min_price = 10
max_price = 50

# Вимірювання продуктивності для OOBTree
time_tree = timeit.timeit(lambda: range_query_tree(min_price, max_price), number=100)

# Вимірювання продуктивності для dict
time_dict = timeit.timeit(lambda: range_query_dict(min_price, max_price), number=100)

# Вивід результатів
print(f"Total range_query time for OOBTree: {time_tree:.6f} seconds")
print(f"Total range_query time for Dict: {time_dict:.6f} seconds")
