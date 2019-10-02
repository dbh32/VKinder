import unittest
from unittest.mock import patch
import main
import random, string
from tests.data.cases import User, user_info


def random_word(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class TestMain(unittest.TestCase):

    @unittest.expectedFailure
    @patch('builtins.input')
    def test_login(self, mock_input):
        # Вводим только один параметр, хотя нужна пара - логин и пароль
        mock_input.side_effect = [random_word(10)]
        with unittest.mock.patch('builtins.input', mock_input):
            main.login()

    def test_check_text_fields(self):
        # Сравнение текстовых полей
        user_1 = User()
        user_2 = user_info
        # Есть совпадения
        self.assertTrue(main.check_text_fields(user_1, user_2, 'music') == 1)
        # Нет совпадений
        self.assertTrue(main.check_text_fields(user_1, user_2, 'interests') == 0)


if __name__ == '__main__':
    unittest.main()
