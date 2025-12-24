from app import create_app, db
from app.model.user import User, UserRepo
from app.model.equipment import Equipment

app = create_app()

with app.app_context():
    db.create_all()
    repo = UserRepo()
    if not repo.get_by_username('admin'):
        admin_user = repo.add('admin', 'password123')
        admin_user.role = 'admin'
        db.session.commit()

if __name__ == "__main__":
    app.run(debug=True)