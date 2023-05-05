from django.shortcuts import render
from django.views.generic import TemplateView, ListView, DetailView, CreateView, UpdateView
from .models import Post, Comment
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required


class AboutView(TemplateView):
    template_name = 'about.html'


class PostListView(ListView):
    model = Post

    def get_queryset(self):
        current_time = timezone.now()
        # data publikacji jest wcześniejsza lub równa bieżącemu czasowi
        queryset = Post.objects.filter(published_date__lte=current_time)
        ordered_queryset = queryset.order_by('-published_date')
        return ordered_queryset


class PostDetailView(DetailView):
    model = Post


class CreatePostView(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostUpdateView(LoginRequiredMixin, UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post


class PostDeleteView(LoginRequiredMixin, DetailView):
    model = Post
    success_url = reverse_lazy('post_lazy')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    model = Post

    def get_queryset(self):
        queryset = Post.objects.filter(published_date__isnull=True)
        ordered_queryset = queryset.order_by('created_date')
        return ordered_queryset
