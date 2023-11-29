from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.core.exceptions import PermissionDenied

from .forms import CommentForm
from .models import Post, Comment


def post_list(request):
    posts = Post.objects.all().order_by('-created_at')

    posts_per_page = 5
    paginator = Paginator(posts, posts_per_page)

    page = request.GET.get('page')

    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)
    except EmptyPage:
        posts = paginator.page(paginator.num_pages)

    return render(request, 'health_tips/post_list.html', {'post_list': posts})
class PostCreate(LoginRequiredMixin,UserPassesTestMixin,CreateView):
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

class PostUpdate(LoginRequiredMixin,UpdateView):
    model = Post
    fields = ['post_title',  'post_content', 'head_image', 'file_upload', 'post_author']
    template_name = 'health_tips/post_update_form.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and request.user == self.get_object().author:
            return super(PostUpdate,self).dispatch(request, *args,**kwargs)
        else:
            raise PermissionDenied
def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = Comment.objects.filter(post=post)

    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.user = request.user
            comment.save()

            return redirect('post_detail', post_id=post_id)
    else:
        form = CommentForm()

    post.increase_hits()  # 조회수 증가

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

class PostDetail(DetailView):
    model = Post

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user = None
        self.POST = None
        self.method = None

    def get_context_data(self, **kwargs):
        context = super(PostDetail, self).get_context_data()
        context['no_category_post_count'] = Post.objects.filter(category=None).count()
        context['comment_form'] = CommentForm
        return context

    def new_comment(request, pk):
        if request.user.is_authenticated:
            post = get_object_or_404(Post, pk=pk)

            if request.method == "POST":
                comment_form = CommentForm(request.POST)
                if comment_form.is_valid():
                    comment = comment_form.save(commit=False)
                    comment.post = post
                    comment.author = request.user
                    comment.save()
                    return redirect(comment.get_absolute_url())
            else:
                return redirect(post.get_absolute_url())

        else:
            raise PermissionError
