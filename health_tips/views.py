from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView, ListView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.checks import messages
from django.urls import reverse
from django.views.decorators.http import require_POST
from django.core.exceptions import PermissionDenied
from .forms import CommentForm, PostForm
from .models import Post, Comment
from django.contrib import messages

@login_required
def post_list(request):
    posts = Post.objects.order_by('-created_at')
    paginator = Paginator(posts, 5)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'health_tips/post_list.html', {'page_obj': page_obj})


# class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
#     try:
#         posts = paginator.page(page)
#     except PageNotAnInteger:
#         posts = paginator.page(1)
#     except EmptyPage:
#         posts = paginator.page(paginator.num_pages)
#
#     return render(request, 'health_tips/post_list.html', {'post_list': posts})
class PostCreate(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Post
    fields = ['post_title',  'post_content', 'head_image', 'file_upload', 'post_author']

    def test_func(self):
        return self.request.user.is_superuser or self.request.user.is_staff
    def form_valid(self, form):
        current_user = self.request.user
        if current_user.is_authenticated and (current_user.is_staff or current_user.is_superuser):
            form.instance.author = current_user
            return super(PostCreate, self).form_valid(form)
        else:
            return redirect('http://127.0.0.1:8000/health_tips/post/')
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=True)
            post.post_author = request.user
            post.save()
            return redirect('post_list')  # 작성 후 포스트 목록 페이지로 이동하도록 설정
    else:
        form = PostForm()

    return render(request, 'health_tips/post_form.html', {'form': form})
class PostUpdate(LoginRequiredMixin, UpdateView):
    model = Post
    fields = ['post_title',  'post_content', 'head_image', 'file_upload', 'post_author']
    template_name = 'health_tips/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().post_author:
            return super(PostUpdate, self).dispatch(request, *args, **kwargs)
        else:
            raise PermissionDenied

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return redirect('post_detail', pk=pk)
    else:
        form = CommentForm()

    post.increase_hits()

    # 좋아요 버튼 처리
    if request.method == 'POST' and request.user.is_authenticated:
        if 'like' in request.POST:
            if request.user not in post.likes.all():
                post.likes.add(request.user)
                post.save()
        elif 'unlike' in request.POST:
            if request.user in post.likes.all():
                post.likes.remove(request.user)
                post.save()

    is_liked = request.user in post.likes.all()
    return render(request, 'health_tips/post_detail.html', {'post': post, 'comments': comments, 'form': form, 'is_liked': is_liked})

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
        # POST 요청이 아니면 게시물 상세 페이지로 이동
        return redirect('post_detail', pk=pk)
    else:
        raise PermissionDenied


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


