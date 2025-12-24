from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

bp = Blueprint("main", __name__)

@bp.route("/")
def index():
    # Всегда показываем главную страницу, но с разным контентом для аутентифицированных/неаутентифицированных
    return render_template("index.html", authenticated=current_user.is_authenticated)

@bp.route("/home")
@login_required
def home():
    # Эта страница может использоваться как дашборд для аутентифицированных пользователей
    return render_template("index.html", authenticated=True)