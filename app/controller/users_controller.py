from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.model.user import UserRepo
from app import db  # Добавляем импорт db для обработки исключений

bp = Blueprint("users", __name__, url_prefix="/users")
repo = UserRepo()


@bp.route("/")
@login_required
def list_users():
    if current_user.role != 'admin':
        flash("У вас нет прав для просмотра пользователей", "error")
        return redirect(url_for('equipment.list_equipment'))

    users = repo.all()
    role_counts = repo.count_by_role()
    return render_template("users/list.html", users=users, role_counts=role_counts)


@bp.route("/", methods=["POST"])
@login_required
def create_user():
    if current_user.role != 'admin':
        flash("У вас нет прав для создания пользователей", "error")
        return redirect(url_for('users.list_users'))

    # Валидация обязательных полей
    username = request.form.get("username", "").strip()
    password = request.form.get("password", "").strip()

    if not username or not password:
        flash("Имя пользователя и пароль обязательны для заполнения", "error")
        return redirect(url_for('users.list_users'))

    if repo.get_by_username(username):
        flash("Имя пользователя уже существует", "error")
        return redirect(url_for('users.list_users'))

    try:
        role = request.form.get("role", "user")
        repo.add(username, password, role)
        flash("Пользователь успешно создан!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при создании пользователя: {str(e)}", "error")

    return redirect(url_for('users.list_users'))


@bp.route("/update", methods=["POST"])
@login_required
def update_user():
    if current_user.role != 'admin':
        flash("У вас нет прав для обновления пользователей", "error")
        return redirect(url_for('users.list_users'))

    try:
        user_id = request.form.get('id')
        username = request.form.get('new_username')
        password = request.form.get('new_password')
        role = request.form.get('new_role')

        # Валидация обязательных полей
        if not username:
            flash("Имя пользователя обязательно для заполнения", "error")
            return redirect(url_for('users.list_users'))

        repo.update(user_id, username=username, password=password, role=role)
        flash("Пользователь успешно обновлен!", "success")
    except Exception as e:
        db.session.rollback()
        flash(f"Ошибка при обновлении пользователя: {str(e)}", "error")

    return redirect(url_for('users.list_users'))


@bp.route("/delete/<int:user_id>", methods=["POST"])
@login_required
def delete_user(user_id):
    if current_user.role != 'admin':
        flash("У вас нет прав для удаления пользователей", "error")
        return redirect(url_for('users.list_users'))

    user = repo.get_by_id(user_id)
    if not user:
        flash("Пользователь не найден", "error")
        return redirect(url_for('users.list_users'))

    if user.username == 'admin':
        flash("Нельзя удалить основного администратора", "error")
        return redirect(url_for('users.list_users'))

    repo.delete(user_id)
    flash("Пользователь успешно удален!", "success")
    return redirect(url_for('users.list_users'))