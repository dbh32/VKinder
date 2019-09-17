from classes.VK import VK
# from datetime import datetime, date, timedelta


class User(VK):

    def __init__(self, login='+79104405298', password='neroguespwn%imba555'):
        VK.__init__(self, login, password)
        self.info = self.get_info()
        # self.age = (date.today() - datetime.strptime(self.info['bdate'], '%d.%m.%Y').date()) \
        #            // timedelta(days=365.2425)

    def get_groups(self):
        return self.vk.groups.get()

    def get_friends(self):
        return self.vk.friends.get()

    def get_info(self):
        params = 'sex, relation, bdate, home_town, interests, music, books'
        for data in self.vk.users.get(fields=params):

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

            data.update({'groups': self.get_groups()})
            data.update({'friends': self.get_friends()})

            return data
