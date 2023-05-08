import films.models as film_models
import films.serializers as film_serializers
import rest_framework.views as views
import rest_framework.generics as generics
from rest_framework import renderers, permissions, response, authentication
from django.contrib.auth.mixins import LoginRequiredMixin
from films.utils import StandardResultsSetPagination, FilteredDataResultsSetPagination
from django.http import Http404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from django.urls import reverse
from functools import reduce
from django.db.models import Q

class HomeView(generics.ListAPIView):
    """
    Home view

    Response data
    top_films: list of top 5 films ordered by rating
    most_seen: list of top 3 films ordered by visualizations
    random_movie: random film
    """
    renderer_classes = [renderers.TemplateHTMLRenderer ,renderers.JSONRenderer]
    template_name = "films/index.html"
    permission_classes = [permissions.AllowAny]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    serializer_class = film_serializers.FilmGetSerializer

    def get(self, request, format=None):
        """
        Get method
        """
        
        top_films = film_models.Film.objects.all().order_by("-rating")[:5]
        most_seen = film_models.Film.objects.all().order_by("-visualizations")[:3]
        random_movie = film_models.Film.objects.all().order_by("?").first()

        top_films = self.serializer_class(top_films, many=True).data
        most_seen = self.serializer_class(most_seen, many=True).data
        random_movie = self.serializer_class(random_movie).data


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
        

class VisualizeFilmView(LoginRequiredMixin, generics.CreateAPIView):
    """
    Visualize Film View

    Will create a film visualization and return the film data with the new visualization

    required parameters:
    film: film id
    user: user id
    """


    serializer_class = film_serializers.FilmVisualizationSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    renderer_classes = [renderers.JSONRenderer]
    
    def get_object(self, data, *args, **kwargs):
        """
        get the film object from the film id
        """
        film_id = data.get("film")
        try:
            film = film_models.Film.objects.get(pk=film_id)
            return film
        except film_models.Film.DoesNotExist:
            raise Http404("Film not found")
    
    def post(self, request, *args, **kwargs):
        """
        post method

        will create a film visualization and return the film data with the new visualization
        """
        film = self.get_object(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(film=film, user=request.user)
            film = {**serializer.data, "film_slug":film.slug ,"visualizations":film.visualizations}
            return response.Response({"film_data":film, "message":"You have successfully rated the film"}, status=201)
        return response.Response(serializer.errors, status=400)
        

class RateFilmView(LoginRequiredMixin, generics.CreateAPIView):
    """
    Rate Film View
    Will rate a film and return the film data with the new rating

    required parameters:
    film: film id
    rating: rating value
    user: user id
    """
    serializer_class = film_serializers.FilmRatingSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    renderer_classes = [renderers.JSONRenderer]

    def get_object(self, data, *args, **kwargs):
        """
        get_object method

        Will return the film object from the film id 
        sended in the request data
        """
        film_id = data.get("film")
        try:
            film = film_models.Film.objects.get(pk=film_id)
            return film
        except film_models.Film.DoesNotExist:
            raise Http404("Film not found")
        
    def post(self, request, *args, **kwargs):
        """
        post method

        receives the request data and returns the film data with the new rating
        or the errors if the data is not valid
        """
        film = self.get_object(request.data)
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save(film=film, user=request.user)
            film = {**serializer.data, "film_slug":film.slug ,"visualizations":film.visualizations}
            return response.Response({"film_data":film, "message":"You have successfully rated the film"}, status=201)
        return response.Response(serializer.errors, status=400)


class SearchFilmView(LoginRequiredMixin, generics.ListAPIView):
    """
    Search Film View

    Will return a list of films filtered by title, genre or film type
    """
    
    template_name = "films/search.html"
    serializer_class = film_serializers.FilmGetSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [authentication.SessionAuthentication, authentication.TokenAuthentication]
    renderer_classes = [renderers.TemplateHTMLRenderer, renderers.JSONRenderer]
    pagination_class = FilteredDataResultsSetPagination

    
     # parameters:
    title = openapi.Parameter('title', openapi.IN_QUERY, description= f"Title Filter, must use any film title name.", type=openapi.TYPE_STRING)
    film_type = openapi.Parameter('film_type', openapi.IN_QUERY, description= f"Film Type Filter, must use any film type name.", type=openapi.TYPE_STRING)
    genres = openapi.Parameter('genres', openapi.IN_QUERY, description= f"Genre Filter, must use any genre name.", type=openapi.TYPE_ARRAY, items=openapi.Items(type=openapi.TYPE_STRING))
    page = openapi.Parameter('page', openapi.IN_QUERY, description= f"Page number", type=openapi.TYPE_INTEGER)
    page_size = openapi.Parameter('page_size', openapi.IN_QUERY, description= f"Page size, not required always 9", type=openapi.TYPE_INTEGER,  required=False, enum=[9])


    @swagger_auto_schema(manual_parameters=[title, film_type, genres, page, page_size])
    def get(self, request, *args, **kwargs):
        """
        get method for search film view

        Will return a list of films filtered by title, genre or film type
        or a message if no films were found/ no filters were provided
        """
        title = self.request.GET.get("title", None)
        genres = self.request.GET.getlist("genres", None)
        film_type = self.request.GET.get("film_type", None)

        genres_list = film_models.Genre.objects.all().values('name')
        film_types_list = film_models.FilmType.objects.all().values('name')

        filtering_data = {'genres_list': genres_list, 'film_types_list': film_types_list}

        if not title and not genres and not film_type:
            return response.Response({"message":"Please provide a title, genre or film type", "filtering_data":filtering_data}, template_name="films/search.html", status=200)
        
        films = self.get_queryset()
        
        if films:
            paginator = FilteredDataResultsSetPagination()
            page = paginator.paginate_queryset(films, request)
            if page is not None:
                serializer = self.get_serializer(page, many=True)
                return paginator.get_paginated_response({"results":serializer.data, "filtering_data":filtering_data}, template_name="films/search.html", status=200)
            
            serializer = self.get_serializer(films, many=True)
            return response.Response({"results":serializer.data, "filtering_data":filtering_data}, template_name="films/search.html", status=200)
        
        return response.Response({"message":"No films found", "filtering_data":filtering_data}, template_name="films/search.html", status=200)
    

    def get_queryset(self, *args, **kwargs):
        """
        get queryset method for search film view

        Will return a queryset with list of films filtered by title, genre or film type
        or a empty queryset if no films were found
        or None if no filters were provided
        """
        title = self.request.GET.get("title", None)
        genres = self.request.GET.getlist("genres", None)
        film_type = self.request.GET.get("film_type", None)
        
        query = []

        if title:
            films_by_title = film_models.Film.objects.filter(title__icontains=title)
            query.append(films_by_title)

        if genres:
            
            genres = genres[0].split(",")
            films_by_genre = film_models.Film.objects.all()
            for genre in genres:
                films_by_genre = films_by_genre.filter(genre__name__iexact=genre)
            
            
            
            query.append(films_by_genre)

        if film_type:
            films_by_type = film_models.Film.objects.filter(film_type__name__iexact=film_type)
            query.append(films_by_type)

        if len(query) > 0:
            query = reduce(lambda x, y: x & y, query)
            return query.distinct().order_by("-rating")
        
        return None

    
    



    

    

       



