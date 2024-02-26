from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

from forum.models import Post
from .models import Profile
from .token import account_activation_token
from django.contrib import messages
from django.contrib.auth.forms import PasswordResetForm
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

account_activation_token: object = default_token_generator


def SendMail(request):
    current_site = get_current_site(request)
    mail_subject = 'Hesabınızı aktifleştirin.'
    message = render_to_string('account/acc_active_email.html', {
        'user': request.user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(request.user.pk)),
        'token': account_activation_token.make_token(request.user),
    })
    to_email = request.user.email
    email = EmailMessage(
        mail_subject, message, to=[to_email]
    )
    email.send()
    return render(request, "account/email.html", {"success": "Aktivasyon linki mailinize gönderildi."})


def signin(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            next_url = request.POST.get('next')
            if next_url:
                print(next_url + 'next')
                return redirect(next_url)
            else:
                return redirect('home')
        else:
            data = {
                'message': True,
                'messagetype': 'error',
                'messagetitle': 'Hata',
                'messagecontent': 'Kullanıcı adı veya şifre hatalı',
            }
            return render(request, 'account/signin.html', data)

    if request.user.is_authenticated:
        return redirect("forum")

    return render(request, "account/signin.html")


def register(request):
    if request.user.is_authenticated:
        return redirect("forum")
    if request.method == "POST":
        FormFirstName = request.POST.get('firstname')
        Formusername = request.POST.get('username')
        Formemail = request.POST.get('email')
        Formpassword = request.POST.get('password')
        Formrepassword = request.POST.get('repassword')
        if Formpassword == Formrepassword:
            if User.objects.filter(username=Formusername).exists():
                data = {
                    'message':True,
                    'messagetype':'error',
                    'messagetitle':'Hata',
                    'messagecontent':'Bu kullanıcı adı daha önceden alınmış lütfen farklı bir kullanıcı adı giriniz',
                    "firstname": FormFirstName,
                    "email": Formemail
                }
                return render(request, "account/signup.html",data)
            else:
                if User.objects.filter(email=Formemail).exists():
                    data = {
                        'message': True,
                        'messagetype': 'error',
                        'messagetitle': 'Hata',
                        'messagecontent': 'Bu email ile daha önceden kayıt olunmuş!',
                        "firstname": FormFirstName,
                        "username": Formusername,
                    }
                    return render(request, "account/signin.html",data)
                else:
                    user = User.objects.create_user(first_name=FormFirstName,
                                                    username=Formusername, email=Formemail, password=Formpassword,
                                                    is_superuser=0, is_active=0)
                    user.save()
                    current_site = get_current_site(request)
                    mail_subject = 'Hesabınızı aktifleştirin.'
                    message = render_to_string('account/acc_active_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': account_activation_token.make_token(user),
                    })
                    to_email = Formemail
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                    )
                    email.send()
                    return render(request, "account/email.html", {"success": "Aktivasyon linki mailinize gönderildi."})
        else:
            data = {
                'message': True,
                'messagetype': 'error',
                'messagetitle': 'Hata',
                'messagecontent': 'Şifreler eşleşmiyor!',
            }
            return render(request, "account/signup.html", data)
    return render(request, "account/signup.html")


def activate(request, uidb64, token):
    user = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = user.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return render(request, 'account/email.html', {"success": "Hesabınız başarıyla aktif edildi. Tıklayarak forum sayfasına geçebilirsiniz", "active": True})
    else:
        return render(request, 'account/email.html', {"error": "Aktivasyon linki geçersiz!", 'errorr': True})


@login_required(login_url='signin')
def profile(request):
    if request.user.is_authenticated:
        approved_posts = Post.objects.filter(status='approved')
        rejected_posts = Post.objects.filter(status='rejected')
        pending_posts = Post.objects.filter(status='pending')

        paginator_approved = Paginator(approved_posts, 10)  # 10 posts per page
        paginator_rejected = Paginator(rejected_posts, 10)
        paginator_pending = Paginator(pending_posts, 10)

        page_number_approved = request.GET.get('page_approved')
        page_number_rejected = request.GET.get('page_rejected')
        page_number_pending = request.GET.get('page_pending')

        try:
            approved_posts = paginator_approved.page(page_number_approved)
        except PageNotAnInteger:
            approved_posts = paginator_approved.page(1)
        except EmptyPage:
            approved_posts = paginator_approved.page(paginator_approved.num_pages)

        try:
            rejected_posts = paginator_rejected.page(page_number_rejected)
        except PageNotAnInteger:
            rejected_posts = paginator_rejected.page(1)
        except EmptyPage:
            rejected_posts = paginator_rejected.page(paginator_rejected.num_pages)

        try:
            pending_posts = paginator_pending.page(page_number_pending)
        except PageNotAnInteger:
            pending_posts = paginator_pending.page(1)
        except EmptyPage:
            pending_posts = paginator_pending.page(paginator_pending.num_pages)

        data = {
            'profile': Profile.objects.get(user=request.user),
            'approved_posts': approved_posts,
            'rejected_posts': rejected_posts,
            'pending_posts': pending_posts,
        }
        return render(request, "account/profile.html", data)
    return redirect("forum")


def password_reset_request(request):
    if request.method == "POST":
        password_reset_form = PasswordResetForm(request.POST)
        if password_reset_form.is_valid():
            data = password_reset_form.cleaned_data['email']
            associated_users = User.objects.filter(email=data)
            if associated_users.exists():
                for user in associated_users:
                    current_site = get_current_site(request)
                    subject = 'Şifre Sıfırlama Talebi'
                    message = render_to_string('account/pass_reset_email.html', {
                        'user': user,
                        'domain': current_site.domain,
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': default_token_generator.make_token(user),
                    })
                    user.email_user(subject, message)
                return render(request,'account/password_reset_done.html')
            else:
                messages.error(request, 'Bu email ile kayıtlı kullanıcı bulunamadı.')
    else:
        password_reset_form = PasswordResetForm()
    return render(request=request, template_name='account/password_reset.html', context={'password_reset_form': password_reset_form})


def logout_request(request):
    logout(request)
    return redirect("forum")
