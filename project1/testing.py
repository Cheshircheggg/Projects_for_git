from typing import List, Optional


class Record:

    """Класс для хранения информации о записи."""

    def __init__(self, date: str, category: str, amount: float, description: str) -> None:
        self.date = date
        self.category = category
        self.amount = amount
        self.description = description

    def get_date(self) -> str:
        return self.date

    def get_category(self) -> str:
        return self.category

    def get_amount(self) -> float:
        return self.amount

    def get_description(self) -> str:
        return self.description


class RecordManager:

    """Класс для управления иформацией в записи."""

    def __init__(self, filename: str) -> None:
        self.filename = filename
        self.records = []
        self.load_records()

    def load_records(self) -> None:

        """Функция предоставления иформации в записи."""

        try:
            with open(self.filename, "r") as f:
                lines = f.read().split("\n\n")  # Разделяем записи по двойному переносу строки
                for line in lines:
                    data = line.strip().split('\n')
                    if len(data) >= 4:
                        date = data[0].split(': ')[1].strip()
                        category = data[1].split(': ')[1].strip()
                        amount = float(data[2].split(': ')[1].strip())
                        description = data[3].split(': ')[1].strip()
                        self.records.append(Record(date, category, amount, description))
        except FileNotFoundError:
            print("Файл не найден. Создан новый файл records.txt.")

    def save_records(self) -> None:

        """Функция сохранения записи."""

        with open(self.filename, "w") as f:
            for record in self.records:
                f.write("Дата: {}\n".format(record.get_date()))
                f.write("Категория: {}\n".format(record.get_category()))
                f.write("Сумма: {}\n".format(record.get_amount()))
                f.write("Описание: {}\n\n".format(record.get_description()))

    def search_records(self, category: Optional[str] = None, date: Optional[str] = None, amount: Optional[float] = None)-> List[Record]:

        """Функция поиска по записям."""

        results: List[Record] = []
        for record in self.records:
            if (not category or record.get_category() == category) and (not date or record.get_date() == date) and (
                    not amount or record.get_amount() == amount):
                results.append(record)
        return results

    def calculate_total_balance(self) -> float:

        """Функция вычисления баланса."""

        total_income = sum(record.get_amount() for record in self.records if record.get_category() == 'Доход')
        total_expense = sum(record.get_amount() for record in self.records if record.get_category() == 'Расход')
        total_balance = total_income - total_expense
        return total_balance


if __name__ == "__main__":

    filename = "./records.txt"
    record_manager = RecordManager(filename)

    while True:
        print("1. Вывод баланса")
        print("2. Добавление записи")
        print("3. Редактирование записи")
        print("4. Поиск по записям")

        choice = input("Выберите действие: ")

        if choice == "1":
            total_balance = record_manager.calculate_total_balance()
            print(f"Общий баланс: {total_balance}")

        elif choice == "2":
            date = input("Введите дату (дд-мм-гггг): ")
            category = input("Введите категорию (Доход/Расход): ")
            amount = float(input("Введите сумму: "))
            description = input("Введите описание: ")
            new_record = Record(date, category, amount, description)
            record_manager.records.append(new_record)
            record_manager.save_records()

        elif choice == "3":

            record_id = int(input("Введите номер записи для редактирования: "))

            if record_id - 1 < len(record_manager.records):
                record = record_manager.records[record_id - 1]

                print("Выберите поле для редактирования:")
                print("1. Дата (текущая: {})".format(record.date))
                print("2. Категория (текущая: {})".format(record.category))
                print("3. Сумма (текущая: {})".format(record.amount))
                print("4. Описание (текущее: {})".format(record.description))

                field_choice = input("Введите номер поля для редактирования: ")

                if field_choice == "1":
                    date = input("Введите новую дату (дд-мм-гггг): ")
                    if date:
                        record.date = date
                elif field_choice == "2":
                    category = input("Введите новую категорию (Доход/Расход): ")
                    if category:
                        record.category = category
                elif field_choice == "3":
                    amount = input("Введите новую сумму: ")
                    if amount:
                        record.amount = float(amount)
                elif field_choice == "4":
                    description = input("Введите новое описание: ")
                    if description:
                        record.description = description

                record_manager.save_records()

            else:
                print("Ошибка: Записи под таким номером {} не существует. Пожалуйста, выберите другое значение.".format(record_id))

        elif choice == "4":

            while True:

                print("Выберите критерий поиска:")
                print("1. По категории (Доход/Расход)")
                print("2. По дате")
                print("3. По сумме")
                search_criteria = input("Введите номер критерия поиска: ")

                if search_criteria == "1":
                    search_category = input("Введите категорию для поиска (Доход/Расход): ")
                    search_result = record_manager.search_records(category=search_category)
                    break

                elif search_criteria == "2":
                    search_date = input("Введите дату для поиска (дд-мм-гггг): ")
                    search_result = record_manager.search_records(date=search_date)
                    break

                elif search_criteria == "3":
                    search_amount = float(input("Введите сумму для поиска: "))
                    search_result = record_manager.search_records(amount=search_amount)
                    break

                else:
                    print("Некорректный номер критерия. Пожалуйста, выберите снова.")

            if search_result:
                for record in search_result:
                    print(
                        f"Дата (дд-мм-гггг): {record.date}\nКатегория: {record.category}\nСумма: {record.amount}\nОписание: {record.description}\n"
                    )

            else:
                print("Записи по указанным критериям не найдены")

        else:
            print("Некорректный выбор. Попробуйте снова.")
