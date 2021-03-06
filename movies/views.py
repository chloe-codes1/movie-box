from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.views.decorators.http import require_POST
from django.db.models import Count, Prefetch
from .models import Movie, Genre, Comment
from .forms import CommentForm
from accounts.models import UserProfile
from django.core.paginator import Paginator
from django.conf import settings
from django.http import JsonResponse
from django.db.models import FilteredRelation, Q

import requests
import random

# main page - 영화 전체 목록
# def home(request):
#     movies = Movie.objects.order_by('-release_date')[:8]
#     movies1 = movies[:4]
#     movies2 = movies[4:]
#     if request.user.is_authenticated:
#         try:
#             profile = UserProfile.objects.get(user=request.user)
#             recommand_movies = list(Movie.objects.filter(genres__in=profile.favorites))
            
#         except UserProfile.DoesNotExist:
#             profile = None
#             recommand_movies = list(Movie.objects.all())
#         recommand_movies = random.sample(recommand_movies, 10)
#         context = {
#                 'recommand_movies': recommand_movies,
#                 'movies1': movies1,
#                 'movies2': movies2,
#             }
#         return render(request, 'movies/home.html', context)
#     context = {
#             'movies1': movies1,
#             'movies2': movies2,
#         }
#     return render(request, 'movies/home.html', context)
    
User = get_user_model()

def home(request):
    movies = Movie.objects.order_by('-release_date')[:8]
    movies1 = movies[:4]
    movies2 = movies[4:]
    if request.user.is_authenticated:
        try:
            user = get_object_or_404(User, id=request.user.id)
            recommend_movies = list(Movie.objects.filter(genres__name__icontains=user.favorite))
            if len(recommend_movies) < 12:
                recommend_movies += random.sample(list(Movie.objects.all()), 12-len(recommend_movies))
        except UserProfile.DoesNotExist:
            profile = None
            recommend_movies = list(Movie.objects.all())
        recommend_movies = random.sample(recommend_movies, 12)
        context = {
                'recommend_movies': recommend_movies,
                'movies1': movies1,
                'movies2': movies2,
            }
        return render(request, 'movies/home.html', context)
    context = {
            'movies1': movies1,
            'movies2': movies2,
        }
    return render(request, 'movies/home.html', context)

# 전체 영화들 보기
def movie_list(request):
    movies = Movie.objects.order_by('-vote_average')
    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,

    }
    return render(request, 'movies/movie_list.html', context)

def sort(request):
    option = request.GET.get('option')
    if option == 'Top rating':
        movies = Movie.objects.order_by('-vote_average')
    elif option == 'Latest':
        movies = Movie.objects.order_by('-release_date')
    elif option == 'Oldest':
        movies = Movie.objects.order_by('release_date')
    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'option': option,
    }
    return render(request, 'movies/movie_list.html', context)


def genre(request):
    option = request.GET.get('option')
    movies = Movie.objects.filter(genres__name__icontains=option)
    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'option': option,
    }
    return render(request, 'movies/movie_list.html', context)


@login_required
def like(request, movie_pk):
    user = request.user 
    movie = get_object_or_404(Movie, pk=movie_pk)
    
    if movie.liked_users.filter(pk=user.pk).exists():
        movie.liked_users.remove(user)
        liked = False
    else:
        movie.liked_users.add(user)
        liked = True

    context = {
        'liked': liked,
        'count': movie.liked_users.count(),
    }

    return JsonResponse(context)  

# 영화별 상세보기 - 해당 영화 리뷰출력
def movie_detail(request, movie_pk):
    movie = get_object_or_404(Movie, id=movie_pk)
    form = CommentForm()
    context = {
        'movie': movie,
        'form':form,
    }
    return render(request, 'movies/movie_detail.html', context)

def search(request):
    option = request.GET.get('option')
    keyword = request.GET.get('keyword')

    if option == 'All':
        movies = Movie.objects.filter(
            Q(title__icontains=keyword) | Q(overview__icontains=keyword)
            )
        option = 'titles and content'
    elif option == 'Title':
        movies = Movie.objects.filter(title__icontains=keyword)
    elif option == 'Content':
        movies = Movie.objects.filter(overview__icontains=keyword)

    paginator = Paginator(movies, 8)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'page_obj': page_obj,
        'keyword': keyword,
        'option': option.lower(),
    }
    return render(request, 'movies/movie_list.html', context)


# 댓글 작성 - 영화에 대한 댓글 입력
@login_required
@require_POST
def comment_create(request, movie_pk):
    movie = get_object_or_404(Movie, pk=movie_pk)
    form = CommentForm(request.POST)
    if form.is_valid():
        comment = form.save(commit=False)
        comment.movie = movie
        comment.user = request.user
        comment.save()
    return redirect('movies:movie_detail', movie.pk)


# 댓글 삭제 - 댓글 작성자일떄만 삭제
@login_required
@require_POST
def comment_delete(request, movie_pk):
    comment_pk = request.POST.get('comment_id')
    comment = get_object_or_404(Comment, pk=comment_pk)
    if request.user == comment.user:
        comment.delete()
    return redirect('movies:movie_detail', movie_pk)