import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, filedialog
import threading
import os
import requests
from io import BytesIO
from PIL import Image

# --- Настройки темы ---
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

# --- Словари переводов ---
LANG = {
    "ru": {
        "title": "YouTube Downloader Pro",
        "link_label": "Ссылка на YouTube или ID видео:",
        "placeholder": "Например: dQw4w9WgXcQ",
        "find_btn": "Найти видео",
        "preview_wait": "Введите ссылку и нажмите 'Найти видео'",
        "folder_label": "Папка:",
        "browse_btn": "Обзор...",
        "video_radio": "Видео (MP4)",
        "audio_radio": "Аудио (MP3)",
        "quality_label": "Качество:",
        "download_btn": "СКАЧАТЬ",
        "status_wait": "Статус: Ожидание",
        "status_loading": "Загрузка информации...",
        "status_ready": "Готово к скачиванию",
        "status_converting": "Конвертация (подождите)...",
        "status_success": "Успешно завершено!",
        "status_error": "Ошибка скачивания",
        "err_empty": "Введите ссылку или ID видео",
        "err_folder": "Выберите папку для сохранения",
        "q_vid_best": "Лучшее качество",
        "q_aud_best": "Лучшее (320 kbps)",
    },
    "en": {
        "title": "YouTube Downloader Pro",
        "link_label": "YouTube Link or Video ID:",
        "placeholder": "Example: dQw4w9WgXcQ",
        "find_btn": "Find Video",
        "preview_wait": "Enter link and click 'Find Video'",
        "folder_label": "Folder:",
        "browse_btn": "Browse...",
        "video_radio": "Video (MP4)",
        "audio_radio": "Audio (MP3)",
        "quality_label": "Quality:",
        "download_btn": "DOWNLOAD",
        "status_wait": "Status: Waiting",
        "status_loading": "Loading info...",
        "status_ready": "Ready to download",
        "status_converting": "Converting (please wait)...",
        "status_success": "Successfully finished!",
        "status_error": "Download error",
        "err_empty": "Enter a link or video ID",
        "err_folder": "Select a folder to save",
        "q_vid_best": "Best Quality",
        "q_aud_best": "Best (320 kbps)",
    }
}

current_lang = "ru"


# --- Логика приложения ---

def get_full_url(user_input):
    user_input = user_input.strip()
    if not user_input: return ""
    if user_input.startswith("http://") or user_input.startswith("https://"):
        return user_input
    return f"https://www.youtube.com/watch?v={user_input}"


def select_folder():
    folder = filedialog.askdirectory()
    if folder:
        save_path_var.set(folder)


def update_quality_options():
    """Обновляет список качества в зависимости от выбранного режима"""
    mode = mode_var.get()
    t = LANG[current_lang]
    if mode == "video":
        options = [t["q_vid_best"], "1080p", "720p", "480p", "360p"]
    else:
        options = [t["q_aud_best"], "192 kbps", "128 kbps"]

    quality_menu.configure(values=options)
    quality_menu.set(options[0])


def change_language(choice):
    """Смена языка 'на лету'"""
    global current_lang
    current_lang = "ru" if choice == "Русский" else "en"
    t = LANG[current_lang]

    app.title(t["title"])
    link_label.configure(text=t["link_label"])
    url_entry.configure(placeholder_text=t["placeholder"])
    preview_btn.configure(text=t["find_btn"])

    # Меняем текст превью только если там дефолтная заглушка
    if thumb_label.cget("image") is None:
        title_label.configure(text=t["preview_wait"])

    folder_label.configure(text=t["folder_label"])
    browse_btn.configure(text=t["browse_btn"])
    video_radio.configure(text=t["video_radio"])
    audio_radio.configure(text=t["audio_radio"])
    quality_label.configure(text=t["quality_label"])
    download_btn.configure(text=t["download_btn"])

    if "Ожидание" in status_label.cget("text") or "Waiting" in status_label.cget("text"):
        status_label.configure(text=t["status_wait"])

    update_quality_options()


def load_preview():
    url = get_full_url(url_entry.get())
    t = LANG[current_lang]

    if not url:
        messagebox.showwarning("Внимание", t["err_empty"])
        return

    status_label.configure(text=t["status_loading"], text_color="#3498db")
    preview_btn.configure(state="disabled")
    download_btn.configure(state="disabled")

    threading.Thread(target=fetch_video_info, args=(url,), daemon=True).start()


def fetch_video_info(url):
    import yt_dlp
    try:
        ydl_opts = {'quiet': True, 'skip_download': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=False)

        title = info.get('title', 'Unknown video')
        thumb_url = info.get('thumbnail', '')

        if thumb_url:
            response = requests.get(thumb_url)
            img = Image.open(BytesIO(response.content))
            ctk_image = ctk.CTkImage(light_image=img, dark_image=img, size=(300, 170))
            app.after(0, lambda: update_ui_preview(title, ctk_image))
        else:
            app.after(0, lambda: update_ui_preview(title, None))

    except Exception as e:
        app.after(0, lambda: status_label.configure(text=LANG[current_lang]["status_error"], text_color="red"))
    finally:
        app.after(0, lambda: preview_btn.configure(state="normal"))
        app.after(0, lambda: download_btn.configure(state="normal"))


def update_ui_preview(title, photo):
    title_label.configure(text=title)
    if photo:
        thumb_label.configure(image=photo, text="")
        thumb_label.image = photo
    status_label.configure(text=LANG[current_lang]["status_ready"], text_color="#2ecc71")


def progress_hook(d):
    t = LANG[current_lang]
    if d['status'] == 'downloading':
        percent_str = d.get('_percent_str', '0%').replace('\x1b[0;94m', '').replace('\x1b[0m', '').strip()
        try:
            percent_float = float(percent_str.replace('%', '')) / 100.0
            dl_text = f"Скачивание: {percent_str}" if current_lang == "ru" else f"Downloading: {percent_str}"
            app.after(0, lambda: progress_bar.set(percent_float))
            app.after(0, lambda: status_label.configure(text=dl_text, text_color="#f39c12"))
        except ValueError:
            pass
    elif d['status'] == 'finished':
        app.after(0, lambda: status_label.configure(text=t["status_converting"], text_color="#9b59b6"))


def start_download():
    url = get_full_url(url_entry.get())
    save_path = save_path_var.get()
    t = LANG[current_lang]

    if not url:
        messagebox.showerror("Ошибка", t["err_empty"])
        return
    if not save_path:
        messagebox.showerror("Ошибка", t["err_folder"])
        return

    mode = mode_var.get()
    quality = quality_menu.get()
    threading.Thread(target=process_download, args=(url, mode, quality, save_path), daemon=True).start()


def process_download(url, mode, quality, save_path):
    import yt_dlp
    import imageio_ffmpeg
    app.after(0, lambda: download_btn.configure(state="disabled"))
    app.after(0, lambda: progress_bar.set(0))
    t = LANG[current_lang]
    ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

    try:
        outtmpl = os.path.join(save_path, '%(title)s.%(ext)s')
        ydl_opts = {
            'outtmpl': outtmpl,
            'nocolor': True,
            'ffmpeg_location': ffmpeg_exe,
            'progress_hooks': [progress_hook]
        }

        # Настройка качества видео
        if mode == "video":
            # Парсим выбранное разрешение
            if "1080p" in quality:
                fmt = 'bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]/best'
            elif "720p" in quality:
                fmt = 'bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best'
            elif "480p" in quality:
                fmt = 'bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4][height<=480]/best'
            elif "360p" in quality:
                fmt = 'bestvideo[ext=mp4][height<=360]+bestaudio[ext=m4a]/best[ext=mp4][height<=360]/best'
            else:  # Лучшее
                fmt = 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best'

            ydl_opts.update({
                'format': fmt,
                'merge_output_format': 'mp4',
            })

        # Настройка качества аудио
        else:
            if "192" in quality:
                audio_q = '192'
            elif "128" in quality:
                audio_q = '128'
            else:
                audio_q = '320'  # Лучшее

            ydl_opts.update({
                'format': 'bestaudio/best',
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': audio_q,
                }],
            })

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        app.after(0, lambda: status_label.configure(text=t["status_success"], text_color="#2ecc71"))
        app.after(0, lambda: progress_bar.set(1.0))

    except Exception as e:
        app.after(0, lambda: status_label.configure(text=t["status_error"], text_color="red"))
        app.after(0, lambda: messagebox.showerror("Error", str(e)))
    finally:
        app.after(0, lambda: download_btn.configure(state="normal"))


# --- Интерфейс (GUI) ---
app = ctk.CTk()
app.title("YouTube Downloader Pro")
app.geometry("520x720")
app.resizable(False, False)

# Верхняя панель с выбором языка
top_frame = ctk.CTkFrame(app, fg_color="transparent")
top_frame.pack(fill="x", padx=10, pady=5)
lang_menu = ctk.CTkOptionMenu(top_frame, values=["Русский", "English"], command=change_language, width=100)
lang_menu.pack(side="right")

# Ввод ссылки
link_label = ctk.CTkLabel(app, text=LANG[current_lang]["link_label"], font=("Arial", 14, "bold"))
link_label.pack(pady=(5, 5))

url_entry = ctk.CTkEntry(app, width=400, placeholder_text=LANG[current_lang]["placeholder"])
url_entry.pack(pady=5)

preview_btn = ctk.CTkButton(app, text=LANG[current_lang]["find_btn"], command=load_preview, fg_color="gray")
preview_btn.pack(pady=10)

# Превью
title_label = ctk.CTkLabel(app, text=LANG[current_lang]["preview_wait"], wraplength=450)
title_label.pack(pady=(5, 0))

thumb_label = ctk.CTkLabel(app, text="[ Превью / Preview ]", width=300, height=170, fg_color="gray30", corner_radius=10)
thumb_label.pack(pady=10)

# Папка
path_frame = ctk.CTkFrame(app, fg_color="transparent")
path_frame.pack(pady=5)

save_path_var = tk.StringVar(value=os.path.expanduser("~/Downloads"))
folder_label = ctk.CTkLabel(path_frame, text=LANG[current_lang]["folder_label"])
folder_label.pack(side="left", padx=5)
ctk.CTkEntry(path_frame, textvariable=save_path_var, width=250, state="readonly").pack(side="left", padx=5)
browse_btn = ctk.CTkButton(path_frame, text=LANG[current_lang]["browse_btn"], command=select_folder, width=80)
browse_btn.pack(side="left")

# Настройки формата и качества
settings_frame = ctk.CTkFrame(app)
settings_frame.pack(pady=15, padx=20, fill="x")

mode_var = tk.StringVar(value="video")

radio_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
radio_frame.pack(pady=10)

video_radio = ctk.CTkRadioButton(radio_frame, text=LANG[current_lang]["video_radio"], variable=mode_var, value="video",
                                 command=update_quality_options)
video_radio.pack(side="left", padx=20)

audio_radio = ctk.CTkRadioButton(radio_frame, text=LANG[current_lang]["audio_radio"], variable=mode_var, value="audio",
                                 command=update_quality_options)
audio_radio.pack(side="left", padx=20)

quality_frame = ctk.CTkFrame(settings_frame, fg_color="transparent")
quality_frame.pack(pady=(0, 10))

quality_label = ctk.CTkLabel(quality_frame, text=LANG[current_lang]["quality_label"])
quality_label.pack(side="left", padx=10)

quality_menu = ctk.CTkOptionMenu(quality_frame, values=[])
quality_menu.pack(side="left")

# Инициализируем список качества при запуске
update_quality_options()

# Прогресс и статус
progress_bar = ctk.CTkProgressBar(app, width=400)
progress_bar.pack(pady=10)
progress_bar.set(0)

status_label = ctk.CTkLabel(app, text=LANG[current_lang]["status_wait"], font=("Arial", 12))
status_label.pack()

download_btn = ctk.CTkButton(app, text=LANG[current_lang]["download_btn"], command=start_download, width=200, height=40,
                             font=("Arial", 14, "bold"), fg_color="#27ae60", hover_color="#2ecc71")
download_btn.pack(pady=10)

app.mainloop()