from django.contrib.auth.models import BaseUserManager
from django.core.exceptions import ValidationError

# ユーザーマネージャー スーパーユーザー作成用に作ったけど、一般ユーザーも作成できる
class UserManager(BaseUserManager):

    # 一般ユーザー作成
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError("メールアドレスは必須です")
        
        if self.model.objects.filter(email=email).exists():
            raise ValidationError("このメールアドレスは既に使用されています")

        email = self.normalize_email(email)

        # `extra_fields` のデフォルト値を設定
        extra_fields.setdefault("birth_date", "1900-01-01")  # デフォルト値
        extra_fields.setdefault("gender", 9)  # デフォルト値（9 = それ以外）
        extra_fields.setdefault("weight", 60.0)  # デフォルト値

        # `gender` のバリデーション（1, 2, 9 のみ許可）
        if extra_fields["gender"] not in [1, 2, 9]:
            raise ValueError("性別の値が不正です")

        # `weight` のバリデーション（0 以上）
        if extra_fields["weight"] <= 0:
            raise ValueError("weight は 0 以上である必要があります")

        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)  # パスワードをハッシュ化
        user.save(using=self._db)
        return user

    # スーパーユーザー作成
    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("スーパーユーザーは `is_staff=True` である必要があります")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("スーパーユーザーは `is_superuser=True` である必要があります")

        return self.create_user(username, email, password, **extra_fields)
