# サーバに、実行してほしいコマンドを送りつけてちゃんと実行したかどうかを確認するやつ
import requests
import json

class CommandRunner:
    def __init__(self, url):
        self.url = url

    def run_command(self, command):
        payload = {"command": command}
        response = requests.post(self.url, json=payload)
        
        if response.status_code == 200:
            return response.json().get("output")
        else:
            return response.json().get("error")
