from classes.Users import User
from classes.MongoDB import MongoDB
from ratings import ratings
from pprint import pprint


# Получаем и сразу обрабатываем результаты поиска.
def get_list_of_search_results(app_user):
    users_list = []

    for each_user in app_user.search_users()['items']:
        user_info = {}
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
        for i in ['common_count', 'relation', 'home_town', 'interests', 'music', 'books']:
            try:
                # Общие друзья и статус "в активном поиске"
                if i == 'common_count' and user_info[i] == 1:
                    user_score += ratings['friends']
                if i == 'relation' and user_info[i] == 6:
                    user_score += ratings['active_search_status']
                # Поля, требующие сравнения по тексту
                if check_text_fields(app_user, user_info, i) == 1:
                    user_score += ratings[i]
                # Проверяем нет ли общих групп...
                if set(app_user.info['groups']['items']).isdisjoint(set(app_user.get_groups(user_info['id'])['items'])):
                    user_info.update({'common_groups': 0})
                else:
                    # ...если есть, то записываем и поднимаем рейтинг
                    user_info.update({'common_groups': 1})
                    user_score += ratings['groups']
            except KeyError:
                pass

        # Добавляем рейтинг в сохраняемые данные
        user_info.update({'user_score': user_score})
        # Добавляем всю инфу о пользователе в общий список
        users_list.append(user_info)

    return users_list


def check_text_fields(app_user, user_info, field):
    # Сравниваем текстовые поля (музыка, книги, интересы)
    x = (app_user.info[field].replace('"', '')).split(',')
    y = (user_info[field].replace('"', '')).split(',')
    if set(x).isdisjoint(set(y)):
        return 0
    else:
        return 1


def get_top10_users_avatars(user, db, collection):
    # Получаем аватарки для наших топ-10
    data = []
    try:
        for uid in db.mongo_get_top10_list(collection):
            data.append({'id': uid,
                         'photos': format_photos_dict(user.get_profile_pics(uid)['items'])})
    except:
        # Если профиль закрыт, к сожалению, ничего не получим
        pass

    return data


def format_photos_dict(photos):
    # Чистим результаты получения фотографий от мусора
    photos_list = []
    likes = []

    for photo in photos:
        # Собираем информацию о количестве лайков
        likes.append(photo['likes']['count'])

    likes_sorted = sort_list(likes)

    for photo in photos:
        # Записываем только топ-3 результата
        if photo['likes']['count'] in likes_sorted[0:3]:
            element = {'likes': photo['likes']['count'], 'url': format_url(photo['sizes'])}
            photos_list.append(element)

    print(photos_list)
    return photos_list


def sort_list(likes):
    return sorted(likes, reverse=True)


def format_url(sizes):
    # Получаем фото только в приемлимом размере
    for photo_info in sizes:
        if photo_info['type'] == 'x':
            return photo_info['url']


if __name__ == '__main__':
    print('______________________________________________________\n'
          '|##  найди  #####################  бесплатно  #######|\n'
          '|#####  себе  ######  *VKINDER*  #######  жми  ######|\n'
          '|##########  пару  #####################  без смс  ##|\n')

    # VK login (or email/phone), password
    login = input('VK Login (email/phone): ')
    password = input('Password: ')
    print('\nПроверяем информацию о пользователе...\n')
    vasya = User(login, password)
    # vasya = User()

    # db, address, port
    vkinder = MongoDB()

    # временный "интерфейс"
    while True:
        print('$$$$$$$$$$$$$$$$$$ COMMANDS $$$$$$$$$$$$$$$$$$$\n'
              '1 - Показать содержимое коллекции в Mongo\n'
              '2 - Дропнуть коллекцию в Mongo\n'
              '3 - Выполнить поиск людей и записать результаты в БД\n'
              '4 - Сохранить в отдельную коллекцию топ-3 аватаров людей из топ-10\n'
              '9 - Посмотреть кэш поиска на текущий момент\n'
              'q - Выход\n'
              '$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$$\n')
        command = input('Комманда: ')
        print('')
        if command == '1':
            vkinder.mongo_show_collection(vkinder.users_collection)
        elif command == '2':
            vkinder.mongo_drop_collection(vkinder.db, vkinder.users_collection)
            vkinder.mongo_drop_collection(vkinder.db, vkinder.top10_collection)
        elif command == '3':
            vkinder.mongo_insert_many(get_list_of_search_results(vasya), vkinder.users_collection)
        elif command == '4':
            vkinder.mongo_insert_many(get_top10_users_avatars(vasya, vkinder, vkinder.users_collection),
                                      vkinder.top10_collection)
        elif command == '9':
            pprint(vasya.previous_search_params)
            print('')
        elif command == 'q':
            print('До скорого!')
            break
