from django.shortcuts import render
from django.http import JsonResponse
from django.utils.timezone import now, timedelta
from records.models import Consumption
from django.db.models import Sum
from django.contrib.auth.decorators import login_required

@login_required
def dashboard(request):
    return render(request, "dashboard/dashboard.html")

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
    required_water = (user.weight if hasattr(user, "weight") else 70) * 35  # デフォルト70kg 現在必要量なので、食事分を引かなければ...

    # ② 今日の栄養素摂取（合計値）
    nutrition = (
        Consumption.objects.filter(user=user, consumed_at__date=today)
        .aggregate(
            caffeine=Sum("drink__caffeine"),
            salt=Sum("drink__salt"),
            sugars=Sum("drink__sugars"),
        )
    )

    # ③ 直近1週間の水分摂取量
    weekly_data = {
        str((today - timedelta(days=i)).strftime("%Y-%m-%d")): 0 for i in range(7)
    }
    weekly_records = (
        Consumption.objects.filter(user=user, consumed_at__date__range=[start_week, today])
        .values("consumed_at__date")
        .annotate(total=Sum("quantity"))
    )
    #print(f"weekly_records:{weekly_records}")
    for record in weekly_records:
        weekly_data[str(record["consumed_at__date"])] = record["total"]
    #print(f"weekly_data:{weekly_data}")
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
            "caffeine": nutrition["caffeine"] or 0,
            "salt": nutrition["salt"] or 0,
            "sugars": nutrition["sugars"] or 0,
        },
        "weekly_data": [{"date": date, "total": total} for date, total in weekly_data.items()],
        "favorite_drinks": list(favorite_drinks),
    })
