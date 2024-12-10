import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QLabel, QLineEdit
import yt_dlp
import os

class YouTubeDownloaderApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("YouTube Downloader")
        self.setGeometry(200, 200, 400, 200)

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

        self.download_button = QPushButton('Скачать видео', self)
        self.download_button.clicked.connect(self.download_video)
        layout.addWidget(self.download_button)

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
            self.status_label.setText("Загрузка завершена!")
        except Exception as e:
            self.status_label.setText(f"Ошибка: {str(e)}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = YouTubeDownloaderApp()
    ex.show()
    sys.exit(app.exec_())
