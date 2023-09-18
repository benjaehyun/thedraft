from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('subforums/<int:subforum_id>/', views.subforums_detail, name='subforums_detail'),
	path('subforums/create/', views.SubforumCreate.as_view(), name='subforums_create'),
	path('subforums/<int:subforum_id>/add_post/', views.add_post, name='add_post'),
	path('companies/', views.CompanyList.as_view(), name='company_index'),
	path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
	path('companies/create/', views.CompanyCreate.as_view(), name='company_create'),
]