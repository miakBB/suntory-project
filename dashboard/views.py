from django.shortcuts import render, redirect
from django.utils.timezone import now
def dashboard(request):
    return render(request,'dashboard.html') 