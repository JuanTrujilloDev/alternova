import films.models as film_models
import films.serializers as film_serializers
import rest_framework.views as views
import rest_framework.generics as generics
from rest_framework import renderers, permissions, response, authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from films.utils import StandardResultsSetPagination
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

class HomeView(views.APIView):
    """
    Home view
    """
    renderer_classes = [renderers.TemplateHTMLRenderer ,renderers.JSONRenderer]

    def get(self, request, format=None):
        """
        Home Page

        Response data
        top_films: list of top 5 films ordered by rating
        most_seen: list of top 3 films ordered by visualizations
        random_movie: random film
        """
        
        top_films = film_models.Film.objects.all().order_by("-rating")[:5]
        most_seen = film_models.Film.objects.all().order_by("-visualizations")[:3]
        random_movie = film_models.Film.objects.all().order_by("?").first()
        return response.Response({"top_films":top_films, "most_seen":most_seen, "random_movie":random_movie}, template_name="films/index.html")
    

class FilmListView(LoginRequiredMixin, generics.ListAPIView):
    """
    Film Listing View

    Will return a list of films with pagination and ordering
    Ordering values: title, genre, -film_type, -rating, -visualizations
    Ordering default value: title
    Ordering example: /films/?ordering=-rating

    Page value is not required, default value is 1
    Page example: /films/?page=2

    Page size value is not required, default value is 9

    Ordering and page size example: /films/?ordering=-rating&page=2
    """
    queryset = film_models.Film.objects.all()
    template_name = "films/films.html"
    serializer_class = film_serializers.FilmGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    pagination_class = StandardResultsSetPagination
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    # parameters:
    ordering = openapi.Parameter('ordering', openapi.IN_QUERY, description= f"Ordering value, accepted values: title, genre, -film_type, -rating, -visualizations", type=openapi.TYPE_STRING)
    page = openapi.Parameter('page', openapi.IN_QUERY, description= f"Page number", type=openapi.TYPE_INTEGER)
    page_size = openapi.Parameter('page_size', openapi.IN_QUERY, description= f"Page size, not required always 9", type=openapi.TYPE_INTEGER,  required=False, enum=[9])
    
    @swagger_auto_schema(manual_parameters=[ordering, page, page_size])
    def get(self, request, *args, **kwargs):
        films = self.get_queryset()
        paginator = StandardResultsSetPagination()
        page = paginator.paginate_queryset(films, request)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return paginator.get_paginated_response(serializer.data, template_name="films/films.html", status=200)
        
        serializer = self.get_serializer(films, many=True)
        return response.Response(serializer.data, template_name="films/films.html", status=200)

    def get_queryset(self, *args, **kwargs):
        ordering = self.request.GET.get("ordering")
        acepted_orders = ["title", "genre", "-film_type", "-rating", "-visualizations"]
        if ordering:
            if ordering in acepted_orders:
                if ordering == "genre":
                    queryset = film_models.Film.objects.all().order_by("genre__name")
                else:
                    queryset = film_models.Film.objects.all().order_by(ordering, "title")

                return queryset
            else:
                raise Http404("Ordering not found")
        queryset = film_models.Film.objects.all()
        return queryset
    

class FilmDetailView(LoginRequiredMixin, views.APIView):
    """
    Film Detail View

    Will return a film detail
    """
    template_name = "films/film_detail.html"
    serializer_class = film_serializers.FilmGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        film = self.get_object()
        serializer = self.serializer_class(film)
        return response.Response({'film':serializer.data}, template_name="films/film_detail.html", status=200)

    def get_object(self, *args, **kwargs):
        slug = self.kwargs.get("slug")
        try:
            film = film_models.Film.objects.get(slug=slug)
            return film
        except film_models.Film.DoesNotExist:
            raise Http404("Film not found")
        

class RandomFilmView(LoginRequiredMixin, views.APIView):
    """
    Random Film View

    Will return a random film detail
    """
    
    template_name = "films/film_detail.html"
    serializer_class = film_serializers.FilmGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]

    def get(self, request, *args, **kwargs):
        film = self.get_object()
        serializer = self.serializer_class(film)
        return response.Response({'film':serializer.data}, template_name="films/film_detail.html", status=200)

    def get_object(self, *args, **kwargs):
        try:
            film = film_models.Film.objects.all().order_by("?").first()
            return film
        except film_models.Film.DoesNotExist:
            raise Http404("Film not found")
    

    

       



