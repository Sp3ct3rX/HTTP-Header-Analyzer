import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import requests
import json
import csv
import pandas as pd
from urllib.parse import urlparse
from datetime import datetime

class HeaderAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Header Analyzer Tool")
        self.root.geometry("800x600")
        self.root.iconbitmap("icon.ico")  # آیکون برنامه

        self.create_widgets()

    def create_widgets(self):
        # توضیح راهنمای استفاده
        instructions = (
            "🔹 چند URL را وارد کن (هر خط یک URL)\n"
            "🔹 روی 'تحلیل' کلیک کن تا Header هر سایت بررسی شود\n"
            "🔹 از گزینه‌های 'ذخیره به JSON' یا 'ذخیره به CSV' استفاده کن\n"
        )
        tk.Label(self.root, text=instructions, fg="gray", justify="left").pack(pady=5)

        # فیلد ورودی URLها
        self.url_text = tk.Text(self.root, height=6, width=90)
        self.url_text.pack(pady=5)

        # دکمه تحلیل
        analyze_btn = ttk.Button(self.root, text="🔍 تحلیل Header", command=self.analyze)
        analyze_btn.pack(pady=5)

        # جدول نمایش نتایج
        self.result_frame = tk.Frame(self.root)
        self.result_frame.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(self.result_frame, columns=("URL", "Server", "Content-Type", "X-Powered-By"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=180)
        self.tree.pack(fill="both", expand=True)

        # دکمه‌های ذخیره
        btn_frame = tk.Frame(self.root)
        btn_frame.pack(pady=10)

        ttk.Button(btn_frame, text="💾 ذخیره به JSON", command=self.save_json).pack(side="left", padx=10)
        ttk.Button(btn_frame, text="📑 ذخیره به CSV", command=self.save_csv).pack(side="left", padx=10)

    def analyze(self):
        self.tree.delete(*self.tree.get_children())  # پاک کردن جدول قبلی
        self.results = []

        urls = self.url_text.get("1.0", "end").strip().splitlines()

        for url in urls:
            if not url.startswith("http"):
                url = "http://" + url

            try:
                r = requests.get(url, timeout=5)
                headers = r.headers
                result = {
                    "URL": url,
                    "Server": headers.get("Server", "N/A"),
                    "Content-Type": headers.get("Content-Type", "N/A"),
                    "X-Powered-By": headers.get("X-Powered-By", "N/A"),
                    "Full-Headers": dict(headers)
                }
                self.results.append(result)
                self.tree.insert("", "end", values=(result["URL"], result["Server"], result["Content-Type"], result["X-Powered-By"]))
            except Exception as e:
                messagebox.showerror("خطا", f"درخواست به {url} ناموفق بود:\n{e}")

    def save_json(self):
        if not self.results:
            messagebox.showwarning("هشدار", "هیچ نتیجه‌ای برای ذخیره وجود ندارد.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".json", filetypes=[("JSON files", "*.json")])
        if file_path:
            with open(file_path, "w", encoding="utf-8") as f:
                json.dump(self.results, f, indent=4, ensure_ascii=False)
            messagebox.showinfo("موفقیت", "فایل JSON با موفقیت ذخیره شد.")

    def save_csv(self):
        if not self.results:
            messagebox.showwarning("هشدار", "هیچ نتیجه‌ای برای ذخیره وجود ندارد.")
            return

        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            df = pd.DataFrame(self.results)
            df.to_csv(file_path, index=False)
            messagebox.showinfo("موفقیت", "فایل CSV با موفقیت ذخیره شد.")


if __name__ == "__main__":
    root = tk.Tk()
    app = HeaderAnalyzerApp(root)
    root.mainloop()
