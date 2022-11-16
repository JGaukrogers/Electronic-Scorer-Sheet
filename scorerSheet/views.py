from django.forms import modelformset_factory
from django.shortcuts import render


# Create your views here.
from scorerSheet.forms import CellForm
from scorerSheet.models import Cell


def show_sheet(request):
    CellFormSet = modelformset_factory(Cell, CellForm, extra=0)
    if request.method == 'POST':
        formset = CellFormSet(request.POST)
        if formset.is_valid():
            for form in formset:
                print(form.cleaned_data)
            formset.save()
    else:
        formset = CellFormSet()

    context = {'formset': formset}
    return render(request, "sheet.html", context)