from django.urls import path

from testoath2.views import UserList, CustomGenerateToken

urlpatterns = [
    path('users/',UserList.as_view() ),
    path('register/',CustomGenerateToken.as_view() ),
]
