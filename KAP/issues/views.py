from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import IssueForm, CommentForm
from .models import Issue, Comment
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import user_passes_test

User = get_user_model()


@user_passes_test(lambda u: u.is_superuser)
def change_issue_status(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)
    if request.method == "POST":
        new_status = request.POST.get("status")
        if new_status in dict(Issue.STATUS_CHOICES):
            issue.status = new_status
            issue.save()
    return redirect("issue_detail", issue.id)


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
    profile = request.user.profile

    if not profile.can_post():
        return render(request, 'issues/no_tokens.html')

    if request.method == 'POST':
        form = IssueForm(request.POST)
        if form.is_valid():
            issue = form.save(commit=False)
            issue.author = request.user
            issue.save()
            profile.use_token()
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


@login_required
def comment_like_toggle(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.user in comment.likes.all():
        comment.likes.remove(request.user)
    else:
        comment.likes.add(request.user)

    # Redirect back to the referring page (list or detail)
    referer = request.META.get('HTTP_REFERER')
    if referer:
        return redirect(referer)
    return redirect('issue_detail', comment_id=comment.id)


@login_required
def issue_delete(request, issue_id):
    issue = get_object_or_404(Issue, id=issue_id)

    if request.user.id == issue.author.id:
        issue.delete()

    return redirect('home')


@login_required
def comment_delete(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)
    issue_id = comment.issue.id
    if request.user.id == comment.author.id:
        comment.delete()

    return redirect('issue', issue_id)
