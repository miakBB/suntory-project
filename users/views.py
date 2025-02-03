from django.shortcuts import render,redirect
from .forms import UserRegistrationForm,UserUpdateForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request,user) #登録後にログイン
            return redirect('login_main')#メインログインへリダイレクト
    else:
        form = UserRegistrationForm()
    return render(request,'register.html',{'form':form}) 

@login_required
def mypage(request):
    user = request.user
    if request.method == 'POST':
        form = UserUpdateForm(request.POST)
        if form.is_valid():
            #ユーザー情報更新
            user.email = form.cleaned_data.get('email')
            user.birth_date = form.cleaned_data.get('birth_date')
            user.gender = form.cleaned_data.get('gender')     
            user.weight = form.cleaned_data.get('weight')
            user.save()
            return redirect('mypage') #マイページへリダイレクト
    else:
        #ユーザーデータをフォームにセット
        data = {
            'username':user.username,
            'email':user.email,
            'birth_date':user.birth_date,
            'gender':user.gender,
            'weight':user.weight,
        }
        form = UserUpdateForm(data)
    return render(request,'mypage.html',{'form':form}) 