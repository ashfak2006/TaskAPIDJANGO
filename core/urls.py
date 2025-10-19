from django.urls import include,path

from .views import listtasks,usercreate,taskdetail,logoutview,setduemessage,markasread,markallasread

urlpatterns = [  
    path('tasks/',listtasks.as_view(),name='tasks'),
    path('logout/',logoutview.as_view(),name='logout'),
    path('tasks/<int:pk>/',taskdetail.as_view(),name='taskdetail'),
    path('user/create/',usercreate.as_view(),name='users'),
    path('tasks/setduemessage/<int:id>/',markasread,name='markasread'),
    path('tasks/setduemessage/markallasread/',markallasread,name='markallasread'),
    path('tasks/setduemessage/',setduemessage,name='setduemessage')
]