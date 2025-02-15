from django.shortcuts import render, redirect
from .forms import UserRegistrationForm, UserUpdateForm, UserLoginForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy


#カスタムログインビュー(メールアドレス)
class CustomLoginView(LoginView):
    authentication_form = UserLoginForm
    template_name = 'login.html'  # 使用するテンプレートを指定
    def get_success_url(self):
        return reverse_lazy('dashboard')
    
#ユーザー登録
def register(request):
    backend_errors = None  # エラーメッセージ用

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)  # 一旦保存せずにデータを取得
                user.gender = int(form.cleaned_data['gender'])  # 性別を整数に変換
                user.save()

                login(request, user)
                return redirect("/dashboard/")  # ダッシュボードへリダイレクト
            
            except Exception as e:
                backend_errors = str(e)  # 予期せぬエラーが発生した場合
                print(f"保存エラー: {backend_errors}")

        else:
            backend_errors = form.errors.as_json()  # バリデーションエラー
            print(f"フォームのバリデーションエラー: {backend_errors}")

    else:
        form = UserRegistrationForm()

    return render(request, 'register.html', {'form': form, 'backend_errors': backend_errors})

#ユーザー情報更新
"""
@login_required
def update(request):
    user = request.user
    success = False  # 更新成功フラグ
    backend_errors = None  # エラーメッセージ

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
                success = True  # 更新成功
            except Exception as e:
                backend_errors = str(e)  # 予期しないエラー
        else:
            backend_errors = form.errors.as_json()  # バリデーションエラー

    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update.html', {'form': form, 'success': success, 'backend_errors': backend_errors})
"""

from django.http import JsonResponse

@login_required
def update(request):
    user = request.user
    success = False  
    backend_errors = None

    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            try:
                form.save()
                success = True
            except Exception as e:
                backend_errors = str(e)
        else:
            backend_errors = form.errors.as_json()

        # AJAX の場合は JSON を返す
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': success, 'errors': backend_errors})
    else:
        form = UserUpdateForm(instance=user)

    return render(request, 'update.html', {'form': form, 'success': success, 'backend_errors': backend_errors})
