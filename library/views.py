from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt, csrf_protect

#The main page of Spectre
@csrf_exempt
def mainPage(request):
    context = {}
    return render(request, 'library/mainPageTemplate.html', context)
