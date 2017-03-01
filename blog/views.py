from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.utils import timezone

from django import forms
from django.views.generic import View, DetailView, CreateView, DeleteView, TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin

from blog.models import UserProfile, Post, Comment, Like
from django.contrib.auth.models import User
from blog.forms import UserUpdateForm, PostForm, CommentForm, LikeForm, BlogFilterForm

from el_pagination.views import AjaxListView

# Base Page
class WelcomePage(TemplateView):
    template_name = 'blog/welcome.html'
    def get_context_data(self, **kwargs):
        context = super(WelcomePage, self).get_context_data(**kwargs)
        context['title'] = "Welcome page"
        return context

# User Management 

# Profile Page
class UserProfile(LoginRequiredMixin, DetailView):
    template_name = 'blog/profile.html'
    model = User
    def get_context_data(self, **kwargs):
        context = super(UserProfile, self).get_context_data(**kwargs)
        context['title'] = "User Profile"
        return context

# Render User data
class UserDisplay(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'blog/update-profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserDisplay, self).get_context_data(**kwargs)
        context['form'] = UserUpdateForm() 
        context['title'] = "Update Profile"
        return context

# Edit User data  
class UserUpdateFormView(LoginRequiredMixin, SingleObjectMixin, FormView):
    form_class = UserUpdateForm
    success_url = '/'
    model = User

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UserUpdateFormView, self).post(request, *args, **kwargs)

    def form_valid(self, form):
        user = self.request.user
        userprofile = user.user_profile 
        user.username = form.cleaned_data['username']
        user.email =  form.cleaned_data['email']
        user.first_name = form.cleaned_data['first_name']
        user.last_name = form.cleaned_data['last_name']
        
        country = form.cleaned_data['country']
        city = form.cleaned_data['city']
        birthday = form.cleaned_data['birthday']
        avatar = form.cleaned_data['avatar']
        if avatar: 
            user.user_profile.avatar = avatar
        userprofile.country = country
        userprofile.city = city 
        userprofile.birthday = birthday 

        user.save()
        return super(UserUpdateFormView, self).form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse("blog:profile", kwargs = {'pk': user.pk})

# Update Profile
class UserUpdate(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        view = UserDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UserUpdateFormView.as_view()
        return view(request, *args, **kwargs)

# Delete Profile
class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = 'accounts/signup/'

# Blog CRUD

# List of posts
class Blog(LoginRequiredMixin, AjaxListView):
    context_object_name = "posts"
    template_name = 'blog/blog.html'
    page_template = 'blog/post_list.html'
    success_url = '/blog'
    
    def get_queryset(self):
        queryset = Post.objects.all()
        if self.request.method == 'POST':
            form = BlogFilterForm(self.request.POST)
            if form.is_valid():
                name = form.cleaned_data['name']
                country = form.cleaned_data['country']
                city = form.cleaned_data['city']

                # basic filter that search for the posts with the exact name
                if name:
                    queryset = queryset.filter(name=name)  

                # basic filter that search for the posts created by users from 
                # queried country 
                if country:
                    user = User.objects.filter(user_profile__country=country)
                    queryset = queryset.filter(user=user) 

                # basic filter that search for the posts created by users from 
                # queried country 
                if city:
                    user = User.objects.filter(user_profile__city=city)
                    queryset = queryset.filter(user=user) 
        else:
            queryset = queryset
        return queryset 

    def get_context_data(self, **kwargs):
        context = super(Blog, self).get_context_data(**kwargs)
        context['form'] = BlogFilterForm()
        return context

    def post(self, request, *args, **kwargs):
        return super(Blog, self).get(request, args, kwargs)

#Create Post 
class CreatePost(SuccessMessageMixin, LoginRequiredMixin, FormView):
    form_class = PostForm 
    template_name = 'blog/create.html'
    success_url = '/blog'
    login_url = '/accounts/login'
    success_message = "A post was created successfully"
    def form_valid(self, form):
        user = self.request.user
        post = Post(user=user, name=form.cleaned_data['name'], pub_date=form.cleaned_data['pub_date'], body=form.cleaned_data['body'], image=form.cleaned_data['image'])
        post.save()
        form.delete_temporary_files()
        return super(CreatePost, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['title'] = 'Create Posts'
        return context   

#Delete Post 
class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post 
    template_name = 'blog/delete-post.html'
    success_url = '/blog' 

#Edit Post 
class DisplayPost(LoginRequiredMixin, DetailView):
    template_name = 'blog/edit.html'
    login_url = '/accounts/login'
    model = Post 
    def get_context_data(self, **kwargs):
        context = super(DisplayPost, self).get_context_data(**kwargs)
        context['form'] = PostForm()
        context['title'] = 'Post' 
        return context

class UpdatePost(SuccessMessageMixin, SingleObjectMixin, FormView):
    form_class = PostForm 
    model = Post 
    success_message = "A post was updated successfully"

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super(UpdatePost, self).post(request, *args, **kwargs)
 
    def form_valid(self, form):
        #obtain current object 
        params = { 'pk': form.cleaned_data['object_id'] }
        post = Post.objects.get(**params)
        post.name = form.cleaned_data['name'] 
        post.pub_date=form.cleaned_data['pub_date']
        post.body = form.cleaned_data['body'] 
        image = form.cleaned_data['image']
        if image: 
            post.image = image
        post.save()

        form.delete_temporary_files()
        return super(UpdatePost, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:edit-post', kwargs={'pk': self.object.pk})

class EditPost(View):
    def get(self, request, *args, **kwargs):
        view = DisplayPost.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UpdatePost.as_view()
        return view(request, *args, **kwargs)


# Render Posts and create comments

# Post page that displays post and comments. 
class PostAndCommentList(LoginRequiredMixin, AjaxListView):
    context_object_name = "comments"
    template_name = 'blog/post.html'
    page_template = 'blog/comment_list.html'
    
    def get_context_data(self, **kwargs):
        context = super(PostAndCommentList, self).get_context_data(**kwargs)
        context['post'] = Post.objects.get(pk= self.kwargs['pk'])
        context['form'] = CommentForm()
        context['like_form'] = LikeForm()
        return context

    def get_queryset(self, **kwargs):
        post = Post.objects.get(pk= self.kwargs['pk'])
        return Comment.objects.filter(article = post) 
    
# Create Comment
class CreateComment(SuccessMessageMixin, LoginRequiredMixin, SingleObjectMixin, FormView):
    form_class = CommentForm 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Post.objects.all())
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super(CreateComment, self).post(request, *args, **kwargs) 

    def form_valid(self, form):
        
        user = self.request.user
        article = self.object
        comment = article.comment_set.create(user=user, body=form.cleaned_data['body'])
        comment.save()
        return super(CreateComment, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post-page', kwargs={'pk': self.object.pk})


# Combine post, list, and create comment 
class PostPage(View):
    def get(self, request, *args, **kwargs):
        view = PostAndCommentList.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'comment' in request.POST:
            view = CreateComment.as_view()
        elif 'like' in request.POST:
            view = Like.as_view()
        elif 'delete-like' in request.POST:
            view = DeleteLike.as_view()
        return view(request, *args, **kwargs)

# Delete Comment 

# Like Button
class Like(SuccessMessageMixin, LoginRequiredMixin, SingleObjectMixin, FormView):
    form_class = LikeForm 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Post.objects.all())
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super(Like, self).post(request, *args, **kwargs) 

    def form_valid(self, form):
        user = self.request.user
        article = self.object
        try:
            article.like_set.get(user=user)
        except:
            like = article.like_set.create(user=user)
            like.save()
        return super(Like, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post-page', kwargs={'pk': self.object.pk})

# Delete Like 
class DeleteLike(SuccessMessageMixin, LoginRequiredMixin, SingleObjectMixin, FormView):
    form_class = LikeForm 
    def post(self, request, *args, **kwargs):
        self.object = self.get_object(queryset=Post.objects.all())
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)
        return super(DeleteLike, self).post(request, *args, **kwargs) 

    def form_valid(self, form):
        user = self.request.user
        article = self.object
        try:
            article.like_set.get(user=user)
            article.like_set.get(user=user).delete()
        except:
            pass

        return super(DeleteLike, self).form_valid(form)

    def get_success_url(self):
        return reverse('blog:post-page', kwargs={'pk': self.object.pk})


