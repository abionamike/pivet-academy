from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Post, Comment
from django.views.generic import ListView, DetailView
from django.core.mail import send_mail
from .forms import CommentForm
from django.shortcuts import get_object_or_404


def home(request):
	first_three = []
	for num in range(3):
		first_three.append(Post.objects.all()[num])

	context = {
		'posts': Post.objects.all(),
		'three': first_three,
	}

	if request.method == "POST":
		message_name = request.POST['message-name']
		message_email = request.POST['message-email'] 
		message = f"Hello,\nYou have a new message. Kindly find details below:\nEmail: {request.POST['message-email']}\nMessage: {request.POST['message-content']}"

		send_mail(
			message_name,
			message,
			message_email,
			['amabiona21@gmail.com'],
			fail_silently = False
		)

		context = {

				'posts': Post.objects.all(),
				'three': first_three,
				'message_name': message_name
			}

		return render(request, 'blog/home.html', context)

		

	return render(request, 'blog/home.html', context)



class PostListView(ListView):
	model = Post


class PostDetailView(DetailView):
	model = Post


def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            return redirect('news-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

	
@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('news-detail', pk=comment.post.pk)

@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('news-detail', pk=comment.post.pk)