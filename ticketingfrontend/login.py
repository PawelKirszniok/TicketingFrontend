from ticketingfrontend import login_manager, database_service
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    user = database_service.get_user(user_id)
    return User(user)


class User(UserMixin):

    def __init__(self, json_data):

        self.login = json_data['login']
        self.name = json_data['name']
        self.password = json_data['password']
        self.picture = json_data['picture']
        self.position = json_data['position']
        self.email = json_data['email']
        self.id = json_data['id']
