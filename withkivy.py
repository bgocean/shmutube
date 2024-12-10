import yt_dlp
import os
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.progressbar import ProgressBar
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.popup import Popup


class YouTubeDownloaderApp(App):
    def build(self):
        self.url_input = TextInput(hint_text='Вставьте ссылку на видео', multiline=False, size_hint=(1, 0.1))
        self.url_input.bind(on_text_validate=self.download_video)

        self.progress_label = Label(text='Прогресс: 0%', size_hint=(1, 0.05))
        self.progress_bar = ProgressBar(max=100, size_hint=(1, 0.05))

        self.download_button_video = Button(text='Скачать Видео', size_hint=(1, 0.1))
        self.download_button_audio = Button(text='Скачать Аудио', size_hint=(1, 0.1))

        self.download_button_video.bind(on_press=self.download_video)
        self.download_button_audio.bind(on_press=self.download_audio)

        self.folder_path = ''

        self.select_folder_button = Button(text='Выбрать папку для сохранения', size_hint=(1, 0.1))
        self.select_folder_button.bind(on_press=self.select_folder)

        layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        layout.add_widget(self.url_input)
        layout.add_widget(self.progress_label)
        layout.add_widget(self.progress_bar)
        layout.add_widget(self.download_button_video)
        layout.add_widget(self.download_button_audio)
        layout.add_widget(self.select_folder_button)

        return layout

    def update_progress(self, d):
        if d["status"] == "downloading":
            total_bytes = d.get("total_bytes", 1)
            downloaded_bytes = d.get("downloaded_bytes", 0)
            progress = downloaded_bytes / total_bytes
            self.progress_bar.value = progress * 100
            self.progress_label.text = f'Прогресс: {int(progress * 100)}%'

    def download_video(self, instance):
        url = self.url_input.text
        if not url:
            self.show_popup('Ошибка', 'Введите ссылку!')
            return

        if not self.folder_path:
            self.show_popup('Ошибка', 'Выберите папку для сохранения!')
            return

        ydl_opts = {
            "outtmpl": os.path.join(self.folder_path, "%(title)s.%(ext)s"),
            "progress_hooks": [self.update_progress],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.show_popup('Успех', 'Загрузка завершена!')
        except Exception as e:
            self.show_popup('Ошибка', f'Ошибка: {str(e)}')

    def download_audio(self, instance):
        url = self.url_input.text
        if not url:
            self.show_popup('Ошибка', 'Введите ссылку!')
            return

        if not self.folder_path:
            self.show_popup('Ошибка', 'Выберите папку для сохранения!')
            return

        ydl_opts = {
            "outtmpl": os.path.join(self.folder_path, "%(title)s.%(ext)s"),
            "format": "bestaudio/best",
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
            "progress_hooks": [self.update_progress],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.show_popup('Успех', 'Загрузка завершена!')
        except Exception as e:
            self.show_popup('Ошибка', f'Ошибка: {str(e)}')

    def show_popup(self, title, message):
        popup = Popup(title=title, content=Label(text=message), size_hint=(None, None), size=(400, 200))
        popup.open()

    def select_folder(self, instance):
        # Используем FileChooserListView для выбора папки
        filechooser = FileChooserListView()
        filechooser.path = '/'

        # Настроим фильтр для папок
        filechooser.filters = ['*/']
        filechooser.bind(on_submit=self.on_folder_selected)

        popup = Popup(title="Выбрать папку для сохранения", content=filechooser, size_hint=(None, None),
                      size=(600, 400))
        popup.open()

    def on_folder_selected(self, instance, value):
        if value:
            self.folder_path = value[0]
            self.show_popup('Папка выбрана', f'Выбрана папка: {self.folder_path}')


if __name__ == '__main__':
    YouTubeDownloaderApp().run()
