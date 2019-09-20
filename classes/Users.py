from classes.VK import VK


# from datetime import datetime, date, timedelta


class User(VK):

    # VK login (or email/phone), password
    def __init__(self, login='', password=''):
        VK.__init__(self, login, password)
        self.info = self.get_info()

    #     self.age = self.get_age()
    #
    # def get_age(self):
    #     bdate_as_date = datetime.strptime(self.info['bdate'], '%d.%m.%Y').date()
    #     age = (date.today() - bdate_as_date) // timedelta(days=365.2425)
    #     return age

    def get_groups(self, uid):
        # Получаем список групп для пользователя с id=uid
        print('@')
        try:
            return self.vk.groups.get(user_id=uid)
        except:
            # Заглушка на случай закрытого профиля
            return {'count': 0, 'items': []}

    def get_info(self):
        # Собираем информацию о пользователе, для которого запускается сервис
        # Если соответствующие поля заполнены, то пишем ОК
        # Если нет - спрашиваем
        fields = 'sex, bdate, home_town, interests, music, books'
        for data in self.vk.users.get(fields=fields):

            if 'bdate' not in data.keys():
                bdate = input('Укажите дату и год рождения (dd.mm.yyyy): ')
                data.update({'bdate': bdate})
                print('Дата рождения -- ОК\n')
                pass
            else:
                print('Дата рождения -- ОК\n')
                pass

            if len(data['home_town']) == 0:
                home_town = input('Укажите Ваш город: ')
                data.update({'home_town': home_town})
                print('Город -- ОК\n')
                pass
            else:
                print('Город -- ОК\n')
                pass

            if len(data['music']) == 0:
                music = input('Любимые музыкальные группы: ')
                data.update({'music': music})
                print('Музыка -- ОК\n')
                pass
            else:
                print('Музыка -- ОК\n')
                pass

            if len(data['books']) == 0:
                books = input('Любимые книги: ')
                data.update({'books': books})
                print('Книги -- ОК\n')
                pass
            else:
                print('Книги -- ОК\n')
                pass

            if len(data['interests']) == 0:
                interests = input('Чем увлекаетесь: ')
                data.update({'interests': interests})
                print('Интересы -- ОК\n')
                pass
            else:
                print('Интересы -- ОК\n')
                pass

            # Добавляем информацию о группах
            data.update({'groups': self.get_groups(data['id'])})

            # Убираем ненужные поля
            data.pop('is_closed')
            data.pop('can_access_closed')

            return data

    def search_users(self):
        # Поиск людей по критериям
        print('Пол')
        print('"1" - жен, "2" - муж, "0" - всё равно')
        sex = int(input('Кого ищём? '))

        print('\nТеперь возраст')
        age_from = int(input('От: '))
        age_to = int(input('До: '))

        fields = 'home_town, common_count, interests, music, books, sex, relation, bdate'

        # Значение home_town подставляется из информации о нашем пользователе
        # Если в итоге пусто, то так и будем искать
        return self.vk.users.search(
            count=100, fields=fields, sex=sex, hometown=self.info['home_town'], age_from=age_from, age_to=age_to
        )
