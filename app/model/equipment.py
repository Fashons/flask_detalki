from app import db
from datetime import datetime


class Equipment(db.Model):
    __tablename__ = 'equipment'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # Компьютер, ноутбук, монитор и т.д.
    model = db.Column(db.String(100), nullable=False)
    inventory_number = db.Column(db.String(50), unique=True, nullable=False)
    status = db.Column(db.String(20), default='available')  # available, in_use, in_repair, retired
    location = db.Column(db.String(100))
    purchase_date = db.Column(db.Date, default=datetime.utcnow)
    price = db.Column(db.Float)
    specification = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Equipment {self.name} ({self.inventory_number})>'


class EquipmentRepo:
    def all(self):
        return Equipment.query.all()

    def add(self, name, type, model, inventory_number, status='available', location=None,
            purchase_date=None, price=None, specification=None, user_id=None):
        equipment = Equipment(
            name=name,
            type=type,
            model=model,
            inventory_number=inventory_number,
            status=status,
            location=location,
            purchase_date=purchase_date,
            price=price,
            specification=specification,
            user_id=user_id
        )
        db.session.add(equipment)
        db.session.commit()
        return equipment

    def delete(self, equipment_id):
        equipment = Equipment.query.get(equipment_id)
        if equipment:
            db.session.delete(equipment)
            db.session.commit()
        return equipment

    def update(self, equipment_id, name=None, type=None, model=None, inventory_number=None,
               status=None, location=None, purchase_date=None, price=None, specification=None, user_id=None):
        equipment = Equipment.query.get(equipment_id)
        if not equipment:
            return None

        if name:
            equipment.name = name
        if type:
            equipment.type = type
        if model:
            equipment.model = model
        if inventory_number:
            equipment.inventory_number = inventory_number
        if status:
            equipment.status = status
        if location:
            equipment.location = location
        if purchase_date:
            equipment.purchase_date = purchase_date
        if price:
            equipment.price = price
        if specification:
            equipment.specification = specification
        if user_id:
            equipment.user_id = user_id

        db.session.commit()
        return equipment

    def get_by_id(self, equipment_id):
        return Equipment.query.get(equipment_id)

    def filter_by(self, type=None, status=None, location=None):
        query = Equipment.query
        if type:
            query = query.filter_by(type=type)
        if status:
            query = query.filter_by(status=status)
        if location:
            query = query.filter_by(location=location)
        return query.all()

    def count_by_status(self):
        from sqlalchemy import func
        return db.session.query(Equipment.status, func.count(Equipment.id)).group_by(Equipment.status).all()

    def count_by_type(self):
        from sqlalchemy import func
        return db.session.query(Equipment.type, func.count(Equipment.id)).group_by(Equipment.type).all()