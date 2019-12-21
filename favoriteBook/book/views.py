from django.shortcuts import render, redirect, get_object_or_404
from .models import RecommendedBook#,Comment
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from .forms import FindForm,CommentCreateForm,RadioForm




def signupfunc(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        try:
            User.objects.get(username=username)
            return render(request, "signup.html",{"error":"this user is already registered","error2":"please register another name"})
        except:
            user = User.objects.create_user(username, "", password)
            return render(request,"signup.html",{'title':'signup'})
    return render(request, "signup.html", {'title':"signup"})

def loginfunc(request):
    if request.method=="POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(to="home")
        else:
            return redirect(to="login")
    return render(request, "login.html")

def logoutfunc(request):
    logout(request)
    return redirect(to="login")


# @login_required
def homefunc(request):
    object_list = RecommendedBook.objects.all()
    tags=[]
    for item in object_list:
        tags.append(item.genre.split())
#         print(item.genre)
#     print("they are tags")
#     print(tags)
#     for i in range(len(tags)):
#         for item in tags[i]:
#             print(item)
#         print("//////////")
    return render(request, 'home.html',{'title':'home', 'object_list':object_list,'tags':tags})


#詳細

#作成
class dataCreate(CreateView):
    template_name="create.html"
    model=RecommendedBook
    fields=('author','bookTitle',"content","bookImage","genre")
    success_url = reverse_lazy('home')


def findfunc(request):
    if (request.method=="POST"):
        form = FindForm()
        str = request.POST['find']
        data = RecommendedBook.objects.filter(genre__contains=str)
    else:
        form=FindForm()
        data = RecommendedBook.objects.all()
    params = {
        'form':form,
        'data':data,
    }
    return render(request,'find.html',params)


def detailfunc(request, pk):
    sort=True
    if request.method=="POST":
        form = CommentCreateForm(request.POST)
        print(request.POST)
        reverseform=RadioForm(request.POST)
#         print(request.POST.get("select"))
        selectNum=request.POST.get('select')
        if form.is_valid():
            comment = form.save(commit=False)
            comment.target = get_object_or_404(RecommendedBook, pk=pk)
            comment.save()
        if selectNum=="1":
            sort=False#新しいコメントを上に
        else:
            sort=True#古いコメントを上に
    reverseform=RadioForm()
    form=CommentCreateForm()
    object = RecommendedBook.objects.get(pk=pk)
#     print(sort)
#     if(sort):
#         print("新しい順")
#     else:
#         print('古い順')

    params = {
        'object':object,
        "form":form,
        "reverseform":reverseform,
        "sort":sort
    }
    return render(request, "detail.html", params)


@login_required
def goodfunc(request, pk):
    posted = RecommendedBook.objects.get(pk=pk)
    post = request.user.get_username()
    if post in posted.goodtext:
        return redirect(to="home")
    posted.good+=1
    posted.goodtext =posted.goodtext+' '+post
    posted.save()
    return redirect(to="home")

@login_required
def notGoodfunc(request, pk):
    posted = RecommendedBook.objects.get(pk=pk)
    post = request.user.get_username()
    if post in posted.notGoodtext:
        return redirect(to="home")
    posted.notGood+=1
    posted.notGoodtext =posted.notGoodtext+' '+post
    posted.save()
    return redirect(to="home")

@login_required
def mypagefunc(request):
    user = request.user
    print(RecommendedBook.objects)
    object_list = RecommendedBook.objects.filter(author=user)
    tags=[]
    for item in object_list:
        tags.append(item.genre.split())
        ###
#     data=RecommendedBook.objects.all()
#     for item in data:
#         print("author:", item.genre)
        ###
    return render(request, 'mypage.html',{"object_list":object_list , "tags":tags})

# def findByGenresfunc(request,item):
#     objects_list = RecommendedBook.objects.all()
#
#     params{
#         'data':data,
#         "form":FindForm()
#     }
#     return render(request, "find.html",params)