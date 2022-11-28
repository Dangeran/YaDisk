import requests
from tkinter import filedialog, messagebox

from settings import TOKEN


class YaUploader:
    base_host = "https://cloud-api.yandex.net/"

    def __init__(self, token: str):
        self.token = token

    def get_headers(self):
        return {
            'Content-Type': 'application/json',
            'Authorization': f'OAuth {self.token}'
        }

    # Получаем ссылку для загрузки файла
    def _get_upload_link(self, path):
        uri = 'v1/disk/resources/upload/'
        request_url = self.base_host + uri
        params = {'path': path, 'overwrite': True}
        response = requests.get(request_url, headers=self.get_headers(), params=params)
        return response.json()['href']

    def upload(self, file_path: str):
        file_name = file_path.split(sep="/")[-1]
        upload_url = self._get_upload_link(file_name)
        response = requests.put(upload_url, data=open(file_path, 'rb'), headers=self.get_headers())
        if response.status_code == 201:
            messagebox.showinfo('Загрузка произошла успешно!', f'Файл {file_path} загружен под именем {file_name}')
        else:
            messagebox.showerror('Загрузка не удалась!', 'Ошибка! Что-то опять пошло не так!')

if __name__ == '__main__':
    # Получить путь к загружаемому файлу и токен от пользователя
    path_to_file = filedialog.askopenfilename()
    uploader = YaUploader(TOKEN)
    uploader.upload(path_to_file)
