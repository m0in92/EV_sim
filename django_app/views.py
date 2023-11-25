from django.shortcuts import render

from.forms import SimulationInputForm


def index(request):
    if request.method == "POST":
        form = SimulationInputForm(request.POST)
        if form.is_valid():
            print('yes')
    else:
        form = SimulationInputForm()
    return render(request=request, template_name='index.html', context={'form': form})


