from rest_framework import serializers
import films.models as film_models

class FilmGetSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)
    film_type = serializers.StringRelatedField()

    class Meta:
        model = film_models.Film
        fields = ["title", "genre", "film_type", "visualizations", "rating", "slug"]