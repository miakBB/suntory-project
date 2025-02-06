from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Drink, DrinkCategory, Consumption
from .forms import ConsumptionForm
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.http import JsonResponse
from datetime import date

@login_required
def create_record(request):
    categories = DrinkCategory.objects.all()
    drinks = Drink.objects.all()

    # 直近1週間の日付リストを生成
    today = now().date()
    past_week_dates = [(today - timedelta(days=i)).strftime("%Y-%m-%d") for i in range(7)]
    
    if request.method == "POST":
        form = ConsumptionForm(request.POST)
        if form.is_valid():
            consumption = form.save(commit=False)

            # `drink` をフォームから取得
            drink_id = request.POST.get("drink")
            if drink_id:
                consumption.drink = Drink.objects.get(id=drink_id)

            # `consumed_at` をフォームから取得（選択された日付）
            consumed_at = request.POST.get("consumed_at")
            if consumed_at:
                consumption.consumed_at = consumed_at

            consumption.user = request.user  # ユーザーをセット
            consumption.quantity = consumption.drink.volume  # `quantity` を `drink.volume` にする
            consumption.save()
            return redirect("list_records")  # 登録後、記録閲覧画面へ
        else:
            print(form.errors)  # デバッグ用: エラーメッセージを出力

    else:
        form = ConsumptionForm()

    return render(request, "records/create_record.html", {
        "form": form,
        "categories": categories,
        "drinks": drinks,
        "past_week_dates": past_week_dates,  # 直近1週間の日付リストをテンプレートに渡す
    })

@login_required
def list_records(request):
    return render(request, "records/list_records.html")

def calculate_required_water(user):
    """ ユーザーの年齢と体重に基づいて、1日の必要水分量 (mL) を計算 """
    today = date.today()
    birth_date = user.birth_date
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if birth_date == date(1900, 1, 1):
        age = 30

    # 年齢別の必要水分量（mL/kg/日）
    if age >= 65:
        water_per_kg = 25
    elif 55 <= age < 65:
        water_per_kg = 30
    else:
        water_per_kg = 35

    # 必要水分量の計算（60%が飲料から）
    required_water = user.weight * water_per_kg * 0.6
    return round(required_water, 1)

@login_required
def get_weekly_data(request):
    user = request.user
    today = now().date()
    start_date = today - timedelta(days=6)  # 直近1週間

    # ① **目標水分量の計算**
    required_water = calculate_required_water(user)

    # ② **1週間分の水分摂取量**
    past_week_dates = {str((today - timedelta(days=i)).strftime("%Y-%m-%d")): 0.0 for i in range(7)}
    
    records = (
        Consumption.objects
        .filter(user=user, consumed_at__date__range=[start_date, today])
        .values("consumed_at__date")
        .annotate(total_quantity=Sum("quantity"))
    )
    for record in records:
        past_week_dates[str(record["consumed_at__date"])] = record["total_quantity"]

    weekly_data = [{"date": date, "total": quantity} for date, quantity in sorted(past_week_dates.items(), reverse=True)]

    # ③ **1週間分の栄養素 & 飲料記録の取得**
    details_data = {}
    nutrition_data = {}

    details = (
        Consumption.objects
        .filter(user=user, consumed_at__date__range=[start_date, today])
        .select_related("drink")
        .values("consumed_at__date", "drink__name", "quantity", "drink__kcal", "drink__caffeine", "drink__sugars", "drink__unit")
    )

    for detail in details:
        date_str = str(detail["consumed_at__date"])
        if date_str not in details_data:
            details_data[date_str] = []
            nutrition_data[date_str] = {"kcal": 0, "caffeine": 0, "sugars": 0}

        unit = detail["drink__unit"]
        quantity = detail["quantity"]

        kcal = (quantity / unit) * detail["drink__kcal"] if unit > 0 else 0
        caffeine = (quantity / unit) * detail["drink__caffeine"] if unit > 0 else 0
        sugars = (quantity / unit) * detail["drink__sugars"] if unit > 0 else 0

        details_data[date_str].append({
            "drink_name": detail["drink__name"],
            "quantity": quantity,
            "kcal": round(kcal, 1),
            "caffeine": round(caffeine, 1),
            "sugars": round(sugars, 1),
        })

        nutrition_data[date_str]["kcal"] += kcal
        nutrition_data[date_str]["caffeine"] += caffeine
        nutrition_data[date_str]["sugars"] += sugars

    return JsonResponse({
        "required_water": required_water,
        "weekly_data": weekly_data,
        "nutrition": nutrition_data,
        "details": details_data
    })