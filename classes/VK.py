import vk_api


class VK:

    def __init__(self, login, password):
        self.vk = self.vk_auth(login, password)

    def vk_auth(self, login, password):
        # Получаем сессию для работы с VK API
        vk_session = vk_api.VkApi(login, password)
        try:
            vk_session.auth(token_only=True)
        except vk_api.AuthError as error_msg:
            print(error_msg)
            return
        vk = vk_session.get_api()
        return vk
