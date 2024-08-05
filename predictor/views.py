# predictor/views.py
from django.shortcuts import render, redirect
from .forms import StockSimulationForm
from .simulation import run_simulation

def index(request):
    if request.method == 'POST':
        form = StockSimulationForm(request.POST)
        if form.is_valid():
            simulation = form.save(commit=False)  # Don't save to DB yet

            # Run the simulation
            graphic, final_values = run_simulation(
                simulation.symbol,
                float(simulation.initial_investment),
                float(simulation.monthly_contribution),
                simulation.num_months
            )

            # Now you can save if needed
            # simulation.save()

            return render(request, 'predictor/results.html', {
                'simulation': simulation,
                'graphic': graphic,
                'final_values': final_values
            })
    else:
        form = StockSimulationForm()

    return render(request, 'predictor/index.html', {'form': form})







