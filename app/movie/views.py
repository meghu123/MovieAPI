from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

from .models import Movies
from .serializers import MoviesSerializer
from rest_framework import generics
from .forms import SignupForm
from django.shortcuts import render, redirect
from django.template import RequestContext
from rest_framework import mixins
from rest_framework import generics
from .forms import GenreDataForm, MoviesDataForm
from django.shortcuts import render
import django_filters


class MoviesList(mixins.ListModelMixin,
                 mixins.CreateModelMixin,
                 generics.GenericAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        if request.user.role == 1:
            return self.create(request, *args, **kwargs)


class MoviesDetail(mixins.RetrieveModelMixin,
                   mixins.UpdateModelMixin,
                   mixins.DestroyModelMixin,
                   generics.GenericAPIView):
    queryset = Movies.objects.all()
    serializer_class = MoviesSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        if request.user.role == 1:
            return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        if request.user.role == 1:
            return self.destroy(request, *args, **kwargs)


class MovieFilter(django_filters.FilterSet):
    class Meta:
        model = Movies
        fields = ('popularity', 'director', 'genre', 'name', 'imdb_score')


class RateFilter(django_filters.FilterSet):
    class Meta:
        model = Movies
        fields = {'imdb_score': ['lt', 'gt'], }


def movie_list(request):
    f = RateFilter(request.GET, queryset=Movies.objects.all())
    return render(request,'template.html', {'filter': f})


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                first_name=form.cleaned_data['first_name'],
                last_name=form.cleaned_data['last_name'],
                email=form.cleaned_data['email'],
                role=form.cleaned_data['role'],
                password=form.cleaned_data['password'],
            )
            return HttpResponseRedirect('/registered/')
    else:
        form = SignupForm()
    return render(request, 'signup.html', {'form': form})


def add_movie(request):
    if request.method == "POST":
        if request.user.role == '1':
            form = MoviesDataForm(request.POST)
            if form.is_valid():
                # commit=False means the form doesn't save at this time.
                # commit defaults to True which means it normally saves.
                form.save()

            return redirect('/movie/')
    else:
        form = MoviesDataForm()

    return render(request,"movie_post.html", {'form': form})


def add_genre(request):
    if request.method == "POST":
        if request.user.role == '1':
            form = GenreDataForm(request.POST)

            if form.is_valid():
                # commit=False means the form doesn't save at this time.
                # commit defaults to True which means it normally saves.
                form.save()

            return redirect('/movie/')
    else:
        form = GenreDataForm()

    return render(request,"genre_post.html", {'form': form})