from rest_framework import serializers
import films.models as film_models

class FilmGetSerializer(serializers.ModelSerializer):
    genre = serializers.StringRelatedField(many=True)
    film_type = serializers.StringRelatedField()

    class Meta:
        model = film_models.Film
        fields = ["pk", "title", "genre", "film_type", "visualizations", "rating", "slug"]


class FilmVisualizationSerializer(serializers.ModelSerializer):

    class Meta:
        model = film_models.UserFilmVisualization
        fields = ["film", "user"]

    def validate(self, attrs):
        film_id = attrs.get("film")
        user_id = attrs.get("user")

        if film_id and user_id:
            
            films = film_models.UserFilmVisualization.objects.filter(film=film_id, user=user_id)
            if films.exists():
                raise serializers.ValidationError("You already visualized this film")
            else:
                return attrs
        else:
            raise serializers.ValidationError("Film and user are required")
        

class FilmRatingSerializer(serializers.ModelSerializer):

    class Meta:
        model = film_models.UserFilmRating
        fields = ["film", "user", "rating"]

    def validate(self, attrs):
        film_id = attrs.get("film")
        user_id = attrs.get("user")
        rating = attrs.get("rating")

        if film_id and user_id and rating:
            if rating > 10 or rating < 0:
                raise serializers.ValidationError("Rating must be between 0 and 10")
            else:
                films = film_models.UserFilmRating.objects.filter(film=film_id, user=user_id)
                if films.exists():
                    raise serializers.ValidationError("You already rated this film")
                else:
                    return attrs
        else:
            raise serializers.ValidationError("Film, user and rating are required")
        
        


