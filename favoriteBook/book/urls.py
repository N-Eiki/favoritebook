from django.urls import path
from django.conf.urls.static import static
from django.conf import settings
# from .views import signupfunc, homefunc, detailfunc, loginfunc,logoutfunc, dataCreate,findfunc , goodfunc, notGoodfunc
from . import views
urlpatterns = [
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
#     path('find/<str:item>', views.findByGenresfunc, name="findgenre")
]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)





