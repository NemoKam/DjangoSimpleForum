from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, JsonResponse

from profileapp.models import ProfileUser, Post, Comment
from profileapp.forms import UserProfileRegisterForm, PostCreateForm, CommentCreateForm


@login_required
def profile_create(request):
    if request.method == 'GET':
        profile_reg_form = UserProfileRegisterForm()
        data = {
            'page_title': 'Profile Create',
            'profile_reg_form': profile_reg_form
        }
        return render(request, 'profileapp/profile_create.html', data)
    else:
        profile_reg_form = UserProfileRegisterForm(request.POST, request.FILES)
        if profile_reg_form.is_valid():
            profile_reg_form.save(request.user.id)
            return redirect('profileapp:profile')
        else:
            return JsonResponse({'status': False, 'error_message': f'Invalid form: {profile_reg_form.errors}'})

@login_required
def profile_edit(request):
    profile = ProfileUser.objects.get(forumuser_ptr_id=request.user.id)
    return HttpResponse('2')
    # not finished

@login_required
def user_profile(request):
    profile = request.user
    wanted_friends_cnt = ProfileUser.objects.filter(pre_friends__in=ProfileUser.objects.filter(id=request.user.id)).count()
    posts_create_form = PostCreateForm()
    comments_create_form = CommentCreateForm()
    posts = Post.objects.filter(author=request.user)
    data = {
        'page_title': 'Profile',
        'user_model': profile,
        'wanted_friends_cnt': wanted_friends_cnt,
        'posts_create_form': posts_create_form,
        'comments_create_form': comments_create_form,
        'posts': posts
    }
    return render(request, 'profileapp/profile.html', data)

def user_other_profile(request, username):
    profile = ProfileUser.objects.get(username=username)
    friends = profile.friends
    data = {
        'page_title': f'Profile {profile.username}',
        'user_model': profile,
        'friends': friends
    }
    return render(request, 'profileapp/profile.html', data)
    # not finished

@login_required
def friends_search(request, username):
    friends_ids = [friend.id for friend in ProfileUser.objects.get(id=request.user.id).friends.all()]
    pre_friends = ProfileUser.objects.filter(username__icontains=username, is_active=True).exclude(username=request.user.username).exclude(id__in=friends_ids)[:10]
    pre_friends_info = [{"username": pre_friend.username, "first_name": pre_friend.first_name, "last_name": pre_friend.last_name, "avatar_url": pre_friend.avatar.url} for pre_friend in pre_friends]
    return JsonResponse({'status': True, 'users': pre_friends_info})

@login_required
def friends_get(request):
    friends = [{"username": friend.username, "first_name": friend.first_name, "last_name": friend.last_name, "avatar_url": friend.avatar.url} for friend in ProfileUser.objects.get(id=request.user.id).friends.all()]
    return JsonResponse({'status': True, 'users': friends})

@login_required
def friends_requested(request):
    wanted_friends = [{"username": friend.username, "first_name": friend.first_name, "last_name": friend.last_name, "avatar_url": friend.avatar.url} for friend in ProfileUser.objects.filter(pre_friends__in=ProfileUser.objects.filter(id=request.user.id))]
    return JsonResponse({'status': True, 'users': wanted_friends})

@login_required
def friends_delete(request, username):
    past_friend = ProfileUser.objects.filter(username=username)[0]
    if past_friend:
        past_friend.pre_friends.remove(request.user)
        request.user.friends.remove(past_friend)
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error_message': "User doesn't found"})
    
@login_required
def friends_add(request, username):
    maybe_friend = ProfileUser.objects.filter(username=username)
    user_id = request.user.id
    if maybe_friend.first():
        user = maybe_friend[0].pre_friends.filter(id=user_id)
        if user.first():
            maybe_friend[0].pre_friends.remove(request.user)
            maybe_friend[0].friends.add(request.user)
            return JsonResponse({'status': True})
        else:
            maybe_in_friends = maybe_friend[0].friends.filter(id=user_id)
            if maybe_in_friends.first():
                return JsonResponse({'status': False, 'error_message': 'You already friends'})
            else:
                if request.user.pre_friends.filter(id=maybe_friend[0].id).first(): # type: ignore
                    return JsonResponse({'status': False, 'error_message': 'You already send'})
                else:
                    request.user.pre_friends.add(maybe_friend[0])
                    return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False, 'error_message': "User doesn't found "})
    
@login_required
def posts_create(request):
    if request.method == 'POST':
        posts_create_form = PostCreateForm(request.POST, request.FILES)
        if posts_create_form.is_valid():
            new_post = posts_create_form.save(request.user, None)
            data = {
                'author': {
                    'username': new_post.author.username,
                    'first_name': new_post.author.first_name,
                    'last_name': new_post.author.last_name,
                    'avatar': new_post.author.avatar.url
                },
                'text': new_post.text,
                'img': new_post.img.url if new_post.img else '',
                'created_at': new_post.created_at,
                'post_id': new_post.id, # type: ignore
            }
            return JsonResponse({'status': True, 'data': data})
        return JsonResponse({'status': False, 'error_message': 'Invalid form'})
    return JsonResponse({'status': False, 'error_message': 'Incorrect request method'})

@login_required
def posts_like(request, post_id):
    post = Post.objects.filter(id=post_id)
    if post.first():
        if post[0].likes.filter(id=request.user.id).first():
            post[0].likes.remove(request.user)
            is_liked = False
        else:
            post[0].likes.add(request.user)
            is_liked = True
        data = {
            'likes': post[0].likes.count(),
            'comments_cnt': post[0].comments.count(),
            'is_liked': is_liked
        }
        return JsonResponse({'status': True, 'data': data})
    else:
        return JsonResponse({'status': False, 'error_message': 'Invalid post id'})

@login_required
def posts_warn(request, post_id):
    post = Post.objects.filter(id=post_id)
    if post.first():
        if post[0].warned.filter(id=request.user.id).first():
            return JsonResponse({'status': False, 'error_message': 'Already warned'})
        else:
            post[0].warned.add(request.user)
            data = {
                'likes': post[0].likes.count(),
                'comments_cnt': post[0].comments.count()
            }
            return JsonResponse({'status': True, 'data': data})
    else:
        return JsonResponse({'status': False, 'error_message': 'Invalid post id'})
    
@login_required
def posts_delete(request, post_id):
    post = Post.objects.filter(id=post_id, author=request.user)
    if post.first():
        post[0].delete()
        return JsonResponse({'status': True})
    else:
        return JsonResponse({'status': False})
    
@login_required
def posts_edit(request, post_id):
    post = Post.objects.filter(id=post_id, author=request.user)
    if post.first():
        post_edit_form = PostCreateForm(request.POST, request.FILES)
        if post_edit_form.is_valid():
            post = post_edit_form.save(request.user, post_id)
            data = {
                'post_id': post.id,
                'text': post.text,
                'img': post.img.url if post.img else ''
            }
            return JsonResponse({'status': True, 'data': data})
        else:
            return JsonResponse({'status': False})
    else:
        return JsonResponse({'status': False})

@login_required
def posts_comments(request, post_id):
    post = Post.objects.filter(id=post_id)
    if post.first():
        all_comments = [{'id': comment.id, 'text': comment.text, 'img_url': comment.img.url, 'created_at': comment.created_at, 'likes': comment.likes.count(), 'author_username': comment.author.username, 'author_first_name': comment.author.first_name, 'author_last_name': comment.author.last_name, 'author_avatar_url': comment.author.avatar.url, 'post_id': post_id} if comment.img else {'id': comment.id, 'text': comment.text, 'created_at': comment.created_at, 'likes': comment.likes.count(), 'author_username': comment.author.username, 'author_first_name': comment.author.first_name, 'author_last_name': comment.author.last_name, 'author_avatar_url': comment.author.avatar.url, 'post_id': post_id} for comment in post[0].comments.all()]
        data = {
            'likes': post[0].likes.count(),
            'comments_cnt': post[0].comments.count(),
            'comments': all_comments
        }
        return JsonResponse({'status': True, 'data': data})
    else:
        return JsonResponse({'status': False, 'error_message': 'Invalid post id'})
    
@login_required
def posts_comments_create(request, post_id):
    post = Post.objects.filter(id=post_id)
    if post.first():
        form = CommentCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save(post_id, request.user)
            all_comments = [{'id': comment.id, 'text': comment.text, 'img_url': comment.img.url, 'created_at': comment.created_at, 'likes': comment.likes.count(), 'author_username': comment.author.username, 'author_first_name': comment.author.first_name, 'author_last_name': comment.author.last_name, 'author_avatar_url': comment.author.avatar.url, 'post_id': post_id} if comment.img else {'id': comment.id, 'text': comment.text, 'created_at': comment.created_at, 'likes': comment.likes.count(), 'author_username': comment.author.username, 'author_first_name': comment.author.first_name, 'author_last_name': comment.author.last_name, 'author_avatar_url': comment.author.avatar.url, 'post_id': post_id} for comment in post[0].comments.all()]
            data = {
                'post_id': post_id,
                'comments_cnt': post[0].comments.count(),
                'comments': all_comments
            }
            return JsonResponse({'status': True, 'data': data})
        else:
            return JsonResponse({'status': False, 'error_message': 'Invalid form'})
    else:
        return JsonResponse({'status': False, 'error_message': 'Invalid post id'})

@login_required
def posts_comments_like(request, post_id, comment_id):
    comment = Comment.objects.filter(id=comment_id)
    if comment.first():
        if comment[0].likes.filter(id=request.user.id).first():
            comment[0].likes.remove(request.user)
            is_liked = False
        else:
            comment[0].likes.add(request.user)
            is_liked = True
        data = {
            'is_liked': is_liked,
            'likes': comment[0].likes.count()
        }
        return JsonResponse({'status': True, 'data': data})
    else:
        return JsonResponse({'status': False, 'error_message': 'Invalid comment id'})
    
@login_required
def posts_comments_warn(request, post_id, comment_id):
    comment = Comment.objects.filter(id=comment_id)
    if comment.first():
        if comment[0].warned.filter(id=request.user.id).first():
            return JsonResponse({'status': False, 'error_message': 'You already warned this comment'})
        else:
            comment[0].warned.add(request.user)
        data = {
            'likes': comment[0].likes.count()
        }
        return JsonResponse({'status': True, 'data': data})
    else:
        return JsonResponse({'status': False, 'error_message': 'Invalid comment id'})