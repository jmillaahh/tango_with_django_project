from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    # html = html = "Rango says hey there partner!<br/>" + '<a href="/rango/about/">About</a>'
    # return HttpResponse(html)
    context_dict = {'boldmessage': 'Crunchy, creamy, cookie, candy, cupcake!'}
    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # html = "Rango says here is the about page.<br/>" + '<a href="/rango/">Index</a>'
    # return HttpResponse(html)
    return render(request, 'rango/about.html')
