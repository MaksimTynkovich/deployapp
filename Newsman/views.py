from unicodedata import category
from Newsman.models import Profile
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.views import LoginView, PasswordResetView, PasswordChangeView
from django.contrib.messages.views import SuccessMessageMixin
from .models import *
import uuid
from django.conf import settings
from django.core.mail import send_mail
from django.contrib.auth import authenticate,login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView, DetailView, CreateView
from django.views import View
import datetime
from .forms import *
from django.urls import reverse_lazy
from django.db.models import Q


date = datetime.datetime.today()
time = str(date.day) + ' ' + '0' + str(date.month) + ' ' + str(date.year)
day = str(date.day - 1) + ' ' + '0' + str(date.month) + ' ' + str(date.year)
hours = date.hour
minutes = date.minute

def add_news(request):
    if request.method == 'POST':
        form = NewsForm(request.POST, request.FILES)
        if form.is_valid():
            display_type = request.POST.get("display_type", None)
#             print(display_type)
            if display_type in ["locationbox"]:
                pass
            else:
                form = form.save(commit=False)
                form.author = request.user
            news = form.save()
            return redirect('/')
    else:
        form = NewsForm()
    return render(request, 'add_news.html', {'form': form, 'title': 'Создать пост'})

def index(request):
    posts = News.objects.all()
    categorys = Category.objects.all()
    recommendations_posts = posts.all()

    posts_first = posts.all()
    posts_two = posts.all()
    context = {
        'recommendations_posts': recommendations_posts.filter(is_published=True)[:3],
        'title': "Новости",
        'time': time,
        'day': day,
        'posts_first': posts_first.filter(is_published=True)[:3],
        'posts_two': posts_two.filter(is_published=True)[3:]
    }
    return render(request, 'index.html', context=context)

def get_category(request, category_slug):
    category = get_object_or_404(Category, slug=category_slug)
    news = News.objects.filter(category_id = category.id)
    time = str(date.day) + ' ' + '0' + str(date.month) + ' ' + str(date.year)
    day = str(date.day - 1) + ' ' + '0' + str(date.month) + ' ' + str(date.year)
    return render(request, 'category.html', {'news': news, 'title': category.title, 'time': time, 'day': day})


def show_post(request, slug):
    post = get_object_or_404(News, slug=slug)
    comments_all = Comment.objects.all().filter(post_id=post.id)
    replys_increment = 0

    answers_list = list(comments_all.values_list('id'))

    for i in answers_list:
        for x in i:
            replys_all = Reply.objects.all().filter(comment_id=x)
            replys_increment += replys_all.count()

    comments = len(comments_all) + replys_increment
    posts_more = News.objects.all().filter(~Q(id=post.id)).filter(category=post.category.id)[:3]
    date = datetime.datetime.today()
    time = str(date.day) + ' ' + '0' + str(date.month) + ' ' + str(date.year)
    day = str(date.day - 1) + ' ' + '0' + str(date.month) + ' ' + str(date.year)
    if request.method == "POST" and request.user.is_authenticated:
        form = TextForm(request.POST)
        if form.is_valid():
            Comment.objects.create(
                user=request.user,
                post=post,
                text=form.cleaned_data.get('text')
            )
            return redirect('post', slug=slug)

    context = {
        'post': post,
        'title': post.title,
        'time': time,
        'minutes': minutes,
        'hours': hours,
        'day': day,
        'posts_more': posts_more,
        'comments': comments,
    }
    return render(request, 'post.html', context=context)

@login_required(login_url='login')
def add_reply(request, post_id, comment_id):
    post = get_object_or_404(News, id=post_id)
    if request.method == "POST":
        form = TextForm(request.POST)
        if form.is_valid():
            comment = get_object_or_404(Comment, id=comment_id)
            Reply.objects.create(
                user=request.user,
                comment=comment,
                text=form.cleaned_data.get('text')
            )
    return redirect('post', slug=post.slug)

# def logout_user(request):
#     logout(request)
#     return redirect('/')

# def login_attempt(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user_obj = User.objects.filter(username = username).first()
#         if user_obj is None:
#             messages.success(request, 'User not found.')
#             return redirect('/accounts/login')
        
        
#         profile_obj = Profile.objects.filter(user = user_obj ).first()

#         if not profile_obj.is_verified:
#             messages.success(request, 'Profile is not verified check your mail.')
#             return redirect('/accounts/login')

#         user = authenticate(username = username , password = password)
#         if user is None:
#             messages.success(request, 'Wrong password.')
#             return redirect('/accounts/login')
        
#         login(request , user)
#         return redirect('/')

#     return render(request , 'login.html')

# def register_attempt(request):

#     if request.method == 'POST':
#         username = request.POST.get('username')
#         email = request.POST.get('email')
#         password = request.POST.get('password')
#         print(password)

#         try:
#             if User.objects.filter(username = username).first():
#                 messages.success(request, 'Username is taken.')
#                 return redirect('/register')

#             if User.objects.filter(email = email).first():
#                 messages.success(request, 'Email is taken.')
#                 return redirect('/register')
            
#             user_obj = User(username = username , email = email)
#             user_obj.set_password(password)
#             user_obj.save()
#             auth_token = str(uuid.uuid4())
#             profile_obj = Profile.objects.create(user = user_obj , auth_token = auth_token)
#             profile_obj.save()
#             send_mail_after_registration(email , auth_token)
#             return redirect('/token')

#         except Exception as e:
#             print(e)


#     return render(request , 'register.html')

# def success(request):
#     return render(request , 'success.html')

def post(request):
    return render(request , 'post.html')


# def token_send(request):
#     return render(request , 'token_send.html')


# def verify(request , auth_token):
#     try:
#         profile_obj = Profile.objects.filter(auth_token = auth_token).first()
#         if profile_obj:
#             if profile_obj.is_verified:
#                 messages.success(request, 'Your account is already verified.')
#                 return redirect('/accounts/login')
#             profile_obj.is_verified = True
#             profile_obj.save()
#             messages.success(request, 'Your account has been verified.')
#             return redirect('/accounts/login')
#         else:
#             return redirect('/error')
#     except Exception as e:
#         print(e)
#         return redirect('/')

# def error_page(request):
#     return  render(request , 'error.html')


# def send_mail_after_registration(email , token):
#     subject = 'Your accounts need to be verified'
#     message = f'Hi paste the link to verify your account http://127.0.0.1:8000/verify/{token}'
#     email_from = settings.EMAIL_HOST_USER
#     recipient_list = [email]
#     send_mail(subject, message , email_from ,recipient_list )
    

class RegisterView(View):
    form_class = RegisterForm
    initial = {'key': 'value'}
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        # will redirect to the home page if a user tries to access the register page while logged in
        if request.user.is_authenticated:
            return redirect(to='/')

        # else process dispatch as it otherwise normally would
        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        form = self.form_class(initial=self.initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            form.save()

            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}')

            return redirect(to='login')

        return render(request, self.template_name, {'form': form})


# Class based view that extends from the built in login view to add a remember me functionality
class CustomLoginView(LoginView):
    form_class = LoginForm

    def form_valid(self, form):
        remember_me = form.cleaned_data.get('remember_me')

        if not remember_me:
            # set session expiry to 0 seconds. So it will automatically close the session after the browser is closed.
            self.request.session.set_expiry(0)

            # Set session as modified to force data updates/cookie to be saved.
            self.request.session.modified = True
    
        # else browser session will be as long as the session cookie time "SESSION_COOKIE_AGE" defined in settings.py
        return super(CustomLoginView, self).form_valid(form)

class ResetPasswordView(SuccessMessageMixin, PasswordResetView):
    template_name = 'users/password_reset.html'
    email_template_name = 'users/password_reset_email.html'
    subject_template_name = 'users/password_reset_subject'
    success_message = "We've emailed you instructions for setting your password, " \
                      "if an account exists with the email you entered. You should receive them shortly." \
                      " If you don't receive an email, " \
                      "please make sure you've entered the address you registered with, and check your spam folder."
    success_url = reverse_lazy('home')


class ChangePasswordView(SuccessMessageMixin, PasswordChangeView):
    template_name = 'users/change_password.html'
    success_message = "Successfully Changed Your Password"
    success_url = reverse_lazy('home')


@login_required
def profile(request):
    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)
        profile_form = UpdateProfileForm(request.POST, request.FILES, instance=request.user.profile)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            messages.success(request, 'Your profile is updated successfully')
            return redirect(to='user-profile')
    else:
        user_form = UpdateUserForm(instance=request.user)
        profile_form = UpdateProfileForm(instance=request.user.profile)

    return render(request, 'users/profile.html', {'user_form': user_form, 'profile_form': profile_form})
