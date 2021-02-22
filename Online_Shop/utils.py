from .models import Products, Users, Ips, ShoppingList
from hashlib import sha256

def Login(request):
    result = ''
    ip = request.META['REMOTE_ADDR']
    username = request.POST.get('username')
    password = request.POST.get('password')
    password = sha256(password.encode()).hexdigest()
    try:
        user_check = Users.objects.get(username=username)
        if user_check.password == password:
            user_check.logged_in = True
            ip_check = Ips.objects.filter(ip=ip)
            if ip_check:
                ip_check[0].user_id = user_check.id
                ip_check[0].save()
            else:
                Ips.objects.create(user=user_check,ip=ip)
            user_check.save()
        else:
            result = 'Incorrect username or password'
    except:
        result = 'User doesn\'t exist'
    return result

def Split(List, size):
    newList = []
    while len(List) > size:
        pice = List[:size]
        newList.append(pice)
        List = List[size:]
    newList.append(List)
    return newList

def Search(query:str):
    result = Products.objects.filter(name__icontains=query)
    return result

def CreateAccout(request):
    email = request.POST.get('email')
    username = request.POST.get('username')
    password = request.POST.get('password')
    first_name = request.POST.get('first_name')
    last_name = request.POST.get('last_name')
    address = request.POST.get('address')
    email_check = Users.objects.filter(email=email)
    username_check = Users.objects.filter(username=username)
    if email_check:
        result = 'Email already exists'
        return result
    elif username_check:
        result = 'Username already exists'
        return result

    password = sha256(password.encode()).hexdigest()
    Users.objects.create(
    username=username,
    password=password,
    email=email,
    first_name=first_name,
    last_name=last_name,
    address=address
    )
    result = 'Account created'
    return result

def CurrentUser(request):
    ip = request.META['REMOTE_ADDR']
    ip = Ips.objects.filter(ip=ip)
    if ip:
        user = ip[0].user
        return user
    else:
        return None

def Redirect(request):
    redirect_url = request.GET.get('next')
    if redirect_url:
        redirect_url = '/' + redirect_url
        return redirect_url
    else:
        return None

def AddProduct(request):
    user = CurrentUser(request)
    product = request.GET.get('product')
    if not ShoppingList.objects.filter(user=user):
        product = Products.objects.filter(pk=product)
        shopping_item = ShoppingList.objects.create(user=user)
        shopping_item.product.set(product)
    else:
        product = Products.objects.get(pk=product)
        shopping_item = ShoppingList.objects.filter(user=user)[0]
        shopping_item.product.add(product)
    return

def RemoveProduct(request):
    user = CurrentUser(request)
    product = request.GET.get('remove')
    shoppinglist = ShoppingList.objects.get(user=user)
    product = Products.objects.get(pk=product)
    shoppinglist.product.remove(product)
    return

def ChangeCount(request):
    items = request.POST
    counts = []
    for k,v in items.items():
        if k.startswith('c_'):
            counts.append(v)
    return counts

