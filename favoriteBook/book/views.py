from django.shortcuts import render, redirect, get_object_or_404
from .models import RecommendedBook#,Comment
from django.urls import reverse_lazy
from django.views.generic import CreateView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from .forms import FindForm,CommentCreateForm




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
        print(item.genre)
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
        print(str)
        data = RecommendedBook.objects.filter(genre=str)
    else:
        form=FindForm()
        data = RecommendedBook.objects.all()
    params = {
        'form':form,
        'data':data,
    }
    return render(request,'find.html',params)


def detailfunc(request, pk):
    if request.method=="POST":
        print("this is a post method")
        form = CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.target = get_object_or_404(RecommendedBook, pk=pk)
            comment.save()

    print("this is a not post mehtod")
    form=CommentCreateForm()
    object = RecommendedBook.objects.get(pk=pk)
    params = {
        'object':object,
        "form":form,
    }
    return render(request, "detail.html", params)



def goodfunc(request, pk):
    posted = RecommendedBook.objects.get(pk=pk)
    post = request.user.get_username()
    if post in posted.goodtext:
        return redirect(to="home")
    posted.good+=1
    posted.goodtext =posted.goodtext+' '+post
    posted.save()
    return redirect(to="home")

def notGoodfunc(request, pk):
    posted = RecommendedBook.objects.get(pk=pk)
    post = request.user.get_username()
    if post in posted.notGoodtext:
        return redirect(to="home")
    posted.notGood+=1
    posted.notGoodtext =posted.notGoodtext+' '+post
    posted.save()
    return redirect(to="home")

# def addGenre(request,pk):  //reqとpkを受け取る
#     posted = RecommendedBook.objects.get(pk=pk) //pkのidをもつpostを取得
#     post = request.POST['genre']//postにより受け取ったものを取得
#     if post in posted.genre://postがすでにある場合
#         return render(return,'addGenre.html',{"message":"this is already set"})//エラーを返す
#     posted.genre=posted.genre+" "+post//追加
#     posted.save()//保存
#あとあとリスト化して出力したいのでhomeで色々変更あり
#     return  redirect(to="home")


# @require_POST
# def create_comment(request, pk):
#     form = CommentCreateForm(request.POST)
#     if form.is_valid():
#         comment = form.save(commit=False)
#         comment.target = get_object_or_404(comment,pk=pk)
#         comment.save()
#         return redirect(to="home")
#     params = {
#         'object':RecommendedBook.objects.get(pk=pk),
#         'form':form,
#     }
#     return render(request, "detail.html", params)
