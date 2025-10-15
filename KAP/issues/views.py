from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required

from .forms import IssueForm, CommentForm
from .models import Issue, Comment

# Signup view


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})

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
    return render(request, 'registration/login.html', {'form': form})


@login_required
def issue_list(request):
    # Order by number of likes descending, then newest first
    issues = sorted(
        Issue.objects.all(),
        key=lambda i: i.total_likes,
        reverse=True
    )
    return render(request, 'issues/issue_list.html', {'issues': issues})


@login_required
def issue_detail(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.issue = issue
            comment.save()
            return redirect('issue_detail', issue_id=issue.id)
    else:
        form = CommentForm()

    return render(request, 'issues/issue_detail.html', {
        'issue': issue,
        'comment_form': form
    })


@login_required
def add_comment(request, issue_id):
    if not request.user.is_authenticated:
        return redirect('login')

    issue = get_object_or_404(Issue, id=issue_id)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.author = request.user
            comment.issue = issue
            comment.save()
            return redirect('issue_detail', issue_id=issue.id)
    else:
        form = CommentForm()

    return render(request, 'issues/issue_detail.html', {
        'issue': issue,
        'comment_form': form
    })


@login_required
def create_issue(request):
    if not request.user.is_authenticated:
        return redirect('login')
    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.author = request.user
            issue.save()
            return redirect('home')
    else:
        form = IssueForm()
    return render(request, 'issues/issue_create.html', {'form': form})


@login_required
def issue_like_toggle(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.user in issue.likes.all():
        issue.likes.remove(request.user)
    else:
        issue.likes.add(request.user)

    # Redirect back to the referring page (list or detail)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('issue_detail', issue_id=issue.id)
