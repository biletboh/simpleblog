from django.shortcuts import render
from django.http import HttpResponse

from django.views.generic import View, DetailView, DeleteView, TemplateView, FormView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.edit import FormMixin
from django.views.generic.detail import SingleObjectMixin

from blog.models import UserProfile
from django.contrib.auth.models import User
from blog.forms import UserUpdateForm


class WelcomePage(TemplateView):
    template_name = 'blog/welcome.html'
    def get_context_data(self, **kwargs):
        context = super(WelcomePage, self).get_context_data(**kwargs)
        context['title'] = "Welcome page"
        return context

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
        #birthday = form.cleaned_data['birthday']
        avatar = form.cleaned_data['avatar']
        if avatar: 
            user.user_profile.avatar = avatar
        userprofile.country = country
        userprofile.city = city 
        #userprofile.birthday = birthday 

        user.save()
        return super(UserUpdateFormView, self).form_valid(form)

    def get_success_url(self):
        user = self.request.user
        return reverse("blog:profile", kwargs = {'pk': user.pk})

class UserUpdate(View):

    def get(self, request, *args, **kwargs):
        view = UserDisplay.as_view()
        return view(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        view = UserUpdateFormView.as_view()
        return view(request, *args, **kwargs)

class UserDelete(LoginRequiredMixin, DeleteView):
    model = User
    success_url = 'accounts/signup/'
