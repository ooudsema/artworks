from django.urls import path, re_path

from . import views

#urlpatterns = [
#   path('', views.index, name='index'),
#]

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('subjects/', views.SubjectListView.as_view(), name='subjects'),
    path('subjects/<int:pk>/', views.SubjectDetailView.as_view(), name='subject_detail'),
    path('art/', views.ArtListView.as_view(), name='art'),
    path('art/<int:pk>/', views.ArtDetailView.as_view(), name='art_detail'),
    path('art/new/', views.ArtworkCreateView.as_view(), name='art_new'),
    path('art/<int:pk>/delete/', views.ArtDeleteView.as_view(), name='art_delete'),
    path('art/<int:pk>/update/', views.ArtUpdateView.as_view(), name='art_update'),
    path('art/search/', views.ArtFilterView.as_view(), name='search')
]