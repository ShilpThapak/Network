from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
from .models import User, post
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator


def index(request):
    allpost=post.objects.all().order_by("-time")
    paginator = Paginator(allpost, 10)
    pageno = request.GET.get('page')
    pageobj = paginator.get_page(pageno)

    return render(request, "network/index.html", {
        "post": post.objects.all().order_by("-time"),
        "pageobj": pageobj
    })

@login_required(login_url='/login/')
def create(request):
    if request.method=="POST":
        text = request.POST["newposttext"]
        userid = request.POST["userid"]
        user = User.objects.get(pk=userid)
        newpost = post(author=user, text=text)
        newpost.save()
        return HttpResponseRedirect(reverse('index'))

def profile(request, profileuser):
    profileuser = User.objects.get(username=profileuser)
    followers = profileuser.follower.all().count()
    following = profileuser.following.all().count()
    
    allpost=post.objects.filter(author=profileuser).order_by("-time")
    paginator = Paginator(allpost, 10)
    pageno = request.GET.get('page')
    pageobj = paginator.get_page(pageno)

    return render(request, "network/profile.html", {
        "post": post.objects.filter(author=profileuser).order_by("-time"),
        "pageobj":pageobj,
        "profileuser": profileuser,
        "followers": followers,
        "following": following,
    })

@login_required(login_url='/login/')
def follow(request):
    profileusername = request.POST["profileuser"]
    username = request.POST["user"]
    profileuser = User.objects.get(username=profileusername)
    user = User.objects.get(username=username)
    user.following.add(profileuser)
    return HttpResponseRedirect(reverse('profile', args=(profileuser,)))
    
@login_required(login_url='/login/')
def unfollow(request):
    profileusername = request.POST["profileuser"]
    username = request.POST["user"]
    profileuser = User.objects.get(username=profileusername)
    user = User.objects.get(username=username)
    user.following.remove(profileuser)
    return HttpResponseRedirect(reverse('profile', args=(profileuser,)))

def following(request):
    allpost=post.objects.filter(author__in=request.user.following.all()).order_by("-time")
    paginator = Paginator(allpost, 10)
    pageno = request.GET.get('page')
    pageobj = paginator.get_page(pageno)
    
    return render(request, "network/following.html", {
        "pageobj": pageobj
    })

@csrf_exempt
def postdata(request, postid):
 #   if request.method == "PUT":
  #      postitem = post.objects.get(id=postid)
  #      data = json.loads(request.body)
  #      postitem.text = data["text"]
  #      postitem.save()
   #     return HttpResponse(status=204)
    if request.method == 'POST':
        text = request.POST['text']
        postitem = post.objects.get(id=postid)
        postitem.text = text
        postitem.save()
        return HttpResponse(status=204)
        #return JsonResponse({"text": text}, status=201)

@login_required(login_url='/login/')
@csrf_exempt
def like(request, postid):
    if request.method == 'POST':
        userid = request.POST['userid']
        print("working!")
        print(userid)
        print(postid)
        postitem = post.objects.get(id=postid)
        user = User.objects.get(id=userid)
        print("likes:", postitem.likers.count())
        print("likes in model:", postitem.likes)
        postitem.likers.add(user)
        postitem.likes= postitem.likers.count()
        postitem.save()
        print("likes:", postitem.likers.count())
        print("likes in model:", postitem.likes)
        #return HttpResponse(status=204)
        return JsonResponse({"likes": postitem.likes}, status=201)

@login_required(login_url='/login/')
@csrf_exempt
def unlike(request, postid):
    if request.method == 'POST':
        userid = request.POST['userid']
        print("working!")
        print(userid)
        print(postid)
        postitem = post.objects.get(id=postid)
        user = User.objects.get(id=userid)
        print("likes:", postitem.likers.count())
        print("likes in model:", postitem.likes)
        postitem.likers.remove(user)
        postitem.likes= postitem.likers.count()
        postitem.save()
        print("likes:", postitem.likers.count())
        print("likes in model:", postitem.likes)
        #return HttpResponse(status=204)
        return JsonResponse({"likes": postitem.likes}, status=201)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")
