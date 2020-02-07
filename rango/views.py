from django.shortcuts import render
from django.http import HttpResponse

# Import Category and Page models
from rango.models import Category, Page

# Create your views here.
def index(request):
    # html = html = "Rango says hey there partner!<br/>" + '<a href="/rango/about/">About</a>'
    # return HttpResponse(html)
    category_list = Category.objects.order_by('-likes')[:5]
    page_list = Page.objects.order_by('-views')[:5]

    context_dict = {}
    context_dict['boldmessage'] = 'Crunchy, creamy, cookie, candy, cupcake!'
    context_dict['categories'] = category_list
    context_dict['pages'] = page_list

    return render(request, 'rango/index.html', context=context_dict)

def about(request):
    # html = "Rango says here is the about page.<br/>" + '<a href="/rango/">Index</a>'
    # return HttpResponse(html)
    return render(request, 'rango/about.html')

def show_category(request, category_name_slug):
    context_dict = {}
    try:
        # will raise an exception if none found and will execute except
        # block code
        category = Category.objects.get(slug=category_name_slug)

        # retrieve all associated pages; filter() will return a list of page
        # objects or an empty list
        pages = Page.objects.filter(category=category)

        context_dict['pages'] = pages
        context_dict['category'] = category

    except Category.DoesNotExist:
        context_dict['category'] = None
        context_dict['pages'] = None

    return render(request, 'rango/category.html', context=context_dict)
