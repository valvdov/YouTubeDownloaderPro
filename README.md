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
3. Install [Deno](https://docs.deno.com/runtime/getting_started/installation/) 2.3 or newer. Recent `yt-dlp` versions require a JavaScript runtime to download YouTube videos.
4. Run:
```bash
python app.py
```

For a standalone build, run `python build.py`. This bundles Deno and the `yt-dlp` EJS scripts into the app.

## 🔄 Automatic releases

Once these files are pushed to the repository's `main` branch, GitHub Actions builds and publishes Windows, macOS, and Linux releases automatically after each push and every Monday at 07:23 UTC. It installs the newest dependency versions allowed by `requirements.txt`. You can also start the workflow in GitHub's **Actions → Build and Release Apps → Run workflow** or push a `v*` tag.

Published apps check the public GitHub releases page on startup and offer to open the download page when a newer version exists. Installing the downloaded update is still a user step. Source runs and local builds marked `dev` do not show update prompts.

The workflow needs GitHub Actions enabled and `contents: write` permission, already declared in [release.yml](.github/workflows/release.yml). GitHub can disable scheduled workflows in public repositories after 60 days without repository activity; re-enable the workflow in the Actions tab if that happens.

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
3. Установите [Deno](https://docs.deno.com/runtime/getting_started/installation/) версии 2.3 или новее. Новым версиям `yt-dlp` он нужен для скачивания с YouTube.
4. Запустите:
```bash
python app.py
```

Для сборки готового приложения запустите `python build.py`. Скрипт добавит Deno и EJS-файлы `yt-dlp` в сборку.

## 🔄 Автоматические релизы

После загрузки этих файлов в ветку `main` GitHub Actions будет собирать и публиковать версии для Windows, macOS и Linux после каждого изменения в основной ветке и каждый понедельник в 07:23 UTC. При сборке устанавливаются самые новые версии зависимостей, допустимые в `requirements.txt`. Запустить сборку вручную можно через **Actions → Build and Release Apps → Run workflow** или отправкой тега `v*`.

Опубликованное приложение при запуске проверяет релизы GitHub и предлагает открыть страницу загрузки новой версии. Установка загруженного обновления остаётся действием пользователя. Запуск из исходников и локальная сборка с версией `dev` уведомления не показывают.

Для работы нужны включённые GitHub Actions; право `contents: write` уже задано в [release.yml](.github/workflows/release.yml). В публичных репозиториях GitHub может отключить расписание после 60 дней без активности. Тогда запустите или включите процесс заново во вкладке Actions.

## ⚖️ Правовая оговорка (Disclaimer)
Данное программное обеспечение создано исключительно в образовательных целях. Разработчик не несет ответственности за использование данного инструмента. Пользователь самостоятельно обязан соблюдать авторские права и Условия использования (Terms of Service) платформ, с которых производится скачивание контента.
