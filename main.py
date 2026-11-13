
import customtkinter as ctk
import requests

SERVER_URL = "http://127.0.0.1:8000"

ctk.set_appearance_mode("dark")

app = ctk.CTk()
app.title("بادام | BADAM AI")
app.geometry("1000x700")
app.configure(fg_color="#071923")


def clear_page():
    for widget in app.winfo_children():
        widget.destroy()


def home_page():
    clear_page()

    ctk.CTkLabel(
        app,
        text="بادام",
        font=("Tahoma", 42, "bold"),
        text_color="#00E5A8"
    ).pack(pady=(80, 15))

    ctk.CTkLabel(
        app,
        text="هوش مصنوعی اختصاصی شما",
        font=("Tahoma", 18),
        text_color="#35C9E8"
    ).pack(pady=10)

    box = ctk.CTkFrame(
        app,
        width=430,
        height=300,
        fg_color="#102D3A",
        corner_radius=25
    )
    box.pack(pady=40)
    box.pack_propagate(False)

    ctk.CTkLabel(
        box,
        text="به بادام خوش آمدید",
        font=("Tahoma", 23, "bold")
    ).pack(pady=35)

    ctk.CTkButton(
        box,
        text="ثبت‌نام",
        width=280,
        height=50,
        fg_color="#00A878",
        command=register_page
    ).pack(pady=12)

    ctk.CTkButton(
        box,
        text="ورود",
        width=280,
        height=50,
        fg_color="#087FA5",
        command=login_page
    ).pack(pady=12)


def register_page():
    clear_page()

    ctk.CTkLabel(
        app,
        text="ساخت حساب کاربری",
        font=("Tahoma", 30, "bold"),
        text_color="#00E5A8"
    ).pack(pady=30)

    box = ctk.CTkFrame(
        app,
        width=460,
        height=480,
        fg_color="#102D3A",
        corner_radius=22
    )
    box.pack(pady=10)
    box.pack_propagate(False)

    name = ctk.CTkEntry(
        box,
        width=340,
        height=45,
        placeholder_text="نام کاربری",
        justify="right"
    )
    name.pack(pady=(35, 12))

    password = ctk.CTkEntry(
        box,
        width=340,
        height=45,
        placeholder_text="رمز عبور انگلیسی",
        show="*",
        justify="right"
    )
    password.pack(pady=12)

    contact = ctk.CTkEntry(
        box,
        width=340,
        height=45,
        placeholder_text="شماره موبایل یا ایمیل",
        justify="right"
    )
    contact.pack(pady=12)

    message = ctk.CTkLabel(
        box,
        text="",
        font=("Tahoma", 13)
    )
    message.pack(pady=12)

    def submit():
        n = name.get().strip()
        p = password.get()
        c = contact.get().strip()

        if not n or not p or not c:
            message.configure(
                text="همه قسمت‌ها را پر کنید",
                text_color="#FF7777"
            )
            return

        message.configure(text="در حال اتصال به سرور...")

        try:
            response = requests.post(
                SERVER_URL + "/register",
                json={
                    "username": n,
                    "password": p,
                    "contact": c
                },
                timeout=10
            )

            result = response.json()

            if response.status_code == 200:
                message.configure(
                    text="حساب با موفقیت ساخته شد!",
                    text_color="#00E5A8"
                )
            else:
                message.configure(
                    text=result.get("detail", "خطا در ثبت‌نام"),
                    text_color="#FF7777"
                )

        except requests.exceptions.RequestException:
            message.configure(
                text="اتصال به سرور برقرار نشد",
                text_color="#FF7777"
            )

    ctk.CTkButton(
        box,
        text="ثبت‌نام",
        width=340,
        height=48,
        fg_color="#00A878",
        command=submit
    ).pack(pady=8)

    ctk.CTkButton(
        box,
        text="بازگشت",
        command=home_page
    ).pack(pady=8)


def chat_page(username):
    clear_page()

    ctk.CTkLabel(
        app,
        text="بادام | BADAM AI",
        font=("Tahoma", 32, "bold"),
        text_color="#00E5A8"
    ).pack(pady=20)

    ctk.CTkLabel(
        app,
        text=f"خوش آمدی، {username}",
        font=("Tahoma", 16),
        text_color="#35C9E8"
    ).pack(pady=5)

    chat = ctk.CTkTextbox(
        app,
        width=850,
        height=450,
        fg_color="#102D3A",
        font=("Tahoma", 15),
        wrap="word"
    )
    chat.pack(padx=30, pady=15, fill="both", expand=True)

    def add_message(sender, message):
        chat.configure(state="normal")
        chat.insert("end", f"{sender}:\n{message}\n\n")
        chat.configure(state="disabled")
        chat.see("end")

    input_frame = ctk.CTkFrame(
        app,
        fg_color="#102D3A"
    )
    input_frame.pack(fill="x", padx=25, pady=10)

    entry = ctk.CTkEntry(
        input_frame,
        height=45,
        placeholder_text="پیامت رو برای بادام بنویس..."
    )
    entry.pack(side="right", fill="x", expand=True, padx=10, pady=10)

    def send_message():
        message = entry.get().strip()

        if not message:
            return

        add_message("شما", message)

        add_message(
            "بادام",
            "پیامت دریافت شد! موتور هوش مصنوعی من هنوز متصل نشده است."
        )

        entry.delete(0, "end")

    ctk.CTkButton(
        input_frame,
        text="ارسال",
        width=100,
        height=45,
        fg_color="#00A878",
        command=send_message
    ).pack(side="left", padx=10, pady=10)

    entry.bind(
        "<Return>",
        lambda event: send_message()
    )

    ctk.CTkButton(
        app,
        text="خروج از حساب",
        fg_color="#087FA5",
        command=home_page
    ).pack(pady=10)


def login_page():
    clear_page()

    ctk.CTkLabel(
        app,
        text="ورود به حساب کاربری",
        font=("Tahoma", 30, "bold"),
        text_color="#00E5A8"
    ).pack(pady=40)

    box = ctk.CTkFrame(
        app,
        width=460,
        height=370,
        fg_color="#102D3A",
        corner_radius=22
    )
    box.pack(pady=10)
    box.pack_propagate(False)

    name = ctk.CTkEntry(
        box,
        width=340,
        height=45,
        placeholder_text="نام کاربری",
        justify="right"
    )
    name.pack(pady=(45, 15))

    password = ctk.CTkEntry(
        box,
        width=340,
        height=45,
        placeholder_text="رمز عبور",
        show="*",
        justify="right"
    )
    password.pack(pady=15)

    message = ctk.CTkLabel(
        box,
        text="",
        font=("Tahoma", 13)
    )
    message.pack(pady=12)

    def submit():
        n = name.get().strip()
        p = password.get()

        if not n or not p:
            message.configure(
                text="نام کاربری و رمز را وارد کنید",
                text_color="#FF7777"
            )
            return

        message.configure(text="در حال بررسی حساب...")

        try:
            response = requests.post(
                SERVER_URL + "/login",
                json={
                    "username": n,
                    "password": p
                },
                timeout=10
            )

            result = response.json()

            if response.status_code == 200:
                chat_page(n)
            else:
                message.configure(
                    text=result.get("detail", "ورود ناموفق بود"),
                    text_color="#FF7777"
                )

        except requests.exceptions.RequestException:
            message.configure(
                text="اتصال به سرور برقرار نشد",
                text_color="#FF7777"
            )

    ctk.CTkButton(
        box,
        text="ورود",
        width=340,
        height=48,
        fg_color="#087FA5",
        command=submit
    ).pack(pady=8)

    ctk.CTkButton(
        box,
        text="بازگشت",
        command=home_page
    ).pack(pady=8)


home_page()
app.mainloop()
