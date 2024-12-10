import yt_dlp
import flet as ft
import os

def download_media(url, mode, save_path, progress_bar, progress_label, page):
    if not url:
        page.snack_bar = ft.SnackBar(content=ft.Text("Введите ссылку!"), bgcolor=ft.colors.ERROR)
        page.snack_bar.open = True
        page.update()
        return

    if not save_path:
        page.snack_bar = ft.SnackBar(content=ft.Text("Выберите папку для сохранения!"), bgcolor=ft.colors.ERROR)
        page.snack_bar.open = True
        page.update()
        return

    progress_bar.value = 0
    progress_label.value = "Загрузка: 0%"
    page.update()

    ydl_opts = {
        "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
        "progress_hooks": [lambda d: update_progress(d, progress_bar, progress_label, page)],
    }

    if mode == "audio":
        ydl_opts.update({
            "format": "bestaudio/best",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }
            ],
        })
    else:
        ydl_opts.update({
            "format": "bestvideo+bestaudio/best",
        })

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        page.snack_bar = ft.SnackBar(content=ft.Text("Загрузка завершена!"))
    except Exception as e:
        page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {e}"), bgcolor=ft.colors.ERROR)
    page.snack_bar.open = True
    page.update()

def update_progress(d, progress_bar, progress_label, page):
    if d["status"] == "downloading":
        total_bytes = d.get("total_bytes", 1)
        downloaded_bytes = d.get("downloaded_bytes", 0)
        progress = downloaded_bytes / total_bytes
        progress_bar.value = progress
        progress_label.value = f"Загрузка: {int(progress * 100)}%"
        page.update()

def main(page: ft.Page):
    page.title = "YouTube Загрузчик"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    url_field = ft.TextField(label="Ссылка на видео", width=400)
    folder_path = ft.Text(value="", visible=False)

    def select_folder(e):
        def on_result(result):
            if result.path:
                folder_path.value = result.path
                page.snack_bar = ft.SnackBar(content=ft.Text(f"Выбрана папка: {result.path}"))
                page.snack_bar.open = True
                page.update()
        page.dialog = ft.FilePicker(on_result=on_result)
        page.dialog.get_directory_path()

    select_folder_button = ft.ElevatedButton("Выбрать папку для сохранения", on_click=select_folder)

    progress_bar = ft.ProgressBar(width=400)
    progress_label = ft.Text("Прогресс: 0%")

    download_button_video = ft.ElevatedButton(
        "Скачать Видео",
        on_click=lambda e: download_media(url_field.value, "video", folder_path.value, progress_bar, progress_label, page)
    )
    download_button_audio = ft.ElevatedButton(
        "Скачать Аудио",
        on_click=lambda e: download_media(url_field.value, "audio", folder_path.value, progress_bar, progress_label, page)
    )

    page.add(
        ft.Column(
            [
                ft.Text("YouTube Загрузчик", size=30, weight=ft.FontWeight.BOLD),
                url_field,
                select_folder_button,
                progress_bar,
                progress_label,
                ft.Row([download_button_video, download_button_audio], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )

if __name__ == "__main__":
    ft.app(target=main)

































# import yt_dlp
# import flet as ft
# import os
#
#
# def download_media(url, mode, save_path, progress_bar, progress_label, page):
#     """
#     Скачивает медиафайл с YouTube.
#
#     :param url: Ссылка на видео YouTube
#     :param mode: "video" для видео или "audio" для аудио
#     :param save_path: Путь для сохранения файла
#     :param progress_bar: Прогресс-бар
#     :param progress_label: Метка прогресса
#     :param page: Страница для обновления UI
#     """
#     if not url:
#         page.snack_bar = ft.SnackBar(content=ft.Text("Введите ссылку!"), bgcolor=ft.colors.ERROR)
#         page.snack_bar.open = True
#         page.update()
#         return
#
#     if not save_path:
#         page.snack_bar = ft.SnackBar(content=ft.Text("Выберите папку для сохранения!"), bgcolor=ft.colors.ERROR)
#         page.snack_bar.open = True
#         page.update()
#         return
#
#     progress_bar.value = 0
#     progress_label.value = "Загрузка: 0%"
#     page.update()
#
#     ydl_opts = {
#         "outtmpl": os.path.join(save_path, "%(title)s.%(ext)s"),
#         "progress_hooks": [lambda d: update_progress(d, progress_bar, progress_label, page)],
#     }
#
#     if mode == "audio":
#         ydl_opts.update({
#             "format": "bestaudio/best",
#             "postprocessors": [
#                 {
#                     "key": "FFmpegExtractAudio",
#                     "preferredcodec": "mp3",
#                     "preferredquality": "192",
#                 }
#             ],
#         })
#     else:
#         ydl_opts.update({
#             "format": "bestvideo+bestaudio/best",
#         })
#
#     try:
#         with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#             ydl.download([url])
#         page.snack_bar = ft.SnackBar(content=ft.Text("Загрузка завершена!"))
#     except Exception as e:
#         page.snack_bar = ft.SnackBar(content=ft.Text(f"Ошибка: {e}"), bgcolor=ft.colors.ERROR)
#     page.snack_bar.open = True
#     page.update()
#
#
# def update_progress(d, progress_bar, progress_label, page):
#     """
#     Обновляет прогресс-бар и метку прогресса.
#
#     :param d: Данные о прогрессе
#     :param progress_bar: Прогресс-бар
#     :param progress_label: Метка прогресса
#     :param page: Страница для обновления UI
#     """
#     if d["status"] == "downloading":
#         total_bytes = d.get("total_bytes", 1)
#         downloaded_bytes = d.get("downloaded_bytes", 0)
#         progress = downloaded_bytes / total_bytes
#         progress_bar.value = progress
#         progress_label.value = f"Загрузка: {int(progress * 100)}%"
#         page.update()
#
#
# def main(page: ft.Page):
#     page.title = "YouTube Загрузчик"
#     page.theme_mode = ft.ThemeMode.LIGHT
#     page.vertical_alignment = ft.MainAxisAlignment.CENTER
#
#     url_field = ft.TextField(label="Ссылка на видео", width=400)
#     folder_path = ft.Text(value="", visible=False)
#     select_folder_button = ft.ElevatedButton(
#         "Выбрать папку для сохранения",
#         on_click=lambda e: folder_path.value := ft.file_picker.FilePicker.save_folder_dialog(
#         on_result=lambda result: folder_path.value := result.path if result else "")
#     )
#
#     progress_bar = ft.ProgressBar(width=400)
#     progress_label = ft.Text("Прогресс: 0%")
#
#     download_button_video = ft.ElevatedButton(
#         "Скачать Видео",
#         on_click=lambda e: download_media(url_field.value, "video", folder_path.value, progress_bar, progress_label,
#                                           page)
#     )
#     download_button_audio = ft.ElevatedButton(
#         "Скачать Аудио",
#         on_click=lambda e: download_media(url_field.value, "audio", folder_path.value, progress_bar, progress_label,
#                                           page)
#     )
#
#     page.add(
#         ft.Column(
#             [
#                 ft.Text("YouTube Загрузчик", size=30, weight=ft.FontWeight.BOLD),
#                 url_field,
#                 select_folder_button,
#                 progress_bar,
#                 progress_label,
#                 ft.Row([download_button_video, download_button_audio], alignment=ft.MainAxisAlignment.CENTER),
#             ],
#             alignment=ft.MainAxisAlignment.CENTER,
#             horizontal_alignment=ft.CrossAxisAlignment.CENTER,
#         )
#     )
#
#
# if __name__ == "__main__":
#     ft.app(target=main)

