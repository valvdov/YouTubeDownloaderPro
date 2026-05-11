# 🎥 YouTube Downloader Pro

A cross-platform application with a graphical interface for downloading videos and audio from YouTube. Built with Python using the yt-dlp library and the modern CustomTkinter UI framework.

 [![Screenshot-2026-05-11-at-18-39-00.png](https://i.postimg.cc/T1SndN4D/Screenshot-2026-05-11-at-18-39-00.png)](https://postimg.cc/FkyYGpmr)

## ✨ Features
* 🌗 Modern interface with dark and light theme support.
* 🇷🇺 🇬🇧 Instant switching between Russian and English languages.
* 🎬 Smart quality selection (1080p, 720p, etc.) and audio bitrate options (320, 192 kbps).
* ⚙️ Automatic FFmpeg download (no manual installation required).
* 📊 Real-time video preview and download progress display.

## 📦 Download (Prebuilt Releases)

You don’t need to install Python! You can download ready-to-use builds for Windows, macOS, and Linux from the **[Releases](../../releases)** section on the right side of this page.

⸻

## 🍏 macOS Troubleshooting (Gatekeeper)

If macOS says the downloaded .app file is “damaged” or “cannot be opened”, this is Apple’s built-in security protection for apps downloaded from the internet.

**How to fix it in 10 seconds:**

1. Open the Terminal application.
2. Type the command: xattr -cr  (make sure there is a space at the end!).
3. Drag the downloaded YTDownloader.app directly into the Terminal window (the path will be inserted automatically).
4. Press Enter.
    Now the application will open instantly with a double click!

⸻

## 🛠 Running from Source Code

If you want to run the project using Python or build it yourself:

1. Clone the repository:
```bash
   git clone https://github.com/valvdov/YouTubeDownloaderPro.git
   cd YouTubeDownloaderPro
```
2. Install dependencies:
```bash
pip install -r requirements.txt
```
3. Run:
```bash
python app.py
```

## ⚖️ Legal Disclaimer
This software is created for educational purposes only. The developer is not responsible for how this tool is used. Users are solely responsible for complying with copyright laws and the Terms of Service of the platforms from which content is downloaded.
# 🎥 YouTube Downloader Pro

Кроссплатформенное приложение с графическим интерфейсом для скачивания видео и аудио с YouTube. Написано на Python с использованием библиотеки `yt-dlp` и современного интерфейса `CustomTkinter`.

[![You-Tube-Downloader-Pro-RU.png](https://i.postimg.cc/XNyfx4Gx/You-Tube-Downloader-Pro-RU.png)](https://postimg.cc/jCtnSVhJ)

## ✨ Возможности
* 🌗 Современный интерфейс с поддержкой темной и светлой темы.
* 🇷🇺 🇬🇧 Поддержка русского и английского языков "на лету".
* 🎬 Умный выбор качества (1080p, 720p и т.д.) и битрейта для аудио (320, 192 kbps).
* ⚙️ Автоматическая загрузка FFmpeg (не требует ручной установки).
* 📊 Отображение превью видео и прогресса скачивания в реальном времени.

## 📦 Скачивание (Готовые сборки)
Вам не обязательно устанавливать Python! Вы можете скачать готовые сборки для Windows, macOS и Linux во вкладке **[Releases](../../releases)** справа на этой странице.

---

## 🍏 Решение проблем на macOS (Gatekeeper)
Если при открытии скачанного файла `.app` macOS пишет, что **"Приложение повреждено"** или **"Не удается открыть"**, это срабатывает встроенная защита Apple от программ, скачанных из интернета.

**Как исправить за 10 секунд:**
1. Откройте приложение **Терминал** (Terminal).
2. Напишите команду: `xattr -cr ` *(обязательно с пробелом на конце!)*.
3. Перетащите скачанное приложение `YTDownloader.app` прямо в окно Терминала (путь подставится сам).
4. Нажмите **Enter**. 
Теперь приложение будет открываться двойным кликом мгновенно!

---

## 🛠 Запуск из исходного кода
Если вы хотите запустить проект через Python или собрать его самостоятельно:

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/valvdov/YouTubeDownloaderPro.git
   cd YouTubeDownloaderPro
   ```
2. Установите зависимости:
```bash
pip install -r requirements.txt
```
3. Запустите:
```bash
python app.py
```

## ⚖️ Правовая оговорка (Disclaimer)
Данное программное обеспечение создано исключительно в образовательных целях. Разработчик не несет ответственности за использование данного инструмента. Пользователь самостоятельно обязан соблюдать авторские права и Условия использования (Terms of Service) платформ, с которых производится скачивание контента.