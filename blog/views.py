from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Post, Comment

# Liste de tous les posts
def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/post_list.html', {'posts': posts})

# Détail d'un post
def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.comments.all()
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

# Créer un post
@login_required
def post_create(request):
    if request.method == 'POST':
        title   = request.POST['title']
        content = request.POST['content']
        Post.objects.create(title=title, content=content, author=request.user)
        messages.success(request, 'Article créé avec succès !')
        return redirect('post_list')
    return render(request, 'blog/post_form.html', {'action': 'Créer'})

# Modifier un post
@login_required
def post_update(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, "Vous n'êtes pas autorisé à modifier cet article.")
        return redirect('post_list')
    if request.method == 'POST':
        post.title   = request.POST['title']
        post.content = request.POST['content']
        post.save()
        messages.success(request, 'Article modifié avec succès !')
        return redirect('post_detail', pk=post.pk)
    return render(request, 'blog/post_form.html', {'action': 'Modifier', 'post': post})

# Supprimer un post
@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        messages.error(request, "Vous n'êtes pas autorisé à supprimer cet article.")
        return redirect('post_list')
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Article supprimé.')
        return redirect('post_list')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})
