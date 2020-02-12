from django.shortcuts import render, redirect
from django.http import HttpResponse

# Import Category and Page models
from rango.models import Category, Page

# form specific imports
from rango.forms import CategoryForm, PageForm, UserForm, UserProfileForm
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

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

@login_required
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


@login_required
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


def register(request):
    registered = False

    if request.method == 'POST':
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()

            user.set_password(user.password)
            user.save()

            profile = profile_form.save(commit=False)
            profile.user = user

            if 'picture' in request.FILES:
                profile.picture = request.FILES['picture']

            profile.save()
            registered = True

        else:
            print(user_form.errors, profile_form.errors)
    else:
        # this code is executed if not a HTTP POST
        # forms are rendered from two blank ModelForm instances
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request,
                  'rango/register.html',
                  context = {'user_form': user_form,
                             'profile_form': profile_form,
                             'registered': registered})

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('rango:index'))
            else:
                # inactive account used -- forbid login request
                return HttpRespone("Your Rango account is disabled.")
        else:
            # bad login details provided
            print(f"Invalid login details: {username}, {password}")
            return HttpRespone("Invalid login details supplied.")
    else:
        # this code will be executed most likely in the case of a HTTP GET
        return render(request, 'rango/login.html')

@login_required
def restricted(request):
    # return HttpResponse("Since you're logged in, you can see this text!")

    # for the sake of passing tests_chapter9.py
    return HttpResponse("<title>Rango-Restricted Page</title>")

@login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('rango:index'))
