from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from forum.models import Category, Post, Comment


def ForumHome(request):
    data = {
        'categories': Category.objects.all()
    }
    return render(request, 'forum/forum_index.html', data)


def PostChangeStatus(status, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.status = status
    post.save()

def ForumPosts(request, pk):
    category = get_object_or_404(Category, pk=pk)
    adminposts = Post.objects.filter(category=category, author__is_superuser=True)
    if request.user.is_superuser:
        posts = Post.objects.filter(category=category)
    else:
        posts = Post.objects.filter(category=category, author=request.user)

    # Pagination işlemleri
    paginator = Paginator(posts, 10)  # Sayfa başına 10 öğe
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = {
        'adminposts': adminposts,
        'posts': page_obj,  # Pagination yapılmış gönderi listesi
        'categories': Category.objects.all(),
        'category': category,
        'postsGeneral': False,
        'users': User.objects.all(),
        'total_posts': paginator.count,  # Toplam gönderi sayısı
        'paginator': paginator,  # Paginator nesnesi
        'page_obj': page_obj,  # Sayfa nesnesi
    }
    return render(request, 'forum/forum_topics.html', data)


def ForumPostsGeneral(request):
    data = {
        'posts': Post.objects.all(),
        'categories': Category.objects.all(),
        'postsGeneral': True
    }
    return render(request,'forum/forum_topics.html', data)


def CreatePost(request):
    data = {
        'categories': Category.objects.all()
    }
    if request.user.is_authenticated:
        if request.method == 'POST':
            title = request.POST['title']
            content = request.POST['content']
            category_id = request.POST['category']
            category = get_object_or_404(Category, pk=category_id)
            post = Post(title=title, content=content, category=category,author=request.user)
            post.save()
            data={
                'message': True,
                'message_title':' Konu Oluşturuldu',
                'message_content': title + 'Başlıklı Konunuz Başarıyla Oluşturuldu'
            }
            return redirect('/forum/posts/'+category_id, data)

        return render(request,'forum/forum-createpost.html',data)
    return redirect('home')


def PostDetail(request, pk):
    post = Post.objects.get(id=pk)
    comments = Comment.objects.filter(post=pk)
    category = post.category
    data = {
        'post': post,
        'comments': comments,
        'category': category,
    }
    if request.method == "POST":
        post = Post.objects.get(id=pk)
        author = request.user
        content = request.POST['content']
        status = request.POST.get('status')
        createcomment = Comment.objects.create(post=post, author=author, content=content)
        PostChangeStatus(status, pk)
        createcomment.save()
        return redirect('post-detail', pk=pk)

    return render(request,'forum/forum-single.html', data)

