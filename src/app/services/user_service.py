from app import db
from app.models import User
from app.schemas.user import UserSchema

class UserService:
    def __init__(self):
        self.user_schema = UserSchema()
        
    def get_all_users(self):
        users = User.query.all()
        return self.user_schema.dump(users, many=True)
    
    def get_user_by_id(self, user_id):
        user = User.query.get(user_id)
        return self.user_schema.dump(user)
    
    def create_user(self, user_data):
        user = User(**user_data)
        db.session.add(user)
        db.session.commit()
        return self.user_schema.dump(user)
    
    def update_user(self, user_id, user_data):
        user = User.query.get(user_id)
        for key, value in user_data.items():
            setattr(user, key, value)
        db.session.commit()
        return self.user_schema.dump(user)
    
    def delete_user(self, user_id):
        user = User.query.get(user_id)
        db.session.delete(user)
        db.session.commit()
