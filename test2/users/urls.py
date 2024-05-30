from django.conf import settings
from django.urls import path, include
from django.conf.urls.static import static

from . import views
urlpatterns = [
    path('', views.sign_in, name='sign_in'),
    path('product',views.product,name="product"),
    path('index', views.index, name="index"),
    path('product1/<int:id>', views.product1, name="product1"),
    path('order/<int:id>', views.order, name="order"),
    path('orderdetail',views.orderdetail,name="orderdetail"),
    path("createorder",views.createorder, name="createorder"),
    path("update/<int:id>",views.update_order,name="update_order"),
    path("productcate/<int:id>",views.product_cate, name="product_cate"),
    path("history_order",views.history_order, name="history_order"),
    path("infor_order/<int:id>",views.infor_order,name="infor_order"),
    path("branch",views.branch,name="branch"),
    path("login", views.login, name="login"),
    path("view_order", views.view_order, name="view_order"),
    path("removeOrder/<int:id>", views.removeOrder, name="removeOrder"),
    path("complete_order/<int:id>", views.complete_order, name="complete_order")
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)