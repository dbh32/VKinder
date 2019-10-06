import unittest
from unittest.mock import patch
import main
import random
import string
import json
from classes.Users import User

credentials = {}
music = {}


def setUpModule():
    with open('fixtures/credentials.json', 'r', encoding='utf-8-sig') as dirs:
        credentials.update(json.load(dirs))
    with open('fixtures/music.json', 'r', encoding='utf-8-sig') as dirs:
        music.update(json.load(dirs))


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class TestMain(unittest.TestCase):

    @classmethod
    @patch('builtins.input')
    def setUpClass(self, mock_input):
        # Логиним пользователя перед выполнением тестов
        mock_input.side_effect = [random_word(8), random_word(8), random_word(8), random_word(8), random_word(8)]
        with unittest.mock.patch('builtins.input', mock_input):
            self.user = User(credentials['login'], credentials['password'])

    def test_user_initial(self):
        # Проверяем, что инициализация прошла успешно и данные по пользователю записались
        self.assertIsNotNone(self.user.info)

    def test_getting_profile_pics(self):
        uid = self.user.info['id']
        result = self.user.get_profile_pics(uid)
        # Проверяем получение фотографий по ID пользователя
        self.assertIsNotNone(result)

    @patch('builtins.input')
    def test_users_search(self, mock_input):
        # Тестируем сразу и обращение к API и работу кэша
        # При инициализации пользователя у нас только одна запись в кэше
        self.assertTrue(len(self.user.previous_search_params) == 1)
        mock_input.side_effect = ['1', '18', '24']
        with unittest.mock.patch('builtins.input', mock_input):
            self.user.search_users()
        # После успешного обращения к API должно стать две записи в кэше
        self.assertTrue(len(self.user.previous_search_params) == 2)

    @unittest.expectedFailure
    @patch('builtins.input')
    def test_login_inconsistent_data(self, mock_input):
        # Вводим только один параметр, хотя нужна пара - логин и пароль
        mock_input.side_effect = [random_word(8)]
        with unittest.mock.patch('builtins.input', mock_input):
            main.login()

    def test_check_text_fields(self):
        # Проверяем работу функции сравнения текстовых полей
        # Разные поля
        self.assertTrue(main.check_text_fields(self.user, music, 'music') == 0)
        # Одинаковые поля
        self.assertTrue(main.check_text_fields(self.user, self.user.info, 'music') == 1)


if __name__ == '__main__':
    unittest.main()
