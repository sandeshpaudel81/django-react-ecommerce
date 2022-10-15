from django.urls import path
from base.views import order_views as views

# url routes related to order

urlpatterns = [

    path('add/', views.addOrderItems, name="orders-add"), # to add order items
    path('myorders/', views.getMyOrders, name='myorders'), # to view my order

    path('<str:pk>/', views.getOrderById, name="user-order"), # to get order by id for admin
    path('<str:pk>/pay/', views.updateOrderToPaid, name="pay"), # add payment to the order
]