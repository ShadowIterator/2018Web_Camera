from django.urls import path,re_path
from . import views

urlpatterns=[
    path('refresh/', views.show_frame),
    path('signup/', views.sign_up),
    path('mjpeg/', views.mjpeg),
	path('welcome/', views.welcome),
	path('play/', views.playSaiki),
	re_path('play/(?P<fileName>.+)', views.playVideo),
    path('login/', views.log_in),
    path('logout/', views.log_out),
    path('manage/', views.manage_user),
    path('delete', views.delete_user),
    path('add', views.add_user)
]
