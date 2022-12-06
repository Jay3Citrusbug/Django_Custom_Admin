from django.urls import path
# from rest_framework.authtoken.views import obtain_auth_token
from .import views


urlpatterns = [
    path('stu_data/',views.StudentApi.as_view()),
    path('stu_data/<int:pk>',views.StudentApi.as_view()),
  

   
    ]
