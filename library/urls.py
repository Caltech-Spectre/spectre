from django.urls import path

from . import views

urlpatterns = [
    path('', views.mainPage, name='home'),
    # /spectre/user/add/, the page where you can join spectre, and add a user
    path('user/', views.showUser, name='user'),
    path('user/books/', views.my_books, name='my_books'),
    path('user/add/', views.addUser),
    path('login/', views.loginPage, name='login'),
    path('book/search/count/', views.bookPageSearchCount),
    path('book/search/xml/', views.bookXMLSearch),
    path('book/', views.showBook, name='book'),
    path('logout/', views.logout, name='logout'),
    path('checkout/', views.checkout, name='checkout'),
    path('checkin/', views.checkin, name='checkin')

]