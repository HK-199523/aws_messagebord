from flask import request,redirect,url_for,render_template,flash,session
from flask_blog import app
from flask_login import login_user,logout_user
from flask_blog.models.users import User


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':                                      #POSTリクエストの時にユーザー名とパスワードを確認。GETリクエストなら元のページに戻る。
        if request.form['username'] != app.config['USERNAME']:        #下記のパスワード確認のものと一緒でconfigファイルで設定したユーザー名とパスワードが同じか確認。
            flash('ユーザー名が異なります。')                           #ちがうならログインを拒否する。
        elif request.form['password'] != app.config['PASSWORD']:
            flash('パスワードが異なります。')
        else:
            login_user(User(request.form['username']))                #login_user()でユーザー名毎にログインセッションを与える。これによりログインの有無を管理する。
            flash('ログインしました。')
            return redirect(url_for('show_entries'))
    return render_template('login.html')

@app.route('/logout')
def logout():
    logout_user()
    flash('ログアウトしました。')
    return redirect(url_for('login'))

@app.errorhandler(404)                                                #存在しないurlにaアクセスした時404エラーを発生するのでその後に呼び出される処理。
def non_existant_route(error):
    return redirect(url_for('login'))