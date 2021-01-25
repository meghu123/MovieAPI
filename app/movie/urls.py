from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from .views import MoviesList,MoviesDetail,signup,add_movie,add_genre,movie_list

urlpatterns = [
    url(r'^movie/$', MoviesList.as_view()),
    url(r'^movie/(?P<pk>[0-9]+)/$', MoviesDetail.as_view()),
    url(r'^$', signup),
    url(r'^add_movie', add_movie),
    url(r'^add_genre', add_genre),
    url(r'^list$', movie_list),
]

urlpatterns = format_suffix_patterns(urlpatterns)