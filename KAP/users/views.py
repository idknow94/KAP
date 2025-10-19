from django.urls import reverse_lazy
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views import View
from django.views.generic import CreateView
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import login
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from issues.models import Issue
from .forms import CampionSignupForm, EditProfileForm, AVATAR_CHOICES
from .models import Profile


class CampionSignupView(CreateView):
    template_name = 'users/signup.html'
    form_class = CampionSignupForm
    success_url = reverse_lazy('login')

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # ❌ REMOVE THIS if you have a signal creating the profile automatically
        # Profile.objects.create(user=user)

        self.send_verification_email(self.request, user)
        return render(self.request, 'users/verify_sent.html', {'email': user.email})

    def send_verification_email(self, request, user):
        current_site = get_current_site(request)
        subject = "Verify your KAP account"
        message = render_to_string('users/verify_email.html', {
            'user': user,
            'domain': request.get_host(),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })
        email = EmailMessage(subject, message, to=[user.email])
        email.content_subtype = "html"  # important: render HTML email
        email.send()


class VerifyEmailView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, 'users/verify_success.html', {'user': user})
        else:
            return render(request, 'users/verify_failed.html')

# Login view (optional if using Django auth)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})


def profile_view(request, username):
    user = get_object_or_404(User, username=username)
    issues = Issue.objects.filter(author=user)
    return render(request, 'users/profile.html', {
        'profile_user': user,
        'issues': issues,
    })


@login_required
def edit_profile(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=profile)
        if form.is_valid():
            profile = form.save(commit=False)
            # Update avatar manually
            avatar_choice = request.POST.get('avatar')
            if avatar_choice in [choice[0] for choice in AVATAR_CHOICES]:
                profile.avatar = avatar_choice
            profile.save()
            return redirect('profile', username=request.user.username)
    else:
        form = EditProfileForm(instance=profile)

    return render(request, 'users/edit_profile.html', {
        'form': form,
        'profile': profile,
        'avatars': AVATAR_CHOICES,
    })
