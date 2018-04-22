from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^books$', views.books),
    url(r'^books/(?P<book_id>\d+)$', views.book_page),
    url(r'^books/post_review$', views.post_review),
    url(r'^books/post_review_new$', views.post_review_new),
    url(r'^books/add_page$', views.add_page),
    url(r'^submit$', views.submit),
    url(r'^login$', views.login),
    url(r'^logout$', views.logout),
    url(r'^users/(?P<user_id>\d+)$', views.user_page),
]