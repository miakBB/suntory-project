from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

User = get_user_model()

#ログインフォーム
class UserLoginForm(AuthenticationForm):
    username = forms.EmailField(label="メールアドレス")  # `username` の代わりに `email` を使う

#ユーザー登録フォーム
class UserRegistrationForm(UserCreationForm):
    GENDER_CHOICES = [
        ('9', 'その他'),
        ('1', '男性'),
        ('2', '女性'),
    ]

    email = forms.EmailField(required=True)
    password1 = forms.CharField(
        label="パスワード",
        widget=forms.PasswordInput,
        help_text="8文字以上で、大文字・小文字・数字・記号を含めてください。",
    )
    password2 = forms.CharField(
        label="パスワード（確認）",
        widget=forms.PasswordInput,
        help_text="確認のため、再度パスワードを入力してください。",
    )
    gender = forms.ChoiceField(
        choices=GENDER_CHOICES,
        initial='9',
        label="性別"
    )

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2', 'username', 'weight', 'birth_date', 'gender')

    def clean_username(self):
        #username` のユニークチェックを回避しつつバリデーションを適用
        username = self.cleaned_data.get("username", "").strip()

        # 空文字の場合のデフォルト値 念の為
        if not username:
            username = "名無しさん"

        # 長さチェック
        if len(username) > 15:
            raise ValidationError("ユーザー名は15文字以内で入力してください。")

        # 正規表現バリデーション（記号を禁止）
        validator = RegexValidator(
            regex=r'^[a-zA-Z0-9ぁ-んァ-ン一-龥ー]+$',
            message="記号は使用できません。"
        )
        #例外が発生した場合はそのまま Django のバリデーションエラーに
        validator(username)  

        return username

    def clean_gender(self):
        #性別のデータを整数に変換
        return int(self.cleaned_data['gender'])

#ユーザー情報更新フォーム
"""
class UserUpdateForm(forms.ModelForm):
    email=forms.EmailField(required=True) #メールアドレスを必須にする文

    class Meta:
        model=get_user_model()
        fields = ( 'email', 'birth_date', 'gender', 'weight')
        labels = {
            'email':'メールアドレス',
            'birth_date':'生年月日',
            'gender':'性別',
            'weight':'体重',
        }    
"""

class UserUpdateForm(forms.ModelForm):
    GENDER_CHOICES = [
        ('9', 'その他'),
        ('1', '男性'),
        ('2', '女性'),
    ]

    email = forms.EmailField(required=True)
    username = forms.CharField(
        max_length=15,
        required=True,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9ぁ-んァ-ン一-龥ー]+$',
                message="記号は使用できません。"
            )
        ],
    )
    weight = forms.FloatField(min_value=1, max_value=150, required=True)
    birth_date = forms.DateField(required=True)
    gender = forms.ChoiceField(choices=GENDER_CHOICES, required=True, initial='9')

    class Meta:
        model = User
        fields = ('email', 'username', 'weight', 'birth_date', 'gender')

    def clean_gender(self):
        return int(self.cleaned_data['gender'])

    def clean_username(self):
        """ユーザー名のバリデーション"""
        username = self.cleaned_data.get("username", "").strip()
        if not username:
            raise ValidationError("ユーザー名を入力してください。")
        return username