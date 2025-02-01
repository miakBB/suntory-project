from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from .managers import UserManager # カスタムマネージャーをインポート

# デフォルトのユーザーモデルを継承して作成
class User(AbstractUser):

    #  AbstractUser(デフォルト) から不要なフィールドを削除
    first_name = None
    last_name = None  

    # 新規追加フィールド
    birth_date = models.DateField(default="1900-01-01", blank=True)  # 生年月日（未入力時は 1900-01-01）
    gender = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(9)])  # 性別（1〜9 の範囲で制限）
    weight = models.FloatField()  # 体重（浮動小数点 少数第一位までそうてい)

    objects = UserManager()  # カスタムマネージャーを適用

    def __str__(self):
        return self.username


"""
User テーブルのフィールド一覧（Django の AbstractUser を継承）

| フィールド名      | 型                          | 説明                                       | 追加・削除 |
|------------------|----------------------------|------------------------------------------|------------|
| id              | AutoField (PK)             | ユーザーの主キー                           | デフォルト |
| password        | CharField (ハッシュ化)       | パスワード（暗号化された値が入る）          | デフォルト |
| last_login      | DateTimeField               | 最終ログイン日時                          | デフォルト |
| is_superuser    | BooleanField                | 管理者権限（管理画面で設定）               | デフォルト |
| username        | CharField (ユニーク)        | ユーザー名                                | デフォルト |
| email          | EmailField (ユニーク)       | メールアドレス（ログインIDとして使用可）    | デフォルト |
| is_staff       | BooleanField                | Django管理画面のアクセス可否               | デフォルト |
| is_active      | BooleanField                | アカウントの有効/無効                      | デフォルト |
| date_joined    | DateTimeField               | 登録日時（ユーザー作成時に自動セット）       | デフォルト |
| birth_date     | DateField                   | 生年月日（未入力時は "1900-01-01"）         | **追加** |
| gender         | PositiveSmallIntegerField   | 性別（1〜9 の範囲で制限）                  | **追加** |
| weight         | FloatField                  | 体重（必須）                              | **追加** |

これでログインはdajngoのデフォルトのやつを使える 多分
"""

