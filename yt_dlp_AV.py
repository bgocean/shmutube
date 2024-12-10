import yt_dlp

def download_media(url, save_path=".", mode="video"):
    """
    Скачивает медиафайл с YouTube.

    :param url: Ссылка на видео YouTube
    :param save_path: Путь для сохранения файла
    :param mode: Режим "video" для видео или "audio" для аудио
    """
    if mode == "audio":
        ydl_opts = {
            "format": "bestaudio/best",
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",
            "postprocessors": [
                {
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",  # Или другой формат: 'aac', 'wav', 'flac'
                    "preferredquality": "192",  # Качество битрейта
                }
            ],
        }
    else:
        ydl_opts = {
            "format": "bestvideo+bestaudio/best",  # Скачивает наилучшее качество
            "outtmpl": f"{save_path}/%(title)s.%(ext)s",
        }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])

# Меню для выбора режима
def main():
    print("Добро пожаловать в YouTube загрузчик!")
    url = input("Введите ссылку на видео YouTube: ").strip()

    print("\nВыберите режим скачивания:")
    print("1. Видео (с аудио)")
    print("2. Только аудио")
    choice = input("Введите 1 или 2: ").strip()

    if choice == "1":
        download_media(url, mode="video")
        print("\nСкачано видео!")
    elif choice == "2":
        download_media(url, mode="audio")
        print("\nСкачано аудио!")
    else:
        print("\nНеверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main()


"""Добавлена возможность выбора режима:

Видео (с аудио): скачивается полное видеофайл.
Только аудио: аудиофайл извлекается и сохраняется в формате MP3 (можно изменить на wav, flac, и т.д.).
Параметры для скачивания аудио:

Используется постпроцессор FFmpegExtractAudio для преобразования аудио в нужный формат.
Интерактивное меню:

Пользователь вводит ссылку и выбирает нужный режим (видео или аудио)."""