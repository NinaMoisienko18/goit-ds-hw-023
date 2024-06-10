from pymongo import MongoClient
from pymongo.server_api import ServerApi
import os
import certifi
from colorama import Fore, Style

os.environ[
    'SSL_CERT_FILE'] = certifi.where()  # пакет сертифікатів CA, що використовується для перевірки SSL-сертифікатів

client = MongoClient(
    "mongodb+srv://nmnysya:Lavanda18@goitproject.cws87xv.mongodb.net/",
    server_api=ServerApi('1')
)

db = client.Cats


def insert_data_to_db(db):
    db.cats.insert_many(
        [
            {
                "name": "Lama",
                "age": 2,
                "features": ["ходить в лоток", "не дає себе гладити", "сірий"],
            },
            {
                "name": "Liza",
                "age": 4,
                "features": ["ходить в лоток", "дає себе гладити", "білий"],
            },
            {
                "name": "Nina",
                "age": 3,
                "features": ["ходить в лоток", "не дає себе гладити", "злюка", "рудий"]
            }
        ]
    )


def reading(db):
    result = db.cats.find({})
    print(f"{Fore.LIGHTCYAN_EX}🗂Всі записи колекції [{db.name}]: {Style.RESET_ALL}")
    for idx, el in enumerate(result):
        print(f"\t----> [{idx + 1}] {el}")


def find_info_about_cat(db):
    result = db.cats.find({}, {"_id": 0, "name": 1})
    names = [doc["name"] for doc in result]
    print(f"{Fore.LIGHTCYAN_EX}🗂 Всі імена котів у колекції [{db.name}]: {Style.RESET_ALL}")
    for idx, el in enumerate(names):
        print(f"\t----> [{idx + 1}] {el}")

    while True:
        user_input = input(
            f"Оберіть номер кота, щоб вивести інфо про нього {[num + 1 for num, name in enumerate(names)]} або "
            f"напишіть 'exit', щоб вийти: ")
        if user_input == 'exit':
            break
        elif not user_input.isdigit() or int(user_input) not in range(1, len(names) + 1):
            print("Некоректний ввід. Спробуйте ще раз.")
        else:
            idx = int(user_input) - 1
            cat_name = names[idx]
            print(f"Ви обрали кота з ім'ям '{cat_name}'.")
            for cat in db.cats.find({'name': cat_name}):
                print(f"🐱Назва - {cat['name']}\n🔆Вік - {cat['age']}\n✅Особливості - {cat['features']}")


def update_info_about_cat(db):
    result = db.cats.find({}, {"_id": 0, "name": 1})
    names = [doc["name"] for doc in result]
    print(f"{Fore.LIGHTCYAN_EX}🗂 Всі імена котів у колекції [{db.name}]: {Style.RESET_ALL}")
    for idx, el in enumerate(names):
        print(f"\t----> [{idx + 1}] {el}")

    while True:
        user_input = input(
            f"Оберіть номер кота, вік якого хочете оновити {[num + 1 for num, name in enumerate(names)]} або "
            f"напишіть 'exit', щоб вийти: ")
        if user_input == 'exit':
            break
        elif not user_input.isdigit() or int(user_input) not in range(1, len(names) + 1):
            print("Некоректний ввід. Спробуйте ще раз.")
        else:
            idx = int(user_input) - 1
            cat_name = names[idx]
            print(f"Ви обрали кота з ім'ям '{cat_name}'.")
            for cat in db.cats.find({'name': cat_name}):
                print(f"🔆Вік - {cat['age']}")
            user_input = int(input(f"Введіть оновлений вік для кота {cat_name}\n>>> "))
            db.cats.update_one({"name": cat_name}, {"$set": {"age": str(user_input)}})
            result = db.cats.find_one({"name": cat_name})
            print(f"Дані оновлено >>> ---- ", result)


def update_features_of_cat(db):
    result = db.cats.find({}, {"_id": 0, "name": 1})
    names = [doc["name"] for doc in result]
    print(f"{Fore.LIGHTCYAN_EX}🗂 Всі імена котів у колекції [{db.name}]: {Style.RESET_ALL}")
    for idx, el in enumerate(names):
        print(f"\t----> [{idx + 1}] {el}")

    while True:
        user_input = input(
            f"Оберіть номер кота, якому хочете додати ще одну особливість {[num + 1 for num, name in enumerate(names)]} або "
            f"напишіть 'exit', щоб вийти: ")
        if user_input == 'exit':
            break
        elif not user_input.isdigit() or int(user_input) not in range(1, len(names) + 1):
            print("Некоректний ввід. Спробуйте ще раз.")
        else:
            idx = int(user_input) - 1
            cat_name = names[idx]
            print(f"Ви обрали кота з ім'ям '{cat_name}'.")
            cat = db.cats.find_one({'name': cat_name})
            if cat:
                print(f"🔆 Особливості - {cat['features']}")
                new_feature = input(f"Додайте ще одну особливіть коту {cat_name} або напишіть 'exit', щоб вийти: ")
                if new_feature == 'exit':
                    break
                elif new_feature.strip():  # Перевірка на те, що рядок не є порожнім
                    new_features = cat.get('features',
                                           [])  # Отримання поточного списку особливостей або створення нового
                    new_features.append(new_feature)
                    db.cats.update_one({"name": cat_name}, {"$set": {"features": new_features}})
                    print("Особливість успішно додана.")
                else:
                    print("Ви не ввели жодної особливості.")
            else:
                print(f"Кот з ім'ям '{cat_name}' не знайдений.")


def delete_doc_by_name_of_cat(db):
    result = db.cats.find({}, {"_id": 0, "name": 1})
    names = [doc["name"] for doc in result]
    print(f"{Fore.LIGHTCYAN_EX}🗂 Всі імена котів у колекції [{db.name}]: {Style.RESET_ALL}")
    for idx, el in enumerate(names):
        print(f"\t----> [{idx + 1}] {el}")

    while True:
        user_input = input(
            f"Оберіть номер кота, якого хочете видалити{[num + 1 for num, name in enumerate(names)]} або "
            f"напишіть 'exit', щоб вийти: ")
        if user_input == 'exit':
            break
        elif not user_input.isdigit() or int(user_input) not in range(1, len(names) + 1):
            print("Некоректний ввід. Спробуйте ще раз.")
        else:
            idx = int(user_input) - 1
            cat_name = names[idx]
            print(f"Ви обрали кота з ім'ям '{cat_name}'.")
            cat = db.cats.find_one({'name': cat_name})
            if cat:
                db.cats.delete_one({"name": cat_name})
                print(f"Kота з імене {cat_name} було видалено.")
            else:
                print(f"Кот з ім'ям '{cat_name}' не знайдений.")


def delete_all_docs(db):
    result = db.cats.find({}, {"_id": 0, "name": 1})
    names = [doc["name"] for doc in result]
    print(f"{Fore.LIGHTCYAN_EX}🗂 Всі імена котів у колекції [{db.name}]: {Style.RESET_ALL}")
    for idx, el in enumerate(names):
        print(f"\t----> [{idx + 1}] {el}")

    print("Процес видалення всіх документів у колекції")

    confirmation = input("Ви впевнені, що бажаєте видалити всі документи? (yes/no): ")
    if confirmation.lower() == "yes":
        db.cats.delete_many({})
        print("Всі документи успішно видалено.")
    else:
        print("Скасовано.")


while True:
    user_input = input("\nОберіть дію:\n"
                       "1. Виведення всіх записів із колекції\n"
                       "2. Виведенння інформації про кота за введеним іменем\n"
                       "3. Оновлення віку кота за ім'ям\n"
                       "4. Додавання нової характеристики до списку features кота за ім'ям\n"
                       "5. Видалення запису з колекції за ім'ям тварини\n"

                       "6. Видалення всіх записів із колекції\n"
                       "7. Завершити роботу\n"
                       "8. Заповнення колекції даними\n"
                       ">>> ")
    if user_input not in ["1", "2", "3", "4", "5", "6", "7", "8"]:
        print("Такої опції, на жаль, немає. Спробуйте ще раз.")

    elif user_input == "7":
        print("Робота завершена.")
        exit()
    elif user_input == "1":
        reading(db)
    elif user_input == "2":
        find_info_about_cat(db)
    elif user_input == "3":
        update_info_about_cat(db)
    elif user_input == "4":
        update_features_of_cat(db)
    elif user_input == "5":
        delete_doc_by_name_of_cat(db)
    elif user_input == "6":
        delete_all_docs(db)
    elif user_input == "8":
        insert_data_to_db(db)


