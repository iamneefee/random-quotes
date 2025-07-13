from django.shortcuts import render

def handler400(request, exception):
    return render(request, 'quotes/errors/others.html')

def handler403(request, exception):
    return render(request, 'quotes/errors/others.html')

def handler404(request, exception):
    return render(request, 'quotes/errors/404.html')

def handler500(request):
    return render(request, 'quotes/errors/others.html')