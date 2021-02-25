from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Products, Users, Ips, ShoppingList, Reviews
from . import utils

def Login(request):
    user = utils.CurrentUser(request)
    next_url = utils.Redirect(request)
    result = ''
    if next_url:
        result = 'Login first'
    if request.method == 'POST':
        result = utils.Login(request)
        if not result and next_url:
            return HttpResponseRedirect(next_url)
        if not result:
            return HttpResponseRedirect('/profile')
    context = {
        'User':user,
        'result':result,
    }
    return render(request, 'login.html', context)

def Index(request):
    user = utils.CurrentUser(request)
    products = Products.objects.filter(featured=True)
    number_of_lists = int(len(products) / 5)
    products = utils.Split(products, 5)
    number_of_lists = [ x for x in range(number_of_lists)]
    context = {
        'User': user,
        'products':products,
        'lists':number_of_lists,
    }
    return render(request,'index.html', context)

@utils.Login_Requierd
def Profile(request):
    user = utils.CurrentUser(request)
    result = ''
    if request.method == 'POST':
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')
        user.phone_number = phone_number
        user.address = address
        user.save()
    context = {
        'User': user,
        'result': result,
    }
    return render(request, 'profile.html', context)

def Product(request,pk=None):
    user = utils.CurrentUser(request)
    product = Products.objects.get(pk=pk)
    reviews = Reviews.objects.filter(product=product)
    added = False
    if request.GET.get('product'):
        return utils.AddProduct(request)
    if ShoppingList.objects.filter(user=user):
        if product in ShoppingList.objects.get(user=user).product.all():
            added = True
    if request.POST.get('review'):
        utils.AddReview(request)
    context = {
        'User': user,
        'product':product,
        'added':added,
        'reviews':reviews,
    }
    return render(request,'product.html', context)

def Search(request):
    user = utils.CurrentUser(request)
    query = request.GET.get('q')
    results = utils.Search(query, request)
    if request.POST:
        results = utils.Search(query, request, filt=True)
    if not query:
        return HttpResponseRedirect('/')
    context = {
        'User': user,
        'results':results
    }
    return render(request,'search.html', context)

def Signup(request):
    result = ''
    if request.method == 'POST':
        result = utils.CreateAccout(request)
    context = {
        'result':result,
    }
    return render(request, 'signup.html', context)

def Logout(request):
    user = utils.CurrentUser(request)
    ip = request.META['REMOTE_ADDR']
    user = Users.objects.get(username=user.username)
    user.logged_in = False
    user.save()
    Ips.objects.filter(ip=ip).delete()
    return HttpResponseRedirect('/')

@utils.Login_Requierd
def ShoppingListView(request):
    user = utils.CurrentUser(request)
    try:
        items = ShoppingList.objects.get(user=user).product.all()
    except ShoppingList.DoesNotExist:
        items = []
    if request.GET.get('remove'):
        utils.RemoveProduct(request)
    prices = [x.price for x in items]
    counts = [1 for x in prices]
    if request.method == 'POST':
        counts = utils.ChangeCount(request)
        prices = [x * y for x,y in zip(prices,counts)]
    items = list(zip(items, prices, counts))
    totalp, totalc = sum(prices),sum(counts)
    context = {
        'User':user,
        'items':items,
        'totalp':totalp,
        'totalc':totalc,
    }
    return render(request, 'shoppinglist.html', context)