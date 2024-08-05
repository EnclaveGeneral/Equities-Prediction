from django import forms
from .models import StockSimulation

class StockSimulationForm(forms.ModelForm):
    class Meta:
        model = StockSimulation
        fields = ['symbol', 'initial_investment', 'monthly_contribution', 'num_months']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['symbol'].widget.attrs.update({'placeholder': 'Enter stock symbol...'})
        self.fields['initial_investment'].widget.attrs.update({'step': '0.01'})
        self.fields['monthly_contribution'].widget.attrs.update({'step': '0.01'})
        self.fields['num_months'].widget.attrs.update({'min': '1'})





