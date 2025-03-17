from django.shortcuts import get_object_or_404, render, HttpResponse
from .models import User,UserProfile,Post,Comment,Follow
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.conf import settings
from datetime import datetime
from.forms import UserForm, UserProfileForm, PostForm, CommentForm



# Create your views here.

def welcome_page(request):
    return render(request, "TripMates/welcome.html")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username = username, password = password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse("TripMates:posts"))
            else:
                return HttpResponse("Your Trip Mates account is not active.")
        else:
            print(f"Invalid login details {username}, {password}")
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, "TripMates/login.html")
    
def register(request):
    registered = False

    if request.method == "POST":
        user_form = UserForm(request.POST)
        profile_form = UserProfileForm(request.POST)

        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            
            user.set_password(user.password)
            user.save

            profile = profile_form.save(commit=False)
            profile.user = user

            if "picture" in request.FILES:
                profile.picture = request.FILES["picture"]

            profile.save()

            registered = True
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = UserForm()
        profile_form = UserProfileForm()

    return render(request, "TripMates/register.html", context={"user_form": user_form, "profile_form" : profile_form, "registered": registered})

@login_required
def user_logout(request):
    logout(request)

    return redirect(reverse("TripMates:Login"))

@login_required
def homepage(request):
    postList = Post.objects.order_by("-date_uploaded")
    context_dict = {}
    context_dict["posts"] = postList

    visitor_cookie_handler(request)
    return render(request, "TripMates/homepage.html", context=context_dict)


@login_required
def follow_user(request, user_id):
    user_to_follow = get_object_or_404(User, id=user_id)
    Follow.objects.get_or_create(follower=request.user, followed=user_to_follow)
    return redirect('profile', user_id=user_id)

@login_required
def unfollow_user(request, user_id):
    user_to_unfollow = get_object_or_404(User, id=user_id)
    Follow.objects.filter(follower=request.user, followed=user_to_unfollow).delete()
    return redirect('profile', user_id=user_id)

@login_required
def create_post(request, post_id):
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid:
            post = form.save(commit=False)
            post.author = request.user
            post.save
            return redirect(reverse("TripMates:Welcome")) # CHANGE WELCOME TO VIEW THE UPLOADED POST
        else:
            form = PostForm()

        return render(request, "TripMates/CreatePost.html", {"form" : form})
    
@login_required
def view_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    comments = post.comments.all()  # Fetch all comments for this post
    form = CommentForm()

    return render(request, 'TripMates/view_posts.html', {
        'post': post,
        'comments': comments,
        'form': form
    })
    
@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.post = post
            comment.save()
            return redirect('post_detail', post_id=post.id)  # Redirect to the post page
    
    else:
        form = CommentForm()
    
    return render(request, 'TripMates/add_comment.html', {'form': form, 'post': post})

def view_profile(request, user_id):
    user = get_object_or_404(User, id=user_id)
    posts = Post.objects.filter(user = user)
    profile = get_object_or_404(UserProfile, id=user_id)

    contextdict = {}
    contextdict["posts"] = posts
    contextdict["username"] = user.username
    contextdict["profile_picture"] = profile.picture

    return render(request, "TripMates/view_profile.html", context=contextdict)

def visitor_cookie_handler(request):
    visits = int(request.COOKIES.get("visits",1))

    last_visit_cookie = request.COOKIES.get("last_visit", str(datetime.now()))
    last_visit_time = datetime.strptime(last_visit_cookie[:-7],"%Y-%m-%d %H:%M:%S")

    if (datetime.now() - last_visit_time).days > 0:
        visits +=1
        request.session["last_visit"] = str(datetime.now())
    else:
        request.session["last_visit"] = last_visit_cookie
    
    request.session["visits"] = visits


#helper method
def get_server_side_cookie(request, cookie, default_val=None):
    val = request.session.get(cookie)
    if not val:
        val = default_val
    return val


