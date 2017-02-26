from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse

from django.views.generic import View, DetailView, DeleteView, TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin
from django.contrib.messages.views import SuccessMessageMixin

from blog.models import UserProfile, Post
from django.contrib.auth.models import User
from blog.forms import UserUpdateForm, PostForm

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

class UserDisplay(DetailView):
    model = User
    template_name = 'blog/update-profile.html'

    def get_context_data(self, **kwargs):
        context = super(UserDisplay, self).get_context_data(**kwargs)
        context['form'] = UserUpdateForm() 
        context['title'] = "Update Profile"
        return context
 
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
class UserUpdate(View):

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
class Blog(AjaxListView):
    context_object_name = "posts"
    template_name = 'blog/blog.html'
    page_template = 'blog/post_list.html'
    
    def get_queryset(self):
        return Post.objects.all()
# Post page
class PostPage(DetailView):
    model = Post 
    template_name = 'blog/post.html'
    def get_context_data(self, **kwargs):
        context = super(PostPage, self).get_context_data(**kwargs)
        return context

#Create Post Page
class CreatePost(SuccessMessageMixin, LoginRequiredMixin, FormView):
    form_class = PostForm 
    template_name = 'blog/create.html'
    success_url = '/'
    login_url = '/accounts/login'
    success_message = "A post was created successfully"
    def form_valid(self, form):
        post = Post(name=form.cleaned_data['name'], pub_date=form.cleaned_data['pub_date'], body=form.cleaned_data['body'], image=form.cleaned_data['image'])
        post.save()
        form.delete_temporary_files()
        return super(CreatePost, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(CreatePost, self).get_context_data(**kwargs)
        context['title'] = 'Create Posts'
        return context   

#Delete News page
class DeletePost(LoginRequiredMixin, DeleteView):
    model = Post 
    template_name = 'blog/delete-post.html'
    success_url = '/blog' 

#Edit News Page
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
