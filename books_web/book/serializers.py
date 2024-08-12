from rest_framework import serializers

# class BookSerializer(serializers.Serializer):
#     id = serializers.CharField(max_length=50)
#     title = serializers.CharField(max_length=255)
#     subtitle = serializers.CharField(max_length=255, required=False)
#     authors = serializers.ListField(child=serializers.CharField(max_length=100), required=False)
#     publisher = serializers.CharField(max_length=255, required=False)
#     published_date = serializers.CharField(max_length=10, required=False)
#     description = serializers.CharField(required=False)
#     cover_image = serializers.URLField(required=False)
#     average_rating = serializers.FloatField(required=False, allow_null=True)
#     ratings_count = serializers.IntegerField(required=False, allow_null=True)


from rest_framework import serializers
from .models import Book, Recommendation, Like

class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'

class RecommendationSerializer(serializers.ModelSerializer):
    book = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all())
    book_details = BookSerializer(read_only=True)
    likes_count = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Recommendation
        fields = ['book','book_details', 'user', 'comment', 'created_at', 'likes_count']

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'
