import os


#ベースConfigクラス(共通項を抜き出し冗長性をなくす。)
class Config(object):
    DYNAMODB_REGION = 'ap-northeast-1'               #DynamoDBを動かすためのREGION（領域）名
    SESSION_TYPE = 'dynamodb'                                    #セッション保存形式。今回はdynamodb
    SESSION_DYNAMODB_TABLE = 'serverless_blog_sessions'          #セッション保存用テーブル名。
    SESSION_DYNAMODB_REGION = DYNAMODB_REGION                    #セッション保存用テーブルの領域。
    USERNAME = 'HIROKI'


#開発環境用Config設定
class DevelopmentConfig(Config):
    #本番環境では余計な情報を出さないためにFlaseにするのが一般的。
    DEBUG = True

    #下記PynamoDB用の設定
    AWS_ACCESS_KEY_ID = 'AWS_ACCESS_KEY_ID'             #下記2つでDynamoDBサービスにアクセスするためのAWSキー情報
    AWS_SECRET_ACCESS_KEY = 'AWS_SECRET_ACCESS_KEY'
    DYNAMODB_ENDPOINT_URL = 'http://localhost:8000'    #ローカル環境でDynamoDBを動かすためのDynamoDBのホスト名

    #下記セッション用の設定
    SECRET_KEY = 'secret key'
    PASSWORD = 'CHACO26'

    #下記DynamoDB用セッションのAWS保存用設定。基本的にPynamoDBの情報を使用する。
    SESSION_DYNAMODB_KEY_ID = AWS_ACCESS_KEY_ID                  #セッション保存用のKEYIDとKEYの設定。以下2行
    SESSION_DYNAMODB_SECRET = AWS_SECRET_ACCESS_KEY              
    SESSION_DYNAMODB_ENDPOINT_URL = DYNAMODB_ENDPOINT_URL        #DynamoDBのホスト名

#本番環境用Config設定
class ProductionConfig(Config):
    DEBUG = False

    #下記PynamoDB用の設定
    AWS_ACCESS_KEY_ID = os.environ.get('SERVERLESS_AWS_ACCESS_KEY_ID')             #下記2つでDynamoDBサービスにアクセスするためのAWSキー情報
    AWS_SECRET_ACCESS_KEY = os.environ.get('SERVERLESS_AWS_SECRET_KEY')
    DYNAMODB_ENDPOINT_URL = None

    #下記セッション用の設定
    SECRET_KEY = os.environ.get('SERVERLESS_SECRET_KEY')
    PASSWORD = os.environ.get('SERVERLESS_USER_PW')


    #下記DynamoDB用セッションのAWS保存用設定。基本的にPynamoDBの情報を使用する。
    SESSION_DYNAMODB_KEY_ID = AWS_ACCESS_KEY_ID                  #セッション保存用のKEYIDとKEYの設定。以下2行
    SESSION_DYNAMODB_SECRET = AWS_SECRET_ACCESS_KEY              
    SESSION_DYNAMODB_ENDPOINT_URL = DYNAMODB_ENDPOINT_URL        #DynamoDBのホスト名