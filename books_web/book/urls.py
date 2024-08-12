from django.urls import path
from .views import *
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('books/', BookList.as_view(), name='get_books'),
    path('books-create/', BookCreateView.as_view(), name='create-book'),
    path('recommendations/', RecommendationCreateView.as_view(), name='create-recommendation'),
    path('recommendations/list/', RecommendationListView.as_view(), name='list-recommendations'),
    path('recommendations/like/', LikeCreateView.as_view(), name='like-recommendation'),
    path('api-token-auth/', obtain_auth_token, name='api_token_auth')
]
