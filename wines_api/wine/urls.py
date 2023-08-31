from django.urls import path
from wine import views

urlpatterns = [
    path('wine_list/', views.wine_list),
]
