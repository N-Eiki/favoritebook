from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
# from .views import signupfunc, homefunc, detailfunc, loginfunc,logoutfunc, dataCreate,findfunc , goodfunc, notGoodfunc
from . import views
urlpatterns = [
    path("", views.signupfunc, name="signup"),
    path("signup/", views.signupfunc, name="signup"),
    path('login/', views.loginfunc, name="login"),
    path('home/', views.homefunc, name="home"),
    path('logout/', views.logoutfunc, name="logout"),
    path('detail/<int:pk>', views.detailfunc,name="detail"),
    path("find/",views.findfunc, name="find"),
    path('good/<int:pk>', views.goodfunc, name="good"),
    path('notGood/<int:pk>', views.notGoodfunc, name="notGood"),
    path('create/', views.dataCreate.as_view() , name="create"),
    path('mypage/', views.mypagefunc, name="mypage"),
    path('delete/<int:pk>', views.dataDelete.as_view(), name="delete"),
    path("changeTag/<int:pk>", views.changeTagfunc, name="changeTag"),
    path('user/<targetUser>', views.userPostsfunc, name="userposts"),
    path('setting', views.settingfunc, name="setting")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





