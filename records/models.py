from django.db import models

#飲料のカテゴリ-テーブル (コーヒー飲料、お茶飲料など,引用：https://products.suntory.co.jp/softdrink/ingredient.html)
class DrinkCategory(models.Model):
    name = models.CharField(max_length=20, unique=True)

    def __str__(self):
        return self.name

#飲料の情報テーブル　(こちらも引用:https://products.suntory.co.jp/softdrink/ingredient.html)
class Drink(models.Model):
    category = models.ForeignKey(DrinkCategory, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    volume = models.FloatField()  # 一本あたりの容量（ml）
    unit = models.FloatField()  # 成分表示の単位（XXmlあたり）
    kcal = models.FloatField() # カロリー
    caffeine = models.FloatField()  # カフェイン含有量（mg）
    salt = models.FloatField()  # 塩分（g）
    sugars = models.FloatField()  # 糖類（g）

    def __str__(self):
        return self.name

#摂取記録テーブル
class Consumption(models.Model):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE)  # ユーザーと紐付け
    drink = models.ForeignKey(Drink, on_delete=models.CASCADE) # 飲料と紐付け
    consumed_at = models.DateTimeField()  # 記録日時 (ユーザーが入力する　先日の飲んだ飲料の記録などのため)
    quantity = models.FloatField()  # 飲んだ量（ml）
    created_at = models.DateTimeField(auto_now_add=True)  # 作成日時(自動で現在日時が入る)

    def __str__(self):
        return f"{self.user} - {self.drink.name} ({self.consumed_at}) {self.quantity}"

"""
def __str__(self):について
 通常、print(オブジェクト名)でオブジェクトを表示すると、オブジェクトのクラス名とIDが表示される。
  例）<Drink: Drink object (1)>
  __str__メソッドをオーバーライドすることで、オブジェクトを文字列に変換する際の挙動を変更できる。
  例) 緑茶 伊右衛門 BLACK (Drink.name である商品名が表示される)
"""