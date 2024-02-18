from django.urls import path
from base.views import product_views as views

urlpatterns = [
	
    path('', views.getProducts, name="products"),
    # very important the place of this route, if i move it down i'll get an error METHOD POST NOT ALLOWED
    # pattern that matches the request (e.g., a pattern with a dynamic parameter like "str:pk/")
    path('create/', views.createProduct, name="product-create"),
    path('upload/', views.uploadImage, name="image-upload"),
    path('<str:pk>/', views.getProduct, name="product"),
    path('update/<str:pk>/', views.updateProduct, name="product-update"),
    path('delete/<str:pk>/', views.deleteProduct, name="product-delete"),

]