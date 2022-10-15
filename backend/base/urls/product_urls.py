from django.urls import path
from base.views import product_views as views # importing all functions from product_views

# url routes related to Product as https://localhost/api/products/....

urlpatterns = [

    path('', views.getProducts, name="products"), # api url route to get all the products
    path('create/', views.createProduct, name='product-create'), # api url route to create new product (by admin)
    path('upload/', views.uploadImage, name='image-upload'), # api url route to upload image of the product
    path('<str:pk>/', views.getProduct, name="product"), # api url route to get single product by its "id"
    path('delete/<str:pk>/', views.deleteProduct, name='product-delete'), # api url route to delete product (by admin)
    path('update/<str:pk>/', views.updateProduct, name='product-update'), # api url route to update product details (by admin)

]