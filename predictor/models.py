from django.db import models

class StockSimulation(models.Model):
    symbol = models.CharField(max_length=10)
    initial_investment = models.DecimalField(max_digits=10, decimal_places=2)
    monthly_contribution = models.DecimalField(max_digits=10, decimal_places=2)
    num_months = models.IntegerField()
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.symbol} simulation on {self.date_created}"


