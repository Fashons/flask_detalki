from flask import Blueprint, request, render_template, redirect, url_for, flash
from flask_login import login_required, current_user
from app.model.equipment import EquipmentRepo
from app.model.user import UserRepo
from datetime import datetime
import json

bp = Blueprint("equipment", __name__, url_prefix="/equipment")
equipment_repo = EquipmentRepo()
user_repo = UserRepo()


@bp.route("/")
@login_required
def list_equipment():
    # Получаем параметры фильтрации из запроса
    filter_type = request.args.get('type')
    filter_status = request.args.get('status')
    filter_location = request.args.get('location')

    # Фильтрация оборудования
    equipment_list = equipment_repo.filter_by(
        type=filter_type,
        status=filter_status,
        location=filter_location
    )

    # Статистика по статусам и типам
    status_counts = equipment_repo.count_by_status()
    type_counts = equipment_repo.count_by_type()

    # Все возможные типы и статусы для фильтров
    all_types = ['Компьютер', 'Ноутбук', 'Монитор', 'Принтер', 'Сканер', 'Сервер', 'Роутер']
    all_statuses = ['available', 'in_use', 'in_repair', 'retired']
    all_locations = ['Офис 101', 'Офис 102', 'Офис 201', 'Склад', 'Бухгалтерия', 'ИТ-отдел']
    all_users = user_repo.all()

    return render_template("equipment/list.html",
                           equipment=equipment_list,
                           status_counts=status_counts,
                           type_counts=type_counts,
                           all_types=all_types,
                           all_statuses=all_statuses,
                           all_locations=all_locations,
                           all_users=all_users)


@bp.route("/", methods=["POST"])
@login_required
def create_equipment():
    if current_user.role not in ['admin', 'manager']:
        flash("У вас нет прав для добавления оборудования", "error")
        return redirect(url_for('equipment.list_equipment'))

    try:
        name = request.form.get("name")
        type_ = request.form.get("type")
        model = request.form.get("model")
        inventory_number = request.form.get("inventory_number")
        status = request.form.get("status", "available")
        location = request.form.get("location")
        purchase_date = request.form.get("purchase_date")
        price = request.form.get("price")
        specification = request.form.get("specification")
        user_id = request.form.get("user_id") or None

        if purchase_date:
            purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()

        if price:
            price = float(price)

        equipment_repo.add(
            name=name,
            type=type_,
            model=model,
            inventory_number=inventory_number,
            status=status,
            location=location,
            purchase_date=purchase_date,
            price=price,
            specification=specification,
            user_id=user_id
        )
        flash("Оборудование успешно добавлено!", "success")
    except Exception as e:
        flash(f"Ошибка при добавлении оборудования: {str(e)}", "error")

    return redirect(url_for('equipment.list_equipment'))


@bp.route("/delete/<int:equipment_id>", methods=["POST"])
@login_required
def delete_equipment(equipment_id):
    if current_user.role != 'admin':
        flash("У вас нет прав для удаления оборудования", "error")
        return redirect(url_for('equipment.list_equipment'))

    equipment = equipment_repo.get_by_id(equipment_id)
    if not equipment:
        flash("Оборудование не найдено", "error")
        return redirect(url_for('equipment.list_equipment'))

    equipment_repo.delete(equipment_id)
    flash("Оборудование успешно удалено!", "success")
    return redirect(url_for('equipment.list_equipment'))


@bp.route("/update", methods=["POST"])
@login_required
def update_equipment():
    if current_user.role not in ['admin', 'manager']:
        flash("У вас нет прав для обновления оборудования", "error")
        return redirect(url_for('equipment.list_equipment'))

    try:
        equipment_id = request.form.get('id')
        name = request.form.get('new_name')
        type_ = request.form.get('new_type')
        model = request.form.get('new_model')
        inventory_number = request.form.get('new_inventory_number')
        status = request.form.get('new_status')
        location = request.form.get('new_location')
        purchase_date = request.form.get('new_purchase_date')
        price = request.form.get('new_price')
        specification = request.form.get('new_specification')
        user_id = request.form.get('new_user_id') or None

        if purchase_date:
            purchase_date = datetime.strptime(purchase_date, '%Y-%m-%d').date()

        if price:
            price = float(price)

        equipment_repo.update(
            equipment_id=equipment_id,
            name=name,
            type=type_,
            model=model,
            inventory_number=inventory_number,
            status=status,
            location=location,
            purchase_date=purchase_date,
            price=price,
            specification=specification,
            user_id=user_id
        )
        flash("Оборудование успешно обновлено!", "success")
    except Exception as e:
        flash(f"Ошибка при обновлении оборудования: {str(e)}", "error")

    return redirect(url_for('equipment.list_equipment'))