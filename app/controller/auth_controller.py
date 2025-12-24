from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, logout_user, login_required, current_user
from app.model.user import UserRepo, User

bp = Blueprint("auth", __name__, url_prefix="/auth")
repo = UserRepo()


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('equipment.list_equipment'))

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = repo.get_by_username(username)

        if user and user.check_password(password):
            login_user(user)
            flash("Вход выполнен успешно!", "success")
            session['logged_in'] = True
            session['user'] = user.username
            session['role'] = user.role
            return redirect(url_for('equipment.list_equipment'))
        else:
            flash("Неверное имя пользователя или пароль", "error")

    return render_template("auth/login.html")


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    flash("Вы успешно вышли из системы.", "info")
    return redirect(url_for('main.index'))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if repo.get_by_username(username):
            flash("Имя пользователя уже существует", "error")
        else:
            repo.add(username, password)
            flash("Регистрация прошла успешно! Пожалуйста, войдите в систему.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")