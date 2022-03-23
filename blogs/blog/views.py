from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Post
from .forms import CommentForm


class PostList(generic.ListView):
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    # template_name = 'index.html'


# class PostDetail(generic.DetailView):
#     model = Post
#     # template = 'post_detail.html'


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    comments = post.comments.filter(active=True)
    new_comment = None

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():

            # create comment but don,t save to database yet
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            # save comment to the database
            new_comment.save()
    else:
        comment_form = CommentForm()
    
    context = {
        'post': post,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
    }
    
    return render(request, 'post_detail.html', context)