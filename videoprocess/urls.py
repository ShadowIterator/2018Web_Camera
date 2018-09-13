from django.urls import path,re_path
from . import views
from . import views_si

urlpatterns=[
    #path('refresh/', views.show_frame),
    path('signup/', views.sign_up),
    path('mjpeg/', views_si.mjpeg),
	path('welcome/', views_si.welcome),
	# path('play/', views_si.playSaiki),
	re_path('play/(?P<fileName>.*)', views_si.playVideo),
    path('login/', views.log_in),
    path('logout/', views.log_out),
    path('manage/', views.manage_user),
    path('delete', views.delete_user),
    path('add', views.add_user),
    path('websocket/', views_si.websocket, name = 'websocket'),
    path('releaseCap/', views_si.releaseCap, name = 'releaseCap'),
    path('info/', views_si.infotest),
    path('records/', views.manage_record),
    path('delrecord',views.del_record)
]
