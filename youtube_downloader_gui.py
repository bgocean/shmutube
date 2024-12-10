import yt_dlp
import flet as ft


def download_media(url, mode, page):
    """
    Скачивает медиафайл с YouTube.

    :param url: Ссылка на видео YouTube
    :param mode: "video" для видео или "audio" для аудио
    :param page: Страница для обновления UI
    """
    page.snack_bar = ft.SnackBar(content=ft.Text("Начинается загрузка..."))
    page.snack_bar.open = True
    page.update()

    ydl_opts = {
        "outtmpl": f"./%(title)s.%(ext)s",
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


def main(page: ft.Page):
    page.title = "YouTube Загрузчик"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.vertical_alignment = ft.MainAxisAlignment.CENTER

    url_field = ft.TextField(label="Ссылка на видео", width=400)
    download_button_video = ft.ElevatedButton("Скачать Видео",
                                              on_click=lambda e: download_media(url_field.value, "video", page))
    download_button_audio = ft.ElevatedButton("Скачать Аудио",
                                              on_click=lambda e: download_media(url_field.value, "audio", page))

    page.add(
        ft.Column(
            [
                ft.Text("YouTube Загрузчик", size=30, weight=ft.FontWeight.BOLD),
                url_field,
                ft.Row([download_button_video, download_button_audio], alignment=ft.MainAxisAlignment.CENTER),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
