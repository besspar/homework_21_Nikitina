from abc import ABC, abstractmethod


class Storage(ABC):
    def __init__(self, items, capacity):
        self.items = items
        self.capacity = capacity

    @abstractmethod
    def add(self, product, amount):
        pass

    @abstractmethod
    def remove(self, product, amount):
        pass

    @abstractmethod
    def get_free_space(self):
        pass

    @abstractmethod
    def get_items(self):
        pass

    @abstractmethod
    def unit_items_count(self):
        pass


class Store(Storage):
    def __init__(self, name, items={}, capacity=100):
        super().__init__(items, capacity)
        self.__name = name

    @property
    def name(self):
        return self.__name

    def add(self, product, amount):
        """ Функция добавления товара в склад """
        if self.get_free_space() > 0:
            if self.items.get(product) is None:
                self.items[product] = amount
            else:
                self.items[product] += amount
            print(f'Курьер доставил {amount} {product} на {self.name}')
        else:
            print(f'В {self.name} недостаточно места, попробуйте что-то другое')

    def remove(self, product, amount):
        """Функция удаления товара со склада"""
        if self.items.get(product) is None:
            print(f'В {self.name} нет {product}\nПопробуйте запросить что-то другое')
        elif self.items[product] < amount:
            print(f'В {self.name} нет столько {product}')
        else:
            self.items[product] -= amount
            print(f'Курьер забрал {amount} {product} со {self.name}а')
            if self.items[product] == 0:
                del self.items[product]


    def get_free_space(self):
        """ Функция возвращает свободное место на складе"""
        space_in_work = 0
        if len(self.items):
            for amount in self.items.values():
                space_in_work += amount
        return self.capacity - space_in_work

    def get_items(self):
        """ Функция возвращает тип и количество товара, которое хранится на складе"""
        if self.get_free_space() < self.capacity:
            print(f'\nВ {self.name} хранится:')
            for item, amount in self.items.items():
                print(f"{amount:5} {item}")
        else:
            print(f'\nВ {self.name} ничего нет')

    def unit_items_count(self):
        """ Функция возвращает виды товара на складе"""
        if self.get_free_space() < self.capacity:
            answer = []
            for item in self.items.keys():
                answer.append(item)
            print(f'\nВ {self.name} хранится: {", ".join(answer)}')
        else:
            print(f'\nВ {self.name} ничего нет')


class Shop(Store):
    def __init__(self, name, items={}, capacity=20):
        super().__init__(name, items, capacity)
        self.__name = name

    def add(self, product, amount):
        """ Функция добавления товара в склад """
        if self.get_free_space() > 0:
            if len(self.items) < 5:
                if self.items.get(product) is None:
                    self.items[product] = amount
                else:
                    self.items[product] += amount
                print(f'Курьер доставил {amount} {product} в {self.name}')
            else:
                print(f'В {self.name} уже слишком много типов товара, попробуйте что-то отгрузить')
        else:
            print(f'В {self.name} недостаточно места, попробуйте что-то другое')

    def remove(self, product, amount):
        """Функция удаления товара из магазина"""
        if self.items.get(product) is None:
            print(f'В {self.name} нет {product}\nПопробуйте запросить что-то другое')
        elif self.items[product] < amount:
            print(f'В {self.name} нет столько {product}')
        else:
            self.items[product] -= amount
            print(f'Курьер забрал {amount} {product} из {self.name}а')
            if self.items[product] == 0:
                del self.items[product]


class Request:
    def __init__(self, request_string):
        data = request_string.split()
        self.amount = int(data[1])
        self.whereabout = data[4]  # instead of attribute "from"
        if data[4] == 'склад':
            self.whereabout = storage
        if data[4] == 'магазин':
            self.whereabout = shop
        self.product = data[2]
        self.to = data[-1]
        if data[-1] == 'склад':
            self.to = storage
        if data[-1] == 'магазин':
            self.to = shop


# в задании было написано функцию main сделать, а потом ее вызывать(?)
# но я предположила, что имелось в виду это
if __name__ == '__main__':
    storage = Store(items={}, capacity=100, name='склад')
    shop = Shop(items={}, capacity=20, name='магазин')

    # Начально наполнение склада
    storage.add('печеньки', 10)
    storage.add('молоко', 10)
    storage.add('конфеты', 10)
    storage.add('хлеб', 10)
    storage.add('вафли', 10)
    storage.add('мороженое', 10)

    # Первое сообщение: как много товара в магазине, на складе
    storage.get_items()
    shop.get_items()
    print('\n')

    # Цикл запросов до стоп-слова
    user_request = ''
    stop_word = 'стоп'

    while user_request != stop_word:
        print("\nФормат задания на перемещение: Доставить 3 печеньки из склад в магазин")
        print("Доступные команды: Товар на складе | Товар в магазине\n")

        user_request = input("\033[31m{}\033[0m".format("Введите задание на перемещение или команду запроса: "))

        if user_request == stop_word:
            break
        else:
            if "Товар на складе".lower() in user_request.lower():
                storage.get_items()
            elif "Товар в магазине".lower() in user_request.lower():
                shop.get_items()
            elif ("Товар на складе".lower() and "Товар в магазине".lower() and "Доставить") not in user_request:
                print("\033[34m{}\033[0m".format("Попробуйте другой запрос"))
            else:
                request = Request(request_string=user_request)

                # Перемещение продуктов
                # Сначала проверяем, есть ли свободное место в месте получения
                # Затем проверяем, не магазин ли получатель и нет ли там уже 5 товаров
                # (потому что для магазина особые условия)
                # После этого проверяем, достаточно ли товара в месте отправления
                # Осуществляем транспортировку

                if request.to.get_free_space() - request.amount < 0:
                    print(f"В {request.to.name} недостаточно места для доставки товара")
                elif request.to == shop and len(request.to.items) == 5:
                    print(f"В {request.to.name} слишком много типов товаров, попробуйте что-то отгрузить")
                elif request.whereabout.items[request.product] < request.amount:
                    print(f"В {request.whereabout.name} недостаточно {request.product}")
                else:
                    request.whereabout.remove(request.product, request.amount)
                    print(f"Курьер везет {request.amount} {request.product} от {request.whereabout.name}а до {request.to.name}а")
                    request.to.add(request.product, request.amount)


                if 'склад' in user_request:
                    storage.get_items()
                if 'магазин' in user_request:
                    shop.get_items()


