from django.shortcuts import render
from django.http.response import HttpResponse, HttpResponseRedirect
from .models import Products, Users, Ips, ShoppingList
from . import utils

def Login(request):
    user = utils.CurrentUser(request)
    result = ''
    if utils.Redirect(request):
        result = 'Login first'
    if request.method == 'POST':
        result = utils.Login(request)
        if not result:
            if utils.Redirect(request):
                return HttpResponseRedirect(utils.Redirect(request))
            return HttpResponseRedirect('/')
    context = {
        'User': user,
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

def Product(request,pk=None):
    user = utils.CurrentUser(request)
    product = Products.objects.get(pk=pk)
    added = False
    if request.GET.get('product'):
        utils.AddProduct(request)
        added = True
    context = {
        'User': user,
        'product':product,
        'added':added,
    }
    return render(request,'product.html', context)

def Search(request):
    user = utils.CurrentUser(request)
    query = request.GET.get('q')
    results = utils.Search(query)
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

def ShoppingListView(request):
    user = utils.CurrentUser(request)
    if not user:
        return HttpResponseRedirect('/login?next=shoppinglist')
    try:
        items = ShoppingList.objects.get(user=user).product.all()
    except ShoppingList.DoesNotExist:
        items = None
    if request.GET.get('remove'):
        utils.RemoveProduct(request)
    items = ShoppingList.objects.get(user=user).product.all()
    prices = [x.price for x in items]
    counts = ['1' for x in prices]
    if request.method == 'POST':
        counts = utils.ChangeCount(request)
        prices = [int(x) * int(y) for x,y in zip(prices,counts)]
    items = list(zip(items, prices, counts))
    total = sum(prices)
    context = {
        'User':user,
        'items':items,
        'total':total,
    }
    return render(request, 'shoppinglist.html', context)