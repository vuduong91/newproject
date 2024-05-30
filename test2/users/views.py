from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.test import TestCase



from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.template import RequestContext
from django.views import View

from .models import Product, Order, OrderDetail, User,Category,CustomUser
from .forms import LoginForm, OrderForm, UpdateForm, CustomUserCreationForm, UserForm
from django.db.models import F


# Create your views here.
# -------------------------------- home website
@login_required(login_url='sign_in')
def index(request):
        cates = Category.objects.all()
        productdetails = Product.objects.all()
        products = Product.objects.all()
        context = {
            "cates": cates,
            "productdetails": productdetails,
            "products": products
        }
        return render(request, 'product/index.html', context)
    # -------------------------------- product site
@login_required(login_url='sign_in')
def product(request):
        productdetails = Product.objects.all()
        products = Product.objects.all()
        context = {"productdetails": productdetails,
                   "products": products}
        return render(request, 'product/product.html', context)

    # --------------------------------- product+cate
@login_required(login_url='sign_in')
def product_cate(request, id):
    cates = get_object_or_404(Category, id=id)
        # ----------- lấy nhiều sản phẩm
    products = Product.objects.filter(nameCate=cates)
    context = {
        "cates": cates,
        "products": products
        }
    return render(request, 'product/product_cate.html', context)

def product1(request, id):
    print(request.POST)
    productdetails = get_object_or_404(Product, id=id)
    if request.method == 'POST':
        return redirect('product1')
    context = {'productdetails': productdetails}
    return render(request, 'product/product_detail.html', context)
 # -----------------------ok

# ------------------------------------using user account to order
def order(request, id):
    product = Product.objects.get(id=id)
    try:
        order = Order.objects.filter(user=request.user).first()
        if not order:
            order = Order.objects.create(user=request.user)
    except Order.DoesNotExist:
        order = Order.objects.create(user=request.user)
        pass
    order_detail, detail_create = OrderDetail.objects.get_or_create(
        order=order,
        product=product
    )
    if not detail_create:
        order_detail.quanity += 1
        order_detail.save()
        return redirect('product')
    return redirect('product')

# ----------------------------------------
def removeOrder(request, id):
    try:
        product = Product.objects.get(pk=id)
        order = Order.objects.filter(user=request.user).first()
        if order:
            try:
                order_detail = order.orderdetail_set.get(product=product)
                if order_detail.quanity >= 1:
                    order_detail.delete()
            except OrderDetail.DoesNotExist:
                return redirect('view_order')

    except Product.DoesNotExist:
        return redirect('view_order')


def view_order(request):
        if not request.user.is_authenticated:
            return redirect('login')
        orders = Order.objects.filter(user=request.user)
        order_detail = OrderDetail.objects.filter(order__in=orders)
        total = 0
        for detail in order_detail:
            if detail.cost and detail.quanity:
                total += detail.cost * detail.quanity
        return render(request, 'product/order.html', {'total':total,'orders': orders, 'order_detail': order_detail})

        # orders = get_object_or_404(OrderDetail, id=id)
        # context = {
        #     "total":total,
        #     "orders": orders}
        # orders = get_object_or_404(OrderDetail, id=id)
        # form = OrderForm(request.POST or None, instance=orders)
        # if form.is_valid():
        #     form.save()
        # context['form'] = form
        # return render(request, 'product/order.html', context)

    # --------------------access
def update_order(request, id):
        orders = get_object_or_404(OrderDetail, id=id)
        form = UpdateForm(request.POST or None, instance=orders)
        if form.is_valid():
            form.save()
        context= {
            'form':form,
            'orders':orders
        }
        return render(request, 'product/update.html', context)
    # ---------------------------------------------- failed to add new order
#     ---------------------------------------------------- fix***
def orderdetail(request):
    users = User()
    form = UserForm(request.POST or None,instance=users)
    context = {
        'form': form,
    }
    if request.method =='POST':
        if form.is_valid():
            infor_user = form.save(commit=False)
            infor_user.email = form.cleaned_data['email']
            infor_user.save()
            messages.success(request,'ur information have been updated')
            return redirect('history_order')
    return render(request, 'product/add_order.html', context)


def createorder(request):
    order = Order()
    form = OrderForm(request.POST or None, instance=order)
    if request.method == 'POST':
        if form.is_valid():
            new_order = form.save(commit=False)
            new_order.user = form.cleaned_data['user']
            new_order.save()
            messages.success(request, 'Order successfully saved!')
            return redirect('history_order')
            # ...
    context = {
        'form': form,
    }
    return render(request, 'product/create_order.html', context)

# def successdetail(request, id):
#         shippings = get_object_or_404(Shipping, id=id)
#         context = {
#             "shippings": shippings
#         }
#         if shippings.id == 1:
#             return render(request, "product/TT.html", context)
#         elif shippings.id == 2:
#             return render(request, "product/QR.html", context)
#         else:
#             return render(request, "product/TG.html", context)

@login_required(login_url='sign_in')

# ------------------------------------ filter and merging order
def history_order(request):
    orders = Order.objects.filter(user=request.user)
    context = {
               "orders": orders,
               }

    return render(request, "product/historyOder.html", context)
@login_required(login_url='sign_in')
def infor_order(request, id):
    try:
        order = Order.objects.get(id=id)
        user = order.user
        users = get_object_or_404(User,id=user.id)
        order_details = OrderDetail.objects.filter(order=order)
        total = 0
        if order_details.exists():
            for detail in order_details:
                if detail.cost and detail.quanity:
                    total += detail.cost * detail.quanity
        context = {
            "users":users,
            "total": total,
            "user": user,
            "order": order,
            "order_details": order_details,
        }
        return render(request, "product/infor_order.html", context)
    except (ObjectDoesNotExist, PermissionError):
        return render(request, 'error.html', {'error_message': 'Object not found or insufficient permissions'})

def complete_order(request,id):
    try:
        order = Order.objects.get(pk=id, user=request.user)
        if request.method == 'POST':
            order.is_completed = True
            order.save()
            message = "Order successfully marked as completed."
            return redirect('history_order', success_message=message)
        else:
            context = {'order': order}
            return render(request, "product/infor_order.html", context)
    except Order.DoesNotExist:
        message = "Order not found."
        return redirect('history_order', error_message=message)

# ------------------------------------------------------------------------------------------
# -----------------dang nhap bang email user, user duoc cap quyen admin moi co the vao admin
def sign_in(request):
    if request.method == 'GET':
        form = LoginForm()
        return render(request, 'product/login.html', {'form': form})
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Hi {email.title()}, welcome back!')
                return redirect('index')
        # form is not valid or user is not authenticated
        messages.error(request, f'Invalid username or password')
        return render(request, 'product/login.html', {'form': form})
def branch(request):
    return render(request,"product/branch.html")

class UsersManagersTests(TestCase):

    def test_create_user(self):
        User = get_user_model()
        user = User.objects.create_user(email="normal@user.com", password="foo")
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo")
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)