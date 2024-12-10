# import kivy
# from kivy.app import App
# from kivy.uix.boxlayout import BoxLayout
# from kivy.uix.textinput import TextInput
# from kivy.uix.button import Button
# from kivy.uix.label import Label
# from kivy.uix.progressbar import ProgressBar
# from kivy.uix.filechooser import FileChooserIconView
# import yt_dlp
# import os
#
#
# class YouTubeDownloaderApp(App):
#     def build(self):
#         self.title = "YouTube Downloader"
#
#         layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
#
#         self.url_input = TextInput(hint_text="Enter YouTube URL", size_hint_y=None, height=30)
#         layout.add_widget(self.url_input)
#
#         self.file_chooser = FileChooserIconView()
#         layout.add_widget(self.file_chooser)
#
#         self.progress_bar = ProgressBar(max=100, size_hint_y=None, height=20)
#         layout.add_widget(self.progress_bar)
#
#         self.status_label = Label(text="Progress: 0%", size_hint_y=None, height=30)
#         layout.add_widget(self.status_label)
#
#         self.download_video_button = Button(text="Download Video", size_hint_y=None, height=40)
#         self.download_video_button.bind(on_press=self.download_video)
#         layout.add_widget(self.download_video_button)
#
#         self.download_audio_button = Button(text="Download Audio", size_hint_y=None, height=40)
#         self.download_audio_button.bind(on_press=self.download_audio)
#         layout.add_widget(self.download_audio_button)
#
#         return layout
#
#     def update_progress(self, progress, status):
#         self.progress_bar.value = progress * 100
#         self.status_label.text = f"Progress: {int(progress * 100)}%"
#
#     def download_video(self, instance):
#         url = self.url_input.text
#         folder_path = self.file_chooser.path
#         if not url:
#             self.status_label.text = "Please enter a valid URL"
#             return
#
#         if not folder_path:
#             self.status_label.text = "Please select a folder"
#             return
#
#         self.status_label.text = "Downloading video..."
#         ydl_opts = {
#             "outtmpl": os.path.join(folder_path, "%(title)s.%(ext)s"),
#             "progress_hooks": [lambda d: self.update_progress(d, 'downloading')]
#         }
#
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             self.status_label.text = "Download Complete!"
#         except Exception as e:
#             self.status_label.text = f"Error: {e}"
#
#     def download_audio(self, instance):
#         url = self.url_input.text
#         folder_path = self.file_chooser.path
#         if not url:
#             self.status_label.text = "Please enter a valid URL"
#             return
#
#         if not folder_path:
#             self.status_label.text = "Please select a folder"
#             return
#
#         self.status_label.text = "Downloading audio..."
#         ydl_opts = {
#             "format": "bestaudio/best",
#             "outtmpl": os.path.join(folder_path, "%(title)s.%(ext)s"),
#             "postprocessors": [{
#                 "key": "FFmpegExtractAudio",
#                 "preferredcodec": "mp3",
#                 "preferredquality": "192",
#             }],
#             "progress_hooks": [lambda d: self.update_progress(d, 'downloading')]
#         }
#
#         try:
#             with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#                 ydl.download([url])
#             self.status_label.text = "Audio Download Complete!"
#         except Exception as e:
#             self.status_label.text = f"Error: {e}"
#
#
# if __name__ == "__main__":
#     YouTubeDownloaderApp().run()


import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit
import yt_dlp
import os

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(200, 200, 400, 250)

        self.folder_path = ''
        self.initUI()

    def initUI(self):
        layout = QVBoxLayout()

        self.url_label = QLabel("Введите ссылку на видео:")
        layout.addWidget(self.url_label)

        self.url_input = QLineEdit(self)
        layout.addWidget(self.url_input)

        self.select_folder_button = QPushButton('Выбрать папку для сохранения', self)
        self.select_folder_button.clicked.connect(self.select_folder)
        layout.addWidget(self.select_folder_button)

        self.download_video_button = QPushButton('Скачать видео', self)
        self.download_video_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_video_button)

        self.download_audio_button = QPushButton('Скачать аудио', self)
        self.download_audio_button.clicked.connect(self.download_audio)
        layout.addWidget(self.download_audio_button)

        self.status_label = QLabel("Статус: Ожидание...", self)
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def select_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Выбрать папку для сохранения")
        if folder:
            self.folder_path = folder
            self.status_label.setText(f"Выбрана папка: {self.folder_path}")

    def download_video(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText("Ошибка: Введите ссылку!")
            return

        if not self.folder_path:
            self.status_label.setText("Ошибка: Выберите папку для сохранения!")
            return

        ydl_opts = {
            "outtmpl": os.path.join(self.folder_path, "%(title)s.%(ext)s"),
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.setText("Загрузка видео завершена!")
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")

    def download_audio(self):
        url = self.url_input.text()
        if not url:
            self.status_label.setText("Ошибка: Введите ссылку!")
            return

        if not self.folder_path:
            self.status_label.setText("Ошибка: Выберите папку для сохранения!")
            return

        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(self.folder_path, "%(title)s.%(ext)s"),
            "postprocessors": [{
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }],
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            self.status_label.setText("Загрузка аудио завершена!")
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloaderApp()
    ex.show()
    sys.exit(app.exec_())
