from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Drink, DrinkCategory, Consumption
from .forms import ConsumptionForm
from django.utils.timezone import now, timedelta
from django.db.models import Sum
from django.http import JsonResponse

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

@login_required
def get_weekly_data(request):
    today = now().date()
    start_date = today - timedelta(days=6)  # 1週間前

    # 直近1週間の日付リストを作成（初期値は 0ml）
    past_week_dates = {str((today - timedelta(days=i)).strftime("%Y-%m-%d")): 0.0 for i in range(7)}

    # DBから取得したデータを統合
    records = (
        Consumption.objects
        .filter(user=request.user, consumed_at__date__range=[start_date, today])
        .values("consumed_at__date")
        .annotate(total_quantity=Sum("quantity"))
    )

    for record in records:
        past_week_dates[str(record["consumed_at__date"])] = record["total_quantity"]


    # **ここで降順にソート**
    summary = [{"date": date, "total_quantity": quantity} for date, quantity in sorted(past_week_dates.items(), reverse=True)]

    # 詳細データの取得（unit を考慮して計算）
    details = (
        Consumption.objects
        .filter(user=request.user, consumed_at__date__range=[start_date, today])
        .select_related("drink")
        .values("consumed_at__date", "drink__name", "quantity", "drink__caffeine", "drink__sugars", "drink__salt", "drink__unit")
    )

    details_data = {}
    for detail in details:
        date_str = str(detail["consumed_at__date"])
        if date_str not in details_data:
            details_data[date_str] = []
        
        # `unit` を考慮して計算
        unit = detail["drink__unit"]
        quantity = detail["quantity"]
        
        caffeine = (quantity / unit) * detail["drink__caffeine"] if unit > 0 else 0
        sugars = (quantity / unit) * detail["drink__sugars"] if unit > 0 else 0
        salt = (quantity / unit) * detail["drink__salt"] if unit > 0 else 0

        details_data[date_str].append({
            "drink_name": detail["drink__name"],
            "quantity": quantity,
            "caffeine": round(caffeine, 2),
            "sugars": round(sugars, 2),
            "salt": round(salt, 2)
        })

    return JsonResponse({"summary": summary, "details": details_data}, safe=False)