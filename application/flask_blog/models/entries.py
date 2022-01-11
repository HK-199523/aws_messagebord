from datetime import datetime
from pynamodb.models import Model
from pynamodb.attributes import UnicodeAttribute,NumberAttribute,UTCDateTimeAttribute
from flask_blog import app


#下記でモデルクラスを作成
class Entry(Model):
    class Meta:
        table_name = "serverless_blog_entries"                             #ここでテーブル名設定。
        region = app.config.get('DYNAMODB_REGION')                         #ここから以下はconfig.pyでの設定どおり設定していく。
        aws_access_key_id = app.config.get('AWS_ACCESS_KEY_ID')
        aws_secret_access_key = app.config.get('AWS_SECRET_ACCESS_KEY')
        host = app.config.get('DYNAMODB_ENDPOINT_URL')
    id = NumberAttribute(hash_key = True,null = False)                     #値のデータ型を各々で指定。NumberAttributeは数値属性。hash_keyは主キー。nulla=falseで値が必須。
    title = UnicodeAttribute(null = True)                                  #UnicodeAttributeは文字列の設定。null=trueであたいが　必ずでなく値がない場合はnullが設定される。
    text = UnicodeAttribute(null = True)
    created_at = UTCDateTimeAttribute(default = datetime.now())            #UTCDateTimeAttributeはUTCベースのDatetime。defaultは値が指定されなかった場合はデフォルトで設定される値。