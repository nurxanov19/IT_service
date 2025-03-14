from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy

from .forms import RegisterForm, PostForm, ProfileUpdateForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from .models import Post, Profile
from django.views import View
from django.contrib.auth.models import User

# Create your views here.


@login_required(login_url='/login')
def home(request):
    query = request.GET.get('query') # tuple -- ('query','')
    posts = Post.objects.all()


    if query:
        posts = posts.filter(
            Q(title__icontains=query) | Q(description__icontains=query) | Q(author__username__icontains=query)
        )

    paginator = Paginator(posts, 2)
    page_number = request.GET.get("page")

    try:
        page_obj = paginator.page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    if request.method == 'POST':
        post_id = request.POST.get('post-id')
        post = Post.objects.filter(id=post_id).first()
        if post and post.author == request.user:
            post.delete()
            return render(request, 'main/home.html', {'page_obj': page_obj, 'query': query})
    # print(posts.image.url)


    return render(request, 'main/home.html', {'page_obj': page_obj, 'query': query})



# def home(request):
#
#
#     posts = Post.objects.all()
#
#     return render(request, 'main/home.html', {'posts': posts})


@login_required(login_url='/login')
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/home')

    else: form = PostForm()
    return render(request, 'main/create_post.html', {'form': form})

def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)  # request.POST posting data to form
        if form.is_valid():
            user = form.save()
            Profile.objects.create(user=user)
            login(request, user)
            return redirect('ask-profile')
    else:                                   # agar user
        form = RegisterForm()   # if there is no data, and request method is not POST, instead it is GET we just create a form

    return render(request, 'registration/sign_up.html', {'form': form})


# CRUD

class PostUpdate(View):
    template_name = 'main/update.html'

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(instance=post)
        return render(request, self.template_name, {'form': form})

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        form = PostForm(request.POST, request.FILES, instance=post)  # Fix applied

        if form.is_valid():
            form.save()
            return redirect(reverse_lazy('detail-post', kwargs={'pk': post.pk}))

        return render(request, self.template_name, {'form': form})


class PostDetail(View):

    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'main/detail.html', {'post': post})


# @login_required
# def profile_view(request):
#
#     profile = Profile.objects.get_or_create(user=request.user)
#     return render(request, 'main/profile.html', {'profile': profile})


@login_required
def profile_view(request):
    # profile, created = Profile.objects.get_or_create(user=request.user)
    profile = request.user.profile

    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=profile, user=request.user)
        if form.is_valid():
            form.save()
            return redirect('profile')

    else:
        form = ProfileUpdateForm(instance=profile, user=request.user)

    return render(request, 'main/profile.html', {'form': form, 'profile': profile})


def ask_profile(request):
    return render(request, 'main/ask_profile.html')





# @login_required(login_url='/login')     # login_url=...  agar biz login qilmagan bo'lsak bizni ... url da yuboradi. Ishlashi: agar login qilinmagan bo'lsa home page ga qo'ymaydi 'login/' pageda turaveradi
# def home(request):
#     query = request.GET.get('query')
#     posts = Post.objects.all()
#
#     if query:
#         posts = posts.filter(Q(name__icontains=query) | Q(description__icontains=query))
#
#
#     paginator = Paginator(posts, 2)
#     page_number = request.GET.get("page")
#     page_obj = paginator.get_page(page_number)
#
#
#     if request.method == 'POST':
#         post_id = request.POST.get('post-id')
#         post = Post.objects.filter(id=post_id).first()
#         if post and post.author == request.user:
#             post.delete()
#
#         posts = Post.objects.all()
#         paginator = Paginator(posts, 2)
#         page_obj = paginator.get_page(page_number)
#
#     return render(request, 'main/home.html', {'page_obj': page_obj, 'query': query, 'posts': posts})



# class SoftwareList(LoginRequiredMixin, View):
#     login_url = 'login'
#     def get(self, request):
#
#         query = request.GET.get('query')
#         posts = Post.objects.all()
#         user = request.user
#         if query:
#             posts = Post.objects.filter(Q(name__icontains=query) | Q(price__icontains=query))
#
#
#         paginator = Paginator(posts, 2)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(request, 'main/home.html', {'page_obj': page_obj, 'user': user})
#
#     def post(self, request):
#         posts = Post.objects.all()
#         if request.method == 'POST':
#             post_id = request.POST.get('post-id')
#             post = Post.objects.filter(id=post_id).first()
#             if post and post.author == request.user:
#                 post.delete()
#
#         paginator = Paginator(posts, 2)
#         page_number = request.GET.get("page")
#         page_obj = paginator.get_page(page_number)
#         return render(request, 'main/home.html', {'page_obj': page_obj})