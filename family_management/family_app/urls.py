from django.urls import path
from . import views

urlpatterns = [
    path('index/', views.index, name='index'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('password_reset/', views.password_reset, name ="password_reset"),
    path('family/', views.family, name='family'),
    path('add_family/', views.add_family, name='add_family'),
    path('update_family/<int:id>', views.update_family, name='update_family'),
    path("delete_family/<int:id>", views.delete_family, name='delete_family'),
    path('family/<int:family_id>', views.family_details, name='family_details'),
    path('add_family_member/<int:family_id>', views.add_family_member, name='add_family_member'),
    path('update_family_member/<int:family_id>/<int:family_member_id>', views.update_family_member, name='update_family_member'),
    path('delete_family_member/<int:family_id>/<int:family_member_id>', views.delete_family_member, name='delete_family_member'),

]
