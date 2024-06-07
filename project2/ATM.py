class ATM:
    """
    Класс ATM, представляющий банкомат, который может принимать и выдавать деньги.

    Атрибуты:
    banknotes (List[int]): Список, хранящий количество банкнот каждого номинала (10, 50, 100, 200, 500 рублей).
    """
    def __init__(self):
        self.banknotes = [0] * 5  # Хранение количества банкнот [10, 50, 100, 200, 500]

    def deposit(self, banknotesCount):
        """
        :type banknotesCount: List[int]
        :rtype: None
        (Вносит новые банкноты в банкомат)
        """
        for count in banknotesCount:
            if count < 0:
                raise ValueError("Количество банкнот не может быть отрицательным")
        for i in range(5):
            self.banknotes[i] += banknotesCount[i]

    def withdraw(self, amount):
        """
        :type amount: int
        :rtype: List[int]
        (Выдает указанную сумму денег из банкомата, используя банкноты наибольшего номинала)
        """
        if amount < 1:
            raise ValueError("Сумма для снятия должна быть больше 0")

        result = [0] * 5
        denominations = [10, 50, 100, 200, 500]
        for i in range(4, -1, -1):
            count = min(amount // denominations[i], self.banknotes[i])
            result[i] = count
            amount -= count * denominations[i]
        if amount > 0:
            return [-1]

        for i in range(5):
            self.banknotes[i] -= result[i]
        return result


def main():
    obj = ATM()
    obj.deposit([0, 0, 1, 2, 1])
    print(obj.withdraw(600))
    obj.deposit([0, 1, 0, 1, 1])
    print(obj.withdraw(600))
    print(obj.withdraw(550))


if __name__ == "__main__":
    main()
