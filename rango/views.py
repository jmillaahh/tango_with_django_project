from django.shortcuts import render, redirect
from django.http import HttpResponse

# Import Category and Page models
from rango.models import Category, Page

# form specific imports
from rango.forms import CategoryForm, PageForm
from django.urls import reverse

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

def add_category(request):
    form = CategoryForm()

    # A HTTP POST?
    if request.method == 'POST':
        form = CategoryForm(request.POST)

        # is form valid?
        if form.is_valid():
            # save new category to database
            form.save(commit=True)
            # once saved, confirtm this and redirect user back to index view
            return redirect('/rango/')
        else:
            print(form.errors)

    return render(request, 'rango/add_category.html', {'form': form})

def add_page(request, category_name_slug):
    try:
        category = Category.objects.get(slug=category_name_slug)
    except Category.DoesNotExist:
        category = None

    if category is None:
        return redirect('/rango/')

    form = PageForm()

    if request.method == 'POST':
        form = PageForm(request.POST)

        if form.is_valid():
            if category:
                page = form.save(commit=False)
                page.category = category
                page.views = 0
                page.save()

                return redirect(reverse('rango:show_category',
                                        kwargs={'category_name_slug':
                                                category_name_slug}))

        else:
            print(form.errors)

    context_dict = {'form': form, 'category': category}
    return render(request, 'rango/add_page.html', context=context_dict)
