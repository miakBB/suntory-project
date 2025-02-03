from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

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

    def clean_gender(self):
        """ フォームから送られた性別データを整数に変換 """
        return int(self.cleaned_data['gender'])

#ユーザー情報更新フォーム
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


