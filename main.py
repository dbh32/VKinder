from classes.Users import User
from classes.MongoDB import MongoDB


def save_user_info_to_db(user, mongo_collection):
    users_list = []
    for data in [user.info]:
        user = {
            'id': data['id'],
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'sex': data['sex'],
            'bdate': data['bdate'],
            'home_town': data['home_town'],
            'relation': data['relation'],
            'interests': data['interests'],
            'music': data['music'],
            'books': data['books'],
            'groups': data['groups'],
            'friends': data['friends']
        }
        users_list.append(user)
    result = mongo_collection.insert_many(users_list)
    return result


if __name__ == '__main__':

    app_user = User()
    vkinder = MongoDB()

    # временный "интерфейс"
    while True:
        print('1 - Показать содержимое коллекции в Mongo\n'
              '2 - Дропнуть коллекцию в Mongo\n'
              '3 - Наполнить коллекцию данными о пользователе\n')
        command = input('Комманда: ')
        print('')
        if command == '1':
            vkinder.mongo_show_users_collection()
        elif command == '2':
            vkinder.mongo_drop_users_collection()
        elif command == '3':
            save_user_info_to_db(app_user, vkinder.users_collection)
        elif command == 'q':
            break
