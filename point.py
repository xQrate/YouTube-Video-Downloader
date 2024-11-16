import yt_dlp
import os
from tkinter import *
from tkinter import messagebox

# Создаем главное окно
root = Tk()
root.title("YouTube Video Downloader")
root.geometry("600x300")
root.config(bg="#D3D3D3")

link1 = StringVar()

# Функция для скачивания видео
def download():
    link = link1.get()
    if not link:
        messagebox.showerror("Ошибка", "Пожалуйста, введите ссылку на видео.")
        return
    try:
        # Получаем путь к папке "Загрузки" текущего пользователя
        download_folder = os.path.join(os.path.expanduser("~"), "Downloads")

        # Указываем настройки для yt-dlp
        ydl_opts = {
            "format": "best",  # Скачиваем лучшее качество
            "outtmpl": os.path.join(download_folder, "%(title)s.%(ext)s")  # Сохраняем файл в папку "Загрузки"
        }

        # Скачиваем видео
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([link])

        messagebox.showinfo("Успех", f"Видео успешно загружено в папку: {download_folder}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка: {e}")

# Функция для очистки поля ввода
def reset():
    link1.set("")

# Функция для выхода из приложения
def Exit():
    root.destroy()

# Заголовок формы
lb = Label(root, text="---Загрузка видео с YouTube---", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb.pack(pady=15)

lb1 = Label(root, text="Ссылка на видео :", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb1.place(x=10, y=80)

En1 = Entry(root, textvariable=link1, font=('Arial', 15, 'bold'), width=30)
En1.place(x=230, y=80)

btn1 = Button(root, text="Скачать", font=('Arial', 10, 'bold'), bd=4, command=download)
btn1.place(x=330, y=130)

btn2 = Button(root, text="Очистить", font=('Arial', 10, 'bold'), bd=4, command=reset)
btn2.place(x=160, y=190)

btn3 = Button(root, text="Выход", font=('Arial', 10, 'bold'), bd=4, command=Exit)
btn3.place(x=250, y=190)

lb = Label(root, text="By RIKA", font=('Arial', 15, 'bold'), bg='#D3D3D3')
lb.place(x=500, y=240)

def animate_text():
    # Получаем текущую позицию x
    x = lb.winfo_x()

    # Если текст не вышел за пределы окна, продолжаем анимацию
    if x < 600:
        lb.place(x=x + 5, y=240)
        # Запускаем анимацию снова через 50 миллисекунд
        root.after(50, animate_text)
    else:
        # Если текст ушел за пределы, возвращаем его на начало
        lb.place(x=-100, y=240)
        root.after(50, animate_text)
        
# Запускаем анимацию
animate_text()


root.mainloop()
