from django.shortcuts import render, redirect
from .models import Drink, DrinkCategory, Consumption
from .forms import ConsumptionForm
from django.utils.timezone import now

def create_record(request):
    categories = DrinkCategory.objects.all()
    drinks = Drink.objects.all()

    if request.method == "POST":
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            consumption = form.save(commit=False)
            consumption.user = request.user
            consumption.quantity = consumption.drink.volume  # volumeをそのままquantityに
            consumption.save()
            return redirect("list_records")  # 登録後、記録閲覧画面(のちに変更予定)
    else:
        form = ConsumptionForm()

    return render(request, "records/create_record.html", {
        "form": form,
        "categories": categories,
        "drinks": drinks,
    })
"""
from django.shortcuts import render
from django.http import HttpResponse

def create_record(request):
    return HttpResponse("飲料記録の登録ページ（未実装）")
"""
from django.http import HttpResponse
def list_records(request):
    return HttpResponse("飲料記録の閲覧ページ（未実装）")
