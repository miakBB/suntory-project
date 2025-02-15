from django.shortcuts import redirect, render
from django.http import HttpResponseNotFound

#ログイン状態に応じてリダイレクト
def home_redirect(request):
    if request.user.is_authenticated:
        return redirect("/dashboard/")
    return redirect("/users/login/")

#404エラーページを表示
def custom_404(request, exception):
    return render(request, "404.html", status=404)
