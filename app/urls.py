from django.urls import path,include
from . import views
from django.conf.urls import url
from rest_framework import routers
app_name='myApp'

router=routers.DefaultRouter()
router.register(r'books',views.ApiBook)

urlpatterns = [
path('api/',include(router.urls)),
# path('',views.base)
 path('',views.Base.as_view(),name='template'),
 path('suggest/',views.suggest,name='suggestion'),
 path('list/<name>',views.BookList.as_view(template_name='book_list.html'),name='myList'),
 path('reserve/<name>/<brand>', views.ReserveView.as_view(), name='reserve'),
 path('<name>/<brand>',views.DetailList.as_view(),name='detail'),
 path('register/',views.Register.as_view(),name='reg'),
 path('show/',views.ShowReserve.as_view(),name='showReserve'),
 path('login/',views.Login.as_view(),name='log'),
 path('logout/',views.Logout.as_view(),name='logout'),
 path('search/',views.Search.as_view(),name='search'),
 path('checkBoxSearch/',views.CheckSearch.as_view(),name='check'),
 path('GetApi/',views.GetApi.as_view(),name='get'),

 # path('(?P<id>[0-9]{1,16})',views.detail_list,name='detail')
 url(r'^request/$', views.send_request, name='request'),
 url(r'^verify/$', views.verify, name='verify'),

    ]
