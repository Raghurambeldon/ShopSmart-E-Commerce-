from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [ 
    path('', views.home, name='home'),
    path('home/',views.home,name='home'),
    path('deals/',views.deals,name='deals'),
     path('signup/',views.signup,name='signup'),
     path('login/',views.login,name='login'),
     path('logout/', views.logout, name='logout'),
      path('productdetail/<int:product_id>', views.product_detail, name='product_detail'),
      path('search_products/', views.search_products, name='search_products'),
    path('add_to_cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart, name='cart'),  
    path('remove_from_cart/<int:cart_item_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('order_summary/<int:order_id>/', views.order_summary, name='order_summary'),
]

urlpatterns += static(settings.MEDIA_URL,document_root= settings.MEDIA_ROOT)