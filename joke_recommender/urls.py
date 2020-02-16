from django.urls import path

from . import views

urlpatterns = [
	path('', views.index, name = 'index'),
	path('<int:joke_id>/', views.detail, name = 'detail'),
	path('my_ratings/', views.ratings_view, name = 'my-ratings'),
	path('<int:joke_id>/rate/', views.rate, name = 'rate'),
]

