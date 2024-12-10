# from pytube import YouTube
#
# # Ссылка на видео (замени на актуальную)
# url = "https://www.youtube.com/shorts/FMjCIiL4ELI"
#
# # Проверяем, что библиотека работает
# try:
#     yt = YouTube(url)
#     print(f"Название видео: {yt.title}")
#     print(f"Автор: {yt.author}")
#     print(f"Длительность: {yt.length} секунд")
# except Exception as e:
#     print(f"Произошла ошибка: {e}")


"""Основная программа"""

from pytube import YouTube
import os


def download_video(url, save_path="."):
    try:
        # Создаем объект YouTube
        yt = YouTube(url)

        # Получаем видео с наилучшим разрешением
        video = yt.streams.get_highest_resolution()

        print(f"Скачиваю: {yt.title} (размер: {video.filesize // 1024} KB)")

        # Скачиваем видео
        video.download(output_path=save_path)
        print(f"Видео успешно скачано в: {os.path.abspath(save_path)}")
    except Exception as e:
        print(f"Произошла ошибка: {e}")


if __name__ == "__main__":
    # Ввод ссылки на видео
    video_url = input("Введите ссылку на YouTube-видео: ")

    # Ввод пути для сохранения
    save_dir = input("Введите путь для сохранения (по умолчанию текущая папка): ")
    if not save_dir.strip():
        save_dir = "."

    download_video(video_url, save_dir)

# YouTube(url): Создаётся объект YouTube для работы с указанным видео.
#
# yt.streams.get_highest_resolution(): Автоматически выбирается поток
# с максимальным разрешением для скачивания.
#
# video.download(output_path): Видео скачивается в указанную папку.
# Если путь не указан, видео сохраняется в текущей директории.

"""Выбор качества видео"""

streams = yt.streams.filter(progressive=True, file_extension='mp4')
print("Доступные варианты качества:")
for i, stream in enumerate(streams):
    print(f"{i + 1}. {stream.resolution} ({stream.filesize // 1024} KB)")
choice = int(input("Выберите номер: "))
streams[choice - 1].download(output_path=save_path)

"""Скачивание только аудио"""
audio_stream = yt.streams.filter(only_audio=True).first()
audio_stream.download(output_path=save_path)
