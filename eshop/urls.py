from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
	path('login/', views.login_view, name="login"),
	path('register/', views.register_view, name="register"),
	path('logout/', views.logout_view, name="logout"),
	path('orders/', views.order_history, name="order_history"),
    path('product/<int:product_id>/',views.product_detail,name='product_detail'),
    path('update_item/', views.updateItem, name="update_item"),
	path('process_order/', views.processOrder, name="process_order"),
]