
from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import sqlite3
import hashlib
import secrets
import hmac
import re

app = FastAPI(title="BADAM AI")

DATABASE = "badam.db"


def create_database():
    connection = sqlite3.connect(DATABASE)
    connection.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL COLLATE NOCASE UNIQUE,
            contact TEXT NOT NULL UNIQUE,
            password_hash TEXT NOT NULL,
            salt TEXT NOT NULL
        )
    """)
    connection.commit()
    connection.close()


create_database()


class RegisterData(BaseModel):
    username: str
    password: str
    contact: str


class LoginData(BaseModel):
    username: str
    password: str


def hash_password(password, salt):
    return hashlib.pbkdf2_hmac(
        "sha256",
        password.encode("utf-8"),
        bytes.fromhex(salt),
        310000
    ).hex()


@app.get("/")
def home():
    return {
        "name": "BADAM AI",
        "status": "online",
        "message": "سلام! بادام آماده است."
    }


@app.post("/register")
def register(data: RegisterData):
    username = data.username.strip()
    password = data.password
    contact = data.contact.strip()

    if not username or not contact:
        raise HTTPException(status_code=400, detail="همه قسمت ها را پر کنید")

    if len(password) < 8:
        raise HTTPException(status_code=400, detail="رمز باید حداقل ۸ کاراکتر باشد")

    if (
        not password.isascii()
        or not any(c.isalpha() for c in password)
        or any(c.isspace() for c in password)
    ):
        raise HTTPException(status_code=400, detail="رمز باید حروف انگلیسی داشته باشد")

    if "@" in contact:
        if not re.fullmatch(r"[^@\s]+@[^@\s]+\.[^@\s]+", contact):
            raise HTTPException(status_code=400, detail="ایمیل معتبر نیست")
    else:
        digits = re.sub(r"[\s+-]", "", contact)
        if not digits.isdigit() or not 10 <= len(digits) <= 15:
            raise HTTPException(status_code=400, detail="شماره تماس معتبر نیست")

    salt = secrets.token_hex(16)
    password_hash = hash_password(password, salt)

    connection = sqlite3.connect(DATABASE)

    try:
        connection.execute(
            """
            INSERT INTO users
            (username, contact, password_hash, salt)
            VALUES (?, ?, ?, ?)
            """,
            (username, contact, password_hash, salt)
        )
        connection.commit()

    except sqlite3.IntegrityError:
        raise HTTPException(
            status_code=409,
            detail="این نام کاربری یا شماره تماس قبلاً ثبت شده"
        )

    finally:
        connection.close()

    return {
        "success": True,
        "message": "حساب کاربری با موفقیت ساخته شد"
    }


@app.post("/login")
def login(data: LoginData):
    connection = sqlite3.connect(DATABASE)

    user = connection.execute(
        """
        SELECT password_hash, salt
        FROM users
        WHERE username = ? COLLATE NOCASE
        """,
        (data.username.strip(),)
    ).fetchone()

    connection.close()

    if user is None:
        raise HTTPException(
            status_code=401,
            detail="نام کاربری یا رمز عبور اشتباه است"
        )

    saved_hash, salt = user
    entered_hash = hash_password(data.password, salt)

    if not hmac.compare_digest(saved_hash, entered_hash):
        raise HTTPException(
            status_code=401,
            detail="نام کاربری یا رمز عبور اشتباه است"
        )

    return {
        "success": True,
        "message": "ورود موفقیت آمیز بود",
        "username": data.username
    }


@app.get("/app", response_class=HTMLResponse)
def mobile_app():
    return """
    <!DOCTYPE html>
    <html lang="fa" dir="rtl">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>BADAM AI</title>
    </head>
    <body style="background:#071923;color:white;text-align:center;font-family:Tahoma;padding:40px 15px">
        <h1 style="color:#00E5A8;font-size:55px">🌰 بادام</h1>
        <h3>به BADAM AI خوش آمدید</h3>
        <p>نسخه آزمایشی بادام</p>
        <p style="color:#35C9E8">هوش مصنوعی اختصاصی شما</p>
    </body>
    </html>
    """
