import json
import requests
import urllib


class UbiPlacesBot():

    TOKEN = "663551182:AAGECxo5uVIDF_Phurd2R--KEaxGCxCtItE"
    URL = "https://api.telegram.org/bot{}/".format(TOKEN)

    def get_url(self, url):
        response = requests.get(url)
        content = response.content.decode("utf8")
        return content


    def get_json_from_url(self, url):
        content = self.get_url(url)
        js = json.loads(content)
        return js


    def get_updates(self, offset=None):
        url = self.URL + "getUpdates"
        if offset:
            url += "?offset={}".format(offset)
        js = self.get_json_from_url(url)
        return js


    def get_last_update_id(self, updates):
        update_ids = []
        for update in updates["result"]:
            update_ids.append(int(update["update_id"]))
        return max(update_ids)

    def get_last_chat_id_and_text(self, updates):
        num_updates = len(updates["result"])
        last_update = num_updates - 1
        text = updates["result"][last_update]["message"]["text"]
        chat_id = updates["result"][last_update]["message"]["chat"]["id"]
        return (text, chat_id)


    def send_message(self, text, chat_id):
        text = urllib.parse.quote_plus(text)
        url = self.URL + "sendMessage?text={}&chat_id={}".format(text, chat_id)
        self.get_url(url)

    @staticmethod
    def _text_analyser(text):
        if text == "/start":
            response = "Bem vindo. Irei fornecer informações " + \
                       "sobre a quantidade de imóveis registrados na sua " + \
                       "plataforma!"
        elif text == "/analyse":
            response = "Quantidade de imóveis hoje: 41150"
        else:
            response = "Descuple... Não entendi o que você disse :("
        return response

    def echo_all(self, updates):
        for update in updates["result"]:
            text = update["message"]["text"]
            chat = update["message"]["chat"]["id"]

            text = self._text_analyser(text)
            self.send_message(text, chat)
