from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView, DetailView
from .models import Post
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from .forms import PostForm, CommentForm


class BlogListView(View):
    def get(self, request):
        blogs = Post.objects.all().order_by('-id')
        context = {
            'blogs': blogs
        }
        return render(request, 'home.html', context=context)


class BlogCreateView(LoginRequiredMixin, View):
    def get(self, request):
        create_form = PostForm()
        context = {
            'form': create_form
        }
        return render(request, 'post_create.html', context=context)

    def post(self, request):
        create_form = PostForm(request.POST, request.FILES)
        if create_form.is_valid():
            new_post = create_form.save(commit=False)
            new_post.author = request.user
            new_post.save()
            return redirect('blogs:home')
        else:
            context = {
                'form': create_form
            }
            return render(request, 'post_create.html', context=context)


class BlogUpdateView(LoginRequiredMixin, UserPassesTestMixin, View):
    def get_object(self):
        pk = self.kwargs.get("pk")
        return get_object_or_404(Post, pk=pk)

    def get(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        update_form = PostForm(instance=post)
        context = {
            'form': update_form
        }
        return render(request, 'update.html', context=context)

    def post(self, request, pk):
        post = get_object_or_404(Post, pk=pk)
        update_form = PostForm(request.POST, request.FILES, instance=post)
        if update_form.is_valid():
            update_form.save()
            return redirect('blogs:home')
        else:
            context = {
                'form': update_form
            }
            return render(request, 'update.html', context=context)

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user


class BlogDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post
    template_name = 'post_delete.html'
    success_url = reverse_lazy('blogs:home')

    def test_func(self):
        blog = self.get_object()
        return blog.author == self.request.user


class BlogDetailView(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'blog_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = CommentForm()
        return context

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.blog = self.object
            comment.author = request.user
            comment.save()
            return self.get(request, *args, **kwargs)
        context['form'] = form
        return self.render_to_response(context)


class BlogSortMyBlogsView(LoginRequiredMixin, View):
    template_name = 'my_blogs.html'

    def get(self, request, *args, **kwargs):
        my_blogs = Post.objects.filter(author=request.user)
        context = {
            'my_blogs': my_blogs,
            'title': 'My Blogs',
        }
        return render(request, self.template_name, context=context)