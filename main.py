from classes.Users import User
from classes.MongoDB import MongoDB


# Веса:
# общие друзья (19)
# один родной город (16)
# общие группы (15)
# статус "в активном поиске" (14)
# музыка (13)
# книги (12)
# интересы (11)


# Получаем и сразу обрабатываем результаты поиска.
def get_list_of_search_results(app_user, collection):
    users_list = []

    for each_user in app_user.search_users()['items']:
        user_info = {}
        # Старуем с 16, тк в диапазон возраста в любом случае попадаем
        user_score = 0

        # Собираем только те данные, которые нужны
        for i in ['id', 'first_name', 'last_name', 'home_town',
                  'common_count', 'interests', 'music',
                  'books', 'sex', 'relation', 'bdate']:
            try:
                user_info.update({i: each_user[i]})
            except KeyError:
                pass

        # Сразу считаем рейтинг найденного человека
        try:
            if user_info['common_count'] == 1:
                user_score += 19
            if user_info['relation'] == 6:
                user_score += 14
            if check_text_fields(app_user, user_info, 'home_town') == 1:
                user_score += 16
            if check_text_fields(app_user, user_info, 'music') == 1:
                user_score += 13
            if check_text_fields(app_user, user_info, 'books') == 1:
                user_score += 12
            if check_text_fields(app_user, user_info, 'interests') == 1:
                user_score += 11
            # Проверяем нет ли общих групп...
            if set(app_user.info['groups']['items']).isdisjoint(set(app_user.get_groups(user_info['id'])['items'])):
                user_info.update({'common_groups': 0})
            else:
                # ...если есть, то записываем и поднимаем рейтинг
                user_info.update({'common_groups': 1})
                user_score += 15
        except KeyError:
            pass

        # Добавляем рейтинг в сохраняемые данные
        user_info.update({'user_score': user_score})
        # Добавляем всю инфу о пользователе в общий список
        users_list.append(user_info)

    # Записываем все данные в БД
    # Пока в отдельном цикле (потом может что-то поменяю)
    for each_user in users_list:
        collection.insert_many([each_user])

    print('Всё! Беги смотреть в БД\n')
    # return users_list


def check_text_fields(app_user, user_info, field):
    x = (app_user.info[field].replace('"', '')).split(',')
    y = (user_info[field].replace('"', '')).split(',')
    if set(x).isdisjoint(set(y)):
        return 0
    else:
        return 1



if __name__ == '__main__':
    print('______________________________________________________')
    print('|##  найди  #####################  бесплатно  #######|')
    print('|#####  себе  ######  *VKINDER*  #######  жми  ######|')
    print('|##########  пару  #####################  без смс  ##|\n')

    # VK login (or email/phone), password
    login = input('VK Login (email/phone): ')
    password = input('Password: ')
    print('\nПроверяем информацию о пользователе...\n')
    vasya = User(login, password)

    # db, address, port
    vkinder = MongoDB()

    # временный "интерфейс"
    while True:
        print('$$$$$$$$$$$$$$$$$$ COMMANDS $$$$$$$$$$$$$$$$$$$\n'
              '1 - Показать содержимое коллекции в Mongo\n'
              '2 - Дропнуть коллекцию в Mongo\n'
              '3 - Наполнить коллекцию результатами поиска\n'
              '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
        command = input('Комманда: ')
        print('')
        if command == '1':
            vkinder.mongo_show_users_collection()
        elif command == '2':
            vkinder.mongo_drop_users_collection()
        elif command == '3':
            get_list_of_search_results(vasya, vkinder.users_collection)
        elif command == 'q':
            break
