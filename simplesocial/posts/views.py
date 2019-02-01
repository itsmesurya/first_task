from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin

from django.urls import reverse_lazy,reverse
from django.http import Http404
from django.views import generic
from django.views.generic import UpdateView
# from django.utils import timezone as tz

from braces.views import SelectRelatedMixin

from . import forms
from . import models

from django.contrib.auth import get_user_model
User = get_user_model()


class PostList(generic.ListView):
    model = models.Post
    # select_related = ("user", "message","group","dead_line")


class UserPosts(generic.ListView):
    model = models.Post
    template_name = "posts/user_post_list.html"

    def get_queryset(self):
        try:
            self.post_user = User.objects.prefetch_related("posts").get(
                username__iexact=self.kwargs.get("username")
            )
        except User.DoesNotExist:
            raise Http404
        else:
            return self.post_user.posts.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["post_user"] = self.post_user
        return context

    # def get_context_data(self, **kwargs):
    #     ctx = super().get_context_data(**kwargs)
    #
    #     now = tz.now()
    #     ctx['now'] = now
    #     ctx['today'] = tz.localtime(now).date()
    #
    #     return ctx


class PostDetail(SelectRelatedMixin, generic.DetailView):
    model = models.Post
    select_related = ("user", "group")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(
            user__username__iexact=self.kwargs.get("username")
        )


class CreatePost(LoginRequiredMixin, SelectRelatedMixin, generic.CreateView):
    # form_class = forms.PostForm
    fields = ('message','group','dead_line')
    model = models.Post


    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


class DeletePost(LoginRequiredMixin, SelectRelatedMixin, generic.DeleteView):
    model = models.Post
    select_related = ("user", "group")
    success_url = reverse_lazy("posts:all")

    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "task Deleted")
        return super().delete(*args, **kwargs)

class EditPost(LoginRequiredMixin, UpdateView):
    model=models.Post
    fields = "__all__"

    success_url = reverse_lazy("posts:all")
    template_name = "posts/post_edit.html"

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.user = self.request.user
        self.object.save()
        return super().form_valid(form)


    def get_queryset(self):
        queryset = super().get_queryset()
        return queryset.filter(user_id=self.request.user.id)


    def edit(self,*args,**kwargs):
        messages.success(self.request, "task edited")
        return super().edit(*args, **kwargs)

# class EditPost(UpdateView):
#     model=models.Post
#     fields = "__all__"
#     template_name = "posts/post_edit.html"
#
#     def get_success_url(self, *args, **kwargs):
#         return reverse("some url name")
