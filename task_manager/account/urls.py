from django.urls import path

urlpatterns = [
    path('',),
    path('create/'),
    path('<int:pk>/update/'),
    path('<int:pk>/delete/'),
]