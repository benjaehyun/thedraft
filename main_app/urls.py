from django.urls import path
from . import views
	
urlpatterns = [
	path('', views.home, name='home'),
	path('about/', views.about, name='about'),
	path('subforums/create/', views.SubforumCreate.as_view(), name='subforums_create'),
	path('subforums/<int:subforum_id>/', views.subforums_detail, name='subforums_detail'),
	path('subforums/<int:pk>/update/', views.SubforumUpdate.as_view(), name='subforums_update'),
	path('subforums/<int:subforum_id>/add_post/', views.add_post, name='add_post'),
  	path('subforums/<int:subforum_id>/post/<int:post_id>/update/', views.update_post, name='update_post'),
	path('subforums/<int:subforum_id>/post/<int:pk>/delete/', views.PostDelete.as_view(), name='delete_post'),
  	path('subforums/<int:subforum_id>/post/<int:post_id>/add_comment/', views.add_comment, name='add_comment'),
	path('company/', views.CompanyList.as_view(), name='company_index'),
	path('company/<int:pk>/', views.CompanyDetail.as_view(), name='company_detail'),
	path('company/create/', views.CompanyCreate.as_view(), name='company_create'),
	path('company/<int:company_id>/subforums/create/', views.CompanySubforumCreate.as_view(), name='company_subforums_create'),
	path('company/<int:company_id>/subforums/<int:pk>/update/', views.Company_SubforumUpdate.as_view(), name='company_subforums_update'),
	path('company/<int:company_id>/subforums/<int:company_subforum_id>/', views.company_subforums_detail, name='company_subforums_detail'),
	path('company/<int:company_id>/subforums/<int:company_subforum_id>/add_post/', views.add_company_post, name='add_company_post'),
    path('company/<int:company_id>/subforums/<int:company_subforum_id>/post/<int:company_post_id>/add_comment/', views.add_company_comment, name='add_company_comment'),
	path('company/<int:company_id>/subforums/<int:company_subforum_id>/posts/<int:company_post_id>/update/', views.update_company_post, name='update_company_post'),
	path('company/<int:company_id>/subforums/<int:company_subforum_id>/posts/<int:pk>/delete/', views.Company_PostDelete.as_view(), name='delete_company_post'),
  	path('accounts/signup/', views.signup, name='signup'), 
]