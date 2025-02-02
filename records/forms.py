from django import forms
from .models import Consumption, Drink, DrinkCategory

class ConsumptionForm(forms.ModelForm):
    category = forms.ModelChoiceField(
        queryset=DrinkCategory.objects.all(), 
        empty_label="カテゴリーを選択"
    )
    drink = forms.ModelChoiceField(
        queryset=Drink.objects.none(),  # 初期状態では空
        empty_label="飲み物を選択"
    )
    quantity = forms.FloatField(widget=forms.HiddenInput())  # 量を自動セット

    class Meta:
        model = Consumption
        fields = ["drink", "consumed_at", "quantity"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if "category" in self.data:
            try:
                category_id = int(self.data.get("category"))
                self.fields["drink"].queryset = Drink.objects.filter(category_id=category_id)
            except (ValueError, TypeError):
                self.fields["drink"].queryset = Drink.objects.none()
        else:
            self.fields["drink"].queryset = Drink.objects.none()
