import datetime
import gspread
import boto3
import pytz
from oauth2client.service_account import ServiceAccountCredentials
from slack_sdk import WebClient
import ssl
import os


def notify_to_slack(message,channel='C02Q090JY6M'):
    ssl_context = ssl.create_default_context()
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE

    slack_token = os.environ.get('SERVERLESS_SLACK_BOT_API_TOKEN')
    client = WebClient(slack_token,ssl = ssl_context)
    client.chat_postMessage(
        channel = channel,
        as_user= True,
        text = message
    )

#下記関数で記事数を取得する。
def get_kpi():
    #下記でユーザーを指定。
    client = boto3.client(
        'dynamodb',
        aws_access_key_id = os.environ.get('SERVERLESS_AWS_ACCESS_KEY_ID'),
        aws_secret_access_key = os.environ.get('SERVERLESS_AWS_SECRET_KEY'),
        region_name = 'ap-northeast-1'
    )
    entry_num = client.scan(TableName = 'serverless_blog_entries',Select = 'COUNT')['Count']   #ここでテーブルの記事数を取得。（SQLに少し似ている）
    return entry_num

#下記関数で本日の日付と取得した記事数を基にスプレッドシートを更新
def update_gas(today,entry_num,doc_id):
    keyfile_path = 'serverless-gas-client-secret.json'                                         #クレデンシャルファイルをセット
    scope = ['https://spreadsheets.google.com/feeds']                                          #scope情報（どのように操作をしていいかの情報）をセット
    credentials = ServiceAccountCredentials.from_json_keyfile_name(keyfile_path,scope)         #ここでクレデンシャルファイルの読み込み
    client = gspread.authorize(credentials)                                                    #ここでクレデンシャルを基に権限を取得だと思う

    gfile = client.open_by_key(doc_id)                                                         #下記２つでGSを開く
    worksheet = gfile.sheet1
    list_of_lists = worksheet.get_all_values()                                                 #ここでシート上の全データを取得
    new_row_number = len(list_of_lists) + 1                                                    #現在使用されている行数+1の行を指定

    worksheet.update_cell(new_row_number,1,today)                                              #メソッドupdate_cell(行番号 ,列番号 ,書き込む値)でセル情報をアップデートする。ここでは日付（下の変数の値）
    worksheet.update_cell(new_row_number,2,entry_num)                                          #上と同じメソッドでここでは1日の記事数を取得

#下記関数がメインの流れ
def run_bot():
    doc_id = '1gMlQrt2VJVGhbch6MRF3Mp8KUQPehpcIS_Vwdm2P8Lw'
    today = str(datetime.datetime.now(pytz.timezone('Asia/Tokyo')).date())
    entry_num = get_kpi()
    update_gas(today,entry_num,doc_id)

    message = f'{today}\n記事数:{entry_num}\nhttps://docs.google.com/spreadsheets/d/{doc_id}'
    notify_to_slack(message)

#下記が実行されるインスタンス
if __name__ == '__main__':
    run_bot()
