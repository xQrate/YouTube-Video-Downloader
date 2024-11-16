import yt_dlp
import os
import time
import socket
from tkinter import *
from tkinter import messagebox
import threading
import sys


# Устанавливаем путь к yt-dlp в зависимости от того, где мы находимся (при запуске через .exe)
if getattr(sys, 'frozen', False):
    # Если программа запущена как .exe
    current_folder = os.path.dirname(sys.executable)  # Папка с .exe файлом
else:
    # Если программа запущена из исходного кода
    current_folder = os.path.dirname(os.path.abspath(__file__))  # Текущая директория скрипта

yt_dlp_path = os.path.join(current_folder, 'yt-dlp')  # Путь к yt-dlp

# Создаем главное окно
root = Tk()
root.title("YouTube Video Downloader")
root.geometry("600x300")
root.config(bg="#D3D3D3")

link1 = StringVar()
loading_label = None  # Глобальная переменная для анимации текста
animation_running = False

# Функция для проверки подключения к интернету
def check_internet():
    try:
        # Попытка подключения к Google DNS
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except OSError:
        return False

# Функция для скачивания видео с повторными попытками
def download():
    if not check_internet():
        messagebox.showerror("Ошибка", "Нет подключения к интернету. Проверьте соединение и попробуйте снова.")
        stop_loading_animation()
        return

    link = link1.get()
    if not link:
        messagebox.showerror("Ошибка", "Пожалуйста, введите ссылку на видео.")
        stop_loading_animation()
        return
    
    # Папка для сохранения видео (в той же папке, что и скрипт)
    download_folder = os.path.join(current_folder, "YouTube_Videos")
    
    # Если папки нет, создаём её
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Настройки для yt-dlp
    ydl_opts = {
        "format": "best",
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),  # Сохраняем в папку "YouTube_Videos"
    }
    
    # Попытки скачивания
    retries = 3  # Максимальное количество попыток
    for attempt in range(retries):
        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([link])  # Попытка скачать видео
            messagebox.showinfo("Успех", f"Видео успешно загружено в папку: {download_folder}")
            stop_loading_animation()
            return
        except yt_dlp.utils.DownloadError as e:
            error_msg = f"Ошибка при скачивании: {e}"
            messagebox.showerror("Ошибка", error_msg)
            stop_loading_animation()
            return
        except ConnectionResetError as e:
            # Если ошибка 10054, пробуем еще раз
            if attempt < retries - 1:
                messagebox.showwarning("Предупреждение", f"Попытка {attempt + 1} из {retries}. Соединение прервано. Повторная попытка...")
                time.sleep(2)  # Ожидание 2 секунды перед повтором
            else:
                messagebox.showerror("Ошибка", "Превышено количество попыток подключения.")
                stop_loading_animation()
                return
        except Exception as e:
            messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")
            stop_loading_animation()
            return

# Функция для очистки поля ввода
def reset():
    link1.set("")

# Функция для выхода из приложения
def Exit():
    root.destroy()

# Функция для запуска скачивания в отдельном потоке
def start_download_thread():
    start_loading_animation()
    download_thread = threading.Thread(target=download)
    download_thread.start()

# Функции для анимации текста "Загрузка..."
def start_loading_animation():
    global loading_label, animation_running
    if not animation_running:
        loading_label = Label(root, text="Загрузка", font=('Arial', 15, 'bold'), bg='#D3D3D3')
        loading_label.pack(pady=110)
        animation_running = True
        animate_loading_dots()

def stop_loading_animation():
    global loading_label, animation_running
    if loading_label:
        loading_label.destroy()
    animation_running = False

def animate_loading_dots():
    global loading_label, animation_running
    if not animation_running:
        return

    current_text = loading_label.cget("text")
    if current_text.endswith("..."):
        loading_label.config(text="Загрузка")
    else:
        loading_label.config(text=current_text + ".")

    root.after(500, animate_loading_dots)

# Заголовок формы
lb = Label(root, text="---Загрузка видео с YouTube---", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb.pack(pady=15)

lb1 = Label(root, text="Ссылка на видео :", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb1.place(x=10, y=80)

En1 = Entry(root, textvariable=link1, font=('Arial', 15, 'bold'), width=30)
En1.place(x=230, y=80)

btn1 = Button(root, text="Скачать", font=('Arial', 10, 'bold'), bd=4, command=start_download_thread)
btn1.place(x=330, y=130)

btn2 = Button(root, text="Очистить", font=('Arial', 10, 'bold'), bd=4, command=reset)
btn2.place(x=180, y=220)

btn3 = Button(root, text="Выход", font=('Arial', 10, 'bold'), bd=4, command=Exit)
btn3.place(x=280, y=220)

root.mainloop()
