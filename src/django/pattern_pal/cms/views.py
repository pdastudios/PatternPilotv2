from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
def HomeView(request):
    template_dirs = [template['DIRS'] for template in settings.TEMPLATES]
    print("THIS IS",template_dirs)
    return render(request, "index.html")