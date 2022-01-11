#ユーザーローダー（ログインセッション受け取った時セッションに含まれるユーザーIDからユーザ情報を取得しチェックする事）の実装
from flask_blog.models.users import User


def setup_auth(login_manager):
    @login_manager.user_loader
    def load_user(user_id):
        return User(user_id)