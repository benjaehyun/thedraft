from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('subforums/create/', views.SubforumCreate.as_view(), name='subforums_create'),
	path('subforums/update/', views.SubforumCreate.as_view(), name='subforums_create'),
	path('subforums/<int:subforum_id>/', views.subforums_detail, name='subforums_detail'),
	path('subforums/<int:subforum_id>/add_post/', views.add_post, name='add_post'),
	path('subforums/<int:subforum_id>/update_post/', views.update_post, name='update_post'),
	path('subforums/<int:subforum_id>/delete_post/', views.delete_post.as_view(), name='delete_post'),
	path('company-subforums/create/', views.Company_SubforumCreate.as_view(), name='company_subforums_create'),
	path('company-subforums/update/', views.Company_SubforumUpdate.as_view(), name='company_subforums_create'),
	path('company-subforums/<int:company_subforum_id>/', views.company_subforums_detail, name='company_subforums_detail'),
	path('company-subforums/<int:company_subforum_id>/add_post/', views.add_company_post, name='add_company_post'),
	path('company-subforums/<int:company_subforum_id>/update_post/', views.update_company_post, name='update_company_post'),
	path('company-subforums/<int:company_subforum_id>/delete_post/', views.delete_company_post.as_view(), name='delete_company_post'),
	path('companies/', views.CompanyList.as_view(), name='company_index'),
	path('companies/<int:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
	path('companies/create/', views.CompanyCreate.as_view(), name='company_create'),
]