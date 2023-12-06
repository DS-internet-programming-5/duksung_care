from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.checks import messages
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .forms import CommentForm
from .models import Post, Comment
from django.contrib import messages
from django.http import JsonResponse

# 게시글 목록
@login_required
def post_list(request):
    posts = Post.objects.order_by('-created_at')
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'health_tips/post_list.html', {'page_obj': page_obj})

# 게시글 상세
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.comment_content = CommentForm(request.POST)
            comment.save()

            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    post.increase_hits()

    return render(request, 'health_tips/post_detail.html', {'post': post, 'comments': comments, 'form': form})

# 좋아요 기능
def likes_post(request, pk):
    if request.method == 'POST' and request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)
        user = request.user

        if user in post.likes.all():
            post.likes.remove(user)
            liked = False
        else:
            post.likes.add(user)
            liked = True

        post.save()

        return JsonResponse({'liked': liked, 'count_likes': post.likes.count()})

    return JsonResponse({}, status=400)

# 게시글 작성
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['post_title', 'post_content', 'head_image','is_banner']
    template_name = 'health_tips/post_form.html'

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            post = form.save(commit=False)
            post.post_author = current_user

            if 'head_image' not in self.request.FILES:
                post.head_image = None

            post.save()
            return redirect('/health_tips/post/')
        else:
            return redirect('/health_tips/post/')

# 게시글 수정
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['post_title', 'post_content', 'head_image', 'file_upload', 'is_banner']
    template_name = 'health_tips/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().post_author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

# 댓글 작성
def new_comment(request, pk):
    if request.user.is_authenticated:
        post = get_object_or_404(Post, pk=pk)

        if request.method == "POST":
            comment_form = CommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.post = post
                comment.user = request.user
                comment.save()
                return redirect('post_detail', pk=pk)
        return redirect('post_detail', pk=pk)
    else:
        raise PermissionDenied

# 댓글 삭제
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    post = comment.post

    if request.user == comment.user:
        comment.delete()
        messages.add_message(request, messages.SUCCESS, '댓글이 성공적으로 삭제되었습니다.')
    else:
        messages.add_message(request, messages.ERROR, '댓글을 삭제할 권한이 없습니다.')

    return redirect(post.get_absolute_url())

# 댓글 수정
class CommentUpdate(LoginRequiredMixin, UpdateView):
    model = Comment
    form_class = CommentForm

    def get_success_url(self):
        return reverse('post_detail', kwargs={'pk': self.get_object().post.pk})

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().user:
            return super(CommentUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied


