from django.views.generic import ListView, DetailView, CreateView
from django.shortcuts import get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from blog.models import Post, Comment, Author


class PostListView(ListView):
    model = Post
    paginate_by = 5


class PostDetailView(DetailView):
    model = Post


class CommentCreateView(LoginRequiredMixin, CreateView):
    model = Comment
    fields = ['content']

    def get_context_data(self, **kwargs):
        context = super(CommentCreateView, self).get_context_data(**kwargs)
        context['post'] = get_object_or_404(Post, pk=self.kwargs['pk'])
        return context

    def form_valid(self, form):
            form.instance.author = self.request.user
            form.instance.post = get_object_or_404(Post, pk=self.kwargs['pk'])
            return super(CommentCreateView, self).form_valid(form)


class AuthorListView(ListView):
    model = Author


class AuthorDetailView(DetailView):
    model = Author
