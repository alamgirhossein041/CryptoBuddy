from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
def home_page(request):
    return render(request,"Home/index.html")

def news(request):
    return render(request,"Home/news.html")    
