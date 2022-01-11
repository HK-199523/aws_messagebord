#全モジュールを結合させたまとめ役のポジション

from flask import Flask
from flask_login import LoginManager
from flask_sessionstore import Session
import os

#下記でconfig情報を定義
config = {
    'default':'flask_blog.config.DevelopmentConfig',
    'development':'flask_blog.config.DevelopmentConfig',
    'production':'flask_blog.config.ProductionConfig'
}
#下記で環境読み込む。
app = Flask(__name__)
config_name = os.getenv('SERVERLESS_BLOG_CONFIG','default') #第一引数の環境変数値が読み込みがない場合はdefaultを読み込む。環境変数の値をconfig_nameに代入。（今回は'flask_blog.config.ProductionConfig')
app.config.from_object(config[config_name])             #config.pyの上記で環境変数の値のクラス内にある大文字の変数と値をオブジェクトとして取得してapp内にあるconfigに取得。
Session(app)                                            #アプリケーションと紐づける＝

login_manager = LoginManager()                          #以下2行でアプリケーションと紐づける事で全箇所でログイン機能が有効になる。
login_manager.init_app(app)

from flask_blog.lib.utils import setup_auth             #ユーザーローダの実装
setup_auth(login_manager)


from flask_blog.views import views,entries
login_manager.login_view = "login"                      #ログインしていない場合はこれで指定のビューにリダイレクトする。今回はloginビュー
login_manager.login_message = 'ログインしてください。'    #flashでログインしてくださいとメッセージを出す。