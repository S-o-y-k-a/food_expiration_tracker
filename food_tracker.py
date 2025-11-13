import tkinter as tk
from tkinter import messagebox
from tkcalendar import DateEntry
from datetime import datetime
import json
import os

DATA_FILE = "products.json"

class ExpiryTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Отслеживание срока годности")
        self.root.geometry("500x500")

        # --- Поля ввода ---
        tk.Label(root, text="Название продукта:").pack(pady=(10, 0))
        self.name_entry = tk.Entry(root, width=40)
        self.name_entry.pack(pady=5)

        tk.Label(root, text="Дата истечения срока:").pack(pady=(10, 0))
        self.date_entry = DateEntry(root, date_pattern='yyyy-mm-dd', width=37)
        self.date_entry.pack(pady=5)

        tk.Button(root, text="Добавить продукт", command=self.add_product).pack(pady=10)

        # --- Список продуктов ---
        self.listbox = tk.Listbox(root, width=60, height=15)
        self.listbox.pack(pady=10, fill=tk.BOTH, expand=True)

        # --- Кнопки управления ---
        tk.Button(root, text="Удалить выбранный", command=self.delete_selected).pack(pady=5)
        tk.Button(root, text="Обновить список", command=self.update_list).pack(pady=5)

        self.products = []
        self.load_data()
        self.update_list()

    # --- Добавление продукта ---
    def add_product(self):
        name = self.name_entry.get().strip()
        date_str = self.date_entry.get_date().strftime("%Y-%m-%d")

        if not name:
            messagebox.showwarning("Ошибка", "Введите название продукта!")
            return

        exp_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        self.products.append({"name": name, "expiry": str(exp_date)})
        self.save_data()
        self.update_list()

        self.name_entry.delete(0, tk.END)

    # --- Удаление выбранного ---
    def delete_selected(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showinfo("Удаление", "Выберите элемент для удаления.")
            return

        index = selected[0]
        del self.products[index]
        self.save_data()
        self.update_list()

    # --- Обновление списка ---
    def update_list(self):
        self.listbox.delete(0, tk.END)
        today = datetime.today().date()
        for p in self.products:
            name = p["name"]
            exp_date = datetime.strptime(p["expiry"], "%Y-%m-%d").date()
            days_left = (exp_date - today).days
            if days_left < 0:
                text = f"❌ {name} — просрочен {abs(days_left)} дн. назад"
            elif days_left == 0:
                text = f"⚠️ {name} — последний день!"
            else:
                text = f"✅ {name} — осталось {days_left} дн."
            self.listbox.insert(tk.END, text)

    # --- Сохранение данных ---
    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.products, f, ensure_ascii=False, indent=2)

    # --- Загрузка данных ---
    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                self.products = json.load(f)
        else:
            self.products = []


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpiryTracker(root)
    root.mainloop()