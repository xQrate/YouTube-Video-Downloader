import yt_dlp
import os
import time
import socket
from tkinter import *
from tkinter import messagebox
import threading
import sys
import requests
import speedtest

# Устанавливаем путь к yt-dlp в зависимости от того, где мы находимся (при запуске через .exe)
if getattr(sys, 'frozen', False):
    current_folder = os.path.dirname(sys.executable)  # Папка с .exe файлом
else:
    current_folder = os.path.dirname(os.path.abspath(__file__))  # Текущая директория скрипта

yt_dlp_path = os.path.join(current_folder, 'yt-dlp')  # Путь к yt-dlp

# Создаем главное окно
root = Tk()
root.title("YouTube Video Downloader")
root.geometry("600x500")
root.config(bg="#D3D3D3")

link1 = StringVar()
proxy_address = StringVar()
proxy_port = StringVar()
loading_label = None  # Глобальная переменная для анимации текста
animation_running = False

# Функция для получения списка бесплатных прокси


# Функция для скачивания видео с повторными попытками
def download():
    link = link1.get()
 

    if not link:
        messagebox.showerror("Ошибка", "Пожалуйста, введите ссылку на видео.")
        stop_loading_animation()
        return

  

    # Папка для сохранения видео (в той же папке, что и скрипт)
    download_folder = os.path.join("YouTube_Videos")

    # Если папки нет, создаём её
    if not os.path.exists(download_folder):
        os.makedirs(download_folder)

    # Настройки для yt-dlp
    ydl_opts = {
        "format": "best",  # Ограничиваем до 720p
        "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s"),
        "socket_timeout": 100,
    }

    # Попытки скачивания
    retries = 6  # Максимальное количество попыток
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

# Функция для очистки полей ввода
def reset():
    link1.set("")
    proxy_address.set("")
    proxy_port.set("")


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
        loading_label.pack(pady=160)
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


def check_internet_speed():
    try:
        # Создаем объект Speedtest
        st = speedtest.Speedtest()

        # Получаем лучший сервер (с наименьшим пингом)
        st.get_best_server()

        # Печатаем информацию о лучшем сервере
        log_message("Получен лучший сервер.")

        # Тестируем скорость загрузки (download), скорости отправки (upload) и пинг
        download_speed = st.download() / 1_000_000  # Преобразуем в Мбит/с
        upload_speed = st.upload() / 1_000_000  # Преобразуем в Мбит/с
        ping = st.results.ping  # Пинг

        # Печатаем результаты
        log_message(f"Скорость загрузки: {download_speed:.2f} Мбит/с")
        log_message(f"Скорость отправки: {upload_speed:.2f} Мбит/с")
        log_message(f"Пинг: {ping} ms")

    except speedtest.SpeedtestException as e:
          log_message(f"Ошибка при тестировании скорости: {e}")
    except Exception as e:
          log_message(f"Неизвестная ошибка: {e}")


   
   
def log_message(message):
    log_text.config(state=NORMAL)  # Разрешаем редактирование
    log_text.insert(END, f"{message}\n")
    log_text.config(state=DISABLED)  # Запрещаем редактирование
    log_text.see(END)  # Прокручиваем вниз

# Автоматическое обновление yt-dlp
def update_yt_dlp():
    try:
        log_message("Проверка обновлений yt-dlp...")
        os.system(f"{yt_dlp_path} -U")
        log_message("yt-dlp обновлён до последней версии.")
        messagebox.showinfo("Обновление", "yt-dlp успешно обновлён.")
    except Exception as e:
        log_message(f"Ошибка при обновлении yt-dlp: {e}")
        messagebox.showerror("Ошибка", f"Не удалось обновить yt-dlp: {e}")

# Функция для записи успешных загрузок
def log_download(link, folder):
    try:
        with open("download_log.txt", "a", encoding="utf-8") as log_file:
            log_file.write(f"Видео: {link}\nСохранено в: {folder}\n\n")
        log_message(f"Видео {link} успешно загружено. Запись добавлена в журнал.")
    except Exception as e:
        log_message(f"Ошибка при записи в журнал: {e}")




# Добавляем виджет для журнала действий
log_label = Label(root, text="Журнал действий:", font=('Arial', 12, 'bold'), bg='#D3D3D3')
log_label.place(x=10, y=220)

log_text = Text(root, height=6, width=75, state=DISABLED, bg="white", fg="black", font=('Arial', 10))
log_text.place(x=10, y=250)

# Добавляем кнопки для новых функций
btn5 = Button(root, text="Проверить скорость", font=('Arial', 10, 'bold'), bd=4, command=check_internet_speed)
btn5.place(x=20, y=380)

btn6 = Button(root, text="Обновить yt-dlp", font=('Arial', 10, 'bold'), bd=4, command=update_yt_dlp)
btn6.place(x=180, y=380)

# Заголовок формы
lb = Label(root, text="---Загрузка видео с YouTube---", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb.pack(pady=15)

lb1 = Label(root, text="Ссылка на видео:", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb1.place(x=10, y=80)

En1 = Entry(root, textvariable=link1, font=('Arial', 15, 'bold'), width=30)
En1.place(x=230, y=80)


btn1 = Button(root, text="Скачать", font=('Arial', 10, 'bold'), bd=4, command=start_download_thread)
btn1.place(x=330, y=120)

btn2 = Button(root, text="Очистить", font=('Arial', 10, 'bold'), bd=4, command=reset)
btn2.place(x=350, y=450)

btn3 = Button(root, text="Выход", font=('Arial', 10, 'bold'), bd=4, command=Exit)
btn3.place(x=450, y=450)


root.mainloop()
