from classes.VK import VK


class User(VK):

    # VK login (or email/phone), password
    def __init__(self, login='', password=''):
        VK.__init__(self, login, password)
        self.info = self.get_info()
        # Кэш поиска
        self.previous_search_params = {0: {
            'sex': 0,
            'age_from': 0,
            'age_to': 0,
            'counter': 0
        }}
        # Переменная для реализации кэша поиска
        self.cash = 0

    def get_groups(self, uid):
        # Получаем список групп для пользователя с id=uid
        print('@')
        try:
            return self.vk.groups.get(user_id=uid)
        except KeyError:
            # Заглушка на случай закрытого профиля
            return {'count': 0, 'items': []}

    def get_info(self):
        # Собираем информацию о пользователе, для которого запускается сервис
        fields = 'sex, bdate, home_town, interests, music, books'
        for data in self.vk.users.get(fields=fields):
            # print(self.vk.users.get(fields=fields))
            self.check_data(data)
            # Добавляем информацию о группах
            data.update({'groups': self.get_groups(data['id'])})

            # Убираем ненужные поля
            data.pop('is_closed')
            data.pop('can_access_closed')

            return data

    def check_data(self, data):
        # Если соответствующие поля заполнены - пишем ОК
        # Если нет - спрашиваем
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

        return data

    def search_users(self):
        # Поиск людей по критериям
        fields = 'home_town, common_count, interests, music, books, sex, relation, bdate'

        print('Пол')
        print('"1" - жен, "2" - муж, "0" - всё равно')
        sex = int(input('Кого ищём? '))

        print('\nТеперь возраст')
        age_from = int(input('От: '))
        age_to = int(input('До: '))

        # Используется для сравнения параметров с кэшем
        params = {
            'sex': sex,
            'age_from': age_from,
            'age_to': age_to,
        }

        # Чтобы кэш не перезаписывал сам себя
        self.cash += 1

        # Если такие параметры уже использовались ранее, то ищем с оффсетом
        if self.compare_params(params) != 0:
            print('\nЕсть запись в кэше. Запрашиваем больше результатов...')

            item = self.compare_params(params)

            # Количество поисков по данным параметрам
            # Он же множитель для ключа offset
            new_counter = self.previous_search_params[item]['counter'] + 1

            self.previous_search_params[item].update({'counter': new_counter})

            # Поиск по параметрам с добавлением offset-а
            search_results = self.vk.users.search(
                offset=new_counter * 20, count=20, fields=fields,
                sex=sex, hometown=self.info['home_town'], age_from=age_from, age_to=age_to
            )
            return search_results

        # Если параметры не использовались, то сохраняем их в кэш и ищем без оффсета
        elif self.compare_params(params) == 0:
            print('\nЧто-то новенькое...')

            new_counter = 0

            # Делаем новую запись в кэш
            self.previous_search_params.update({self.cash: params})
            self.previous_search_params[self.cash].update({'counter': new_counter})

            search_results = self.vk.users.search(
                count=20, fields=fields,
                sex=sex, hometown=self.info['home_town'], age_from=age_from, age_to=age_to
            )
            return search_results

    def compare_params(self, params):
        # Сравниваем последние переданные параметры с кэшем
        for k, v in self.previous_search_params.items():
            if v['sex'] == params['sex'] \
                    and v['age_from'] == params['age_from'] \
                    and v['age_to'] == params['age_to']:
                return k
        return 0

    def get_profile_pics(self, uid):
        # Получаем фото пользователя
        try:
            print('@')
            return self.vk.photos.get(owner_id=uid, album_id='profile', extended=1)
        # Чтобы не было ошибки при закрытом профиле
        except KeyError:
            pass
