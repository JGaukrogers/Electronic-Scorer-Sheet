from django.shortcuts import render


# Create your views here.
def show_sheet(request):
    return render(request, 'scorerSheet/sheet.html', {})
