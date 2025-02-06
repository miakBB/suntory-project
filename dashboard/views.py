from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from records.models import Consumption
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from datetime import date

@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

def calculate_required_water(user):
    """ ユーザーの年齢と体重に基づいて、1日の必要水分量 (mL) を計算 """
    today = date.today()
    birth_date = user.birth_date
    age = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    if birth_date == date(1900, 1, 1):
        age = 30  # 生年月日が未入力の場合はデフォルト値（30歳）を設定する

    # 年齢別の必要水分量（mL/kg/日）
    if age >= 65:
        water_per_kg = 30
    elif 55 <= age < 65:
        water_per_kg = 35
    else:
        water_per_kg = 40

    # 必要水分量の計算（80%が飲料から）
    required_water = user.weight * water_per_kg * 0.8

    return round(required_water, 1)

@login_required
def get_dashboard_data(request):
    user = request.user
    today = now().date()
    start_week = today - timedelta(days=6)

    # ① 今日の水分摂取量
    daily_total = (
        Consumption.objects.filter(user=user, consumed_at__date=today)
        .aggregate(total=Sum("quantity"))["total"] or 0
    )
    required_water = calculate_required_water(user)

    # ② 今日の栄養素摂取（カロリー、糖分、カフェイン）
    nutrition_data = (
        Consumption.objects
        .filter(user=user, consumed_at__date=today)
        .select_related("drink")
        .values("drink__kcal", "drink__caffeine", "drink__sugars", "drink__unit", "quantity")
    )

    total_kcal = 0
    total_caffeine = 0
    total_sugars = 0

    for item in nutrition_data:
        unit = item["drink__unit"]
        quantity = item["quantity"]

        kcal = (quantity / unit) * item["drink__kcal"] if unit > 0 else 0
        caffeine = (quantity / unit) * item["drink__caffeine"] if unit > 0 else 0
        sugars = (quantity / unit) * item["drink__sugars"] if unit > 0 else 0

        total_kcal += kcal
        total_caffeine += caffeine
        total_sugars += sugars

    # ③ 直近1週間の水分摂取量
    weekly_data = {
        str((today - timedelta(days=i)).strftime("%Y-%m-%d")): 0 for i in range(7)
    }
    weekly_records = (
        Consumption.objects.filter(user=user, consumed_at__date__range=[start_week, today])
        .values("consumed_at__date")
        .annotate(total=Sum("quantity"))
    )
    for record in weekly_records:
        weekly_data[str(record["consumed_at__date"])] = record["total"]

    # ④ お気に入り飲料 (過去4週間)
    start_month = today - timedelta(weeks=4)
    favorite_drinks = (
        Consumption.objects.filter(user=user, consumed_at__date__gte=start_month)
        .values("drink__name")
        .annotate(total=Sum("quantity"))
        .order_by("-total")[:5]  # 上位5つ
    )

    return JsonResponse({
        "daily_total": daily_total,
        "required_water": required_water,
        "nutrition": {
            "kcal": round(total_kcal, 1),
            "caffeine": round(total_caffeine, 1),
            "sugars": round(total_sugars, 1),
        },
        "weekly_data": [{"date": date, "total": total} for date, total in weekly_data.items()],
        "favorite_drinks": list(favorite_drinks),
    })
