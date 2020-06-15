from django.shortcuts import render, redirect, get_object_or_404
from .models import RecommendedBook#,Comment
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib.auth import logout
from .forms import FindForm,CommentCreateForm,RadioForm,newTagForm
from django.db.models import Q




def signupfunc(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
        try:
            User.objects.get(username=username)
            return render(request, "signup.html",{"error":"this user is already registered","error2":"please register another name"})
        except:
            user = User.objects.create_user(username, "", password)
            return redirect(to="login")
#             return render(request,"signup.html",{'title':'signup'})
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
    return render(request, "login.html",{"title":"login"})

def logoutfunc(request):
    logout(request)
    return redirect(to="login")


# @login_required
def homefunc(request):
    object_list = RecommendedBook.objects.all()
    tags=[]
    for object in object_list:
        object_item=[]
        taglong=""
        items = object.genre.split()
#         print("items",items)
        for item in items:
            taglong+=item
            object_item.append(item)
            if len(taglong)>15:
                if len(taglong)>20:
                    over_item=object_item.pop()
                    over_str = len(taglong)-20
#                     print(over_str)
#                     print("over",over_item[0:len(over_item)-over_str])
                    object_item.append(over_item[0:len(over_item)-over_str]+"...")

                object_item.append("...")
                break
        tags.append(object_item)
#
    return render(request, 'home.html',{'title':'home', 'object_list':object_list,'tags':tags})


#詳細

#作成
class dataCreate(CreateView):
    template_name="create.html"
    model=RecommendedBook
    fields=('author','bookTitle',"content","bookImage","genre")
    success_url = reverse_lazy('home')

def findfunc(request):
    selecttags=[]
    aboutTags=[]
    all=RecommendedBook.objects.all()
    for words in all:
        aboutTags.append(words.genre)
        for word in words.genre.split():
            if word not in selecttags:
                selecttags.append(word)

    if (request.method=="POST"):
        try:
            str = request.POST['find']
            data = RecommendedBook.objects.filter(genre__contains=str)
            form = FindForm(request.POST)

        except:
            checks_value = request.POST.getlist('chekcs[]')
            checked_tags=[]
            for tag in aboutTags:
                for i in range(len(checks_value)):
                    if checks_value[i] in tag:
                        checked_tags.append(tag)
            checked_tags=set(checked_tags)
            data = RecommendedBook.objects.filter(genre__in=checked_tags)
            form = FindForm()
        if len(data)==0:
            data=0
    else:
        form=FindForm()
        data = RecommendedBook.objects.all()
    all=data
    tags=[]
    for object in all:
        object_item=[]
        taglong=""
        items = object.genre.split()
        for item in items:
            taglong+=item
            object_item.append(item)
            if len(taglong)>15:
                if len(taglong)>20:
                    over_item=object_item.pop()
                    over_str = len(taglong)-20
#                     print(over_str)
#                     print("over",over_item[0:len(over_item)-over_str])
                    object_item.append(over_item[0:len(over_item)-over_str]+"...")

                object_item.append("...")
                break
        tags.append(object_item)

    params = {
        'form':form,
        'data':data,
        "selecttags":selecttags,
        "tags":tags,
        "title":"find",
    }
    return render(request,'find.html',params)


def detailfunc(request, pk):
    sort=True
    if request.method=="POST":
        form = CommentCreateForm(request.POST)
#         print(request.POST)
        reverseform=RadioForm(request.POST)
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
    params = {
        'object':object,
        "form":form,
        "reverseform":reverseform,
        "sort":sort,
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
    object_list = RecommendedBook.objects.filter(author=user)
    tags=create_tags(object_list)
    params={
    "object_list":object_list ,
     "tags":tags,
     "title":"mypage",
     }
    return render(request, 'mypage.html',params)

def create_tags(object_list):
    tags=[]
    for object in object_list:
        object_item=[]
        taglong=""
        items = object.genre.split()
        for item in items:
            taglong+=item
            object_item.append(item)
            if len(taglong)>15:
                if len(taglong)>20:
                    over_item=object_item.pop()
                    over_str = len(taglong)-20
                    object_item.append(over_item[0:len(over_item)-over_str]+"...")
                else:
                    object_item.append("...")
                break
            tags.append(object_item)
    return tags    



@login_required
def changeTagfunc(request, pk):
    object = RecommendedBook.objects.get(pk=pk)
    tags = object.genre.split()
    if request.method=="POST":
        deletetag=request.POST["tag1"].strip()
        newtag=request.POST['tag2']
#         print(deletetag)
#         print(newtag)
        if (deletetag!="")and(deletetag in object.genre):
            object.genre = object.genre.replace(deletetag+" ","")
            object.save()

        object.genre += " "+newtag
        object.save()
        return redirect(to="home")
#     print("全オブジェクト：",object.genre)
    params = {
        "form":newTagForm,
        "tags":tags,
    }
    return render(request, "changeTag.html", params)


class dataDelete(DeleteView):
    model=RecommendedBook
    success_url=reverse_lazy('mypage')

def userPostsfunc(request, targetUser):
    object_list = RecommendedBook.objects.filter(author=targetUser)
    # print(data)
    tags = create_tags(object_list)
    params={
    "object_list":object_list ,
    "tags":tags,
     "title":"mypage",
     "target":targetUser,
     }
    
    if(targetUser==request.user):
        return redirect(to="mypage")
        #  return (request, "mypage.html", params)

    return render(request, 'userpage.html',params)

