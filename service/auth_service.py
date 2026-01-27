from models.user import User


class AuthService:
    def __init__(self, user_repo):
        self.user_repo = user_repo

    def register(self, username, password):
        # Önce bu kullanıcı adı alınmış mı kontrol et
        if self.user_repo.find_by_username(username):
            return False, "Bu kullanici adi zaten alinmis!"

        # Yeni kullanıcı oluştur ve depoya ekle
        new_user = User(username, password)
        self.user_repo.add_user(new_user)
        return True, "Kayit basarili!"