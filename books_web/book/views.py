from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .fetch_data import fetch_books
from .serializers import BookSerializer
from rest_framework.generics import ListCreateAPIView, CreateAPIView, ListAPIView
from rest_framework.permissions import *
from .models import *
from .serializers import *
from rest_framework.permissions import IsAuthenticated


class BookList(APIView):
    def get(self, request):
        keyword = request.query_params.get('keyword', '')
        authors = request.query_params.getlist('author', '')
        category = request.query_params.get('category', '')
        filter_type = request.query_params.get('filter', '')

        query_params = {}
        if keyword:
            query_params['q'] = keyword
        if authors:
            if 'q' in query_params:
                query_params['q'] += ' ' + ','.join([f'inauthor:{author}' for author in authors])
            else:
                query_params['q'] = ','.join([f'inauthor:{author}' for author in authors])
        if category:
            if 'q' in query_params:
                query_params['q'] += f' subject:{category}'
            else:
                query_params['q'] = f'subject:{category}'
        if filter_type:
            query_params['filter'] = filter_type
        books_data = fetch_books(query_params)
        if "error" in books_data:
            return Response({"error": books_data["error"]}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
        books = books_data.get('items', [])
        serialized_books = []
        try:
            for book in books:
                volume_info = book.get('volumeInfo', {})
                image_links = volume_info.get('imageLinks', {})
                cover_image = image_links.get('thumbnail') or image_links.get('smallThumbnail')

                data = {
                    "title": volume_info.get("title"),
                    "subtitle": volume_info.get("subtitle"),
                    "authors": volume_info.get("authors"),
                    "publisher": volume_info.get("publisher"),
                    "published_date": volume_info.get("publishedDate"),
                    "description": volume_info.get("description"),
                    "cover_image": cover_image,
                    "average_rating": volume_info.get("averageRating"),
                    "ratings_count": volume_info.get("ratingsCount"),
                }
                serialized_books.append(BookSerializer(data).data)
            return Response(serialized_books, status=status.HTTP_200_OK)
        except:
            return Response({"errors" : "There might be an internal server error"}, status=status.HTTP_400_BAD_REQUEST)



class BookCreateView(ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class RecommendationCreateView(CreateAPIView):
    queryset = Recommendation.objects.all()
    serializer_class = RecommendationSerializer


    def perform_create(self, serializer):
        print(self.request.data)
        print(self.request.user.username)
        serializer.save(user=self.request.user.username)

class RecommendationListView(ListAPIView):
    serializer_class = RecommendationSerializer

    def get_queryset(self):
        queryset = Recommendation.objects.all()

        genre = self.request.query_params.get('genre', None)
        rating = self.request.query_params.get('rating', None)
        pub_date = self.request.query_params.get('pub_date', None)

        if genre:
            queryset = queryset.filter(book__genre__icontains=genre)
        if rating:
            queryset = queryset.filter(book__average_rating__gte=rating)
        if pub_date:
            queryset = queryset.filter(book__published_date__year=pub_date)

        sort_by = self.request.query_params.get('sort_by', 'created_at')
        queryset = queryset.order_by(sort_by)

        return queryset

class LikeCreateView(CreateAPIView):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer


    def perform_create(self, serializer):
        serializer.save(user=self.request.user)