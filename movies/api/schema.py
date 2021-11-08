import graphene
from graphene_django.types import DjangoObjectType
from .models import Movie, Director
import graphql_jwt
from graphql_jwt.decorators import login_required
from graphene_django.filter import DjangoFilterConnectionField
from graphene import relay


class MovieType(DjangoObjectType):
    class Meta:
        model= Movie

    movie_age= graphene.String()
    def resolve_movie_age(self,info):
        return "Old Movie" if self.year <=2000 else "New Movie"

class DirectorType(DjangoObjectType):
    class Meta:
        model= Director

### relay Implementation
class MovieNode(DjangoObjectType):
    class Meta:
        model= Movie
        filter_fields= {
            'title':['exact','icontains','istartswith'],
            'year':['exact']
        }
        interfaces = (relay.Node ,)

class Query(graphene.ObjectType):
    #all_movies= graphene.List(MovieType)
    all_movies = DjangoFilterConnectionField(MovieNode)

    #movie = graphene.Field(MovieType, title=graphene.String(),id= graphene.Int())
    movie= relay.Node.Field(MovieNode)          #above line is replaced here

    all_directors = graphene.List(DirectorType)
    director = graphene.Field(DirectorType,id= graphene.Int(),name=graphene.String())

    def resolve_all_directors(self,info):
        return Director.objects.all()

    #@login_required                                                     #decorator to check for login cresentials..provided by..from graphql_jwt.decorators import login_required
    #def resolve_all_movies(self,info,**kwargs):
    #    return Movie.objects.all()

    def resolve_director(self,info,**kwargs):
        id=kwargs.get('id')
        name=kwargs.get ('name')

        if name is not None:
            return Director.objects.get(name=name)

        if id is not None:
            return Director.objects.get(pk=id)

        return None

    # @login_required
    # def resolve_movie(self,info,**kwargs):
    #     id = kwargs.get('id')
    #     title = kwargs.get ('title')
    #
    #     if id is not None:
    #         return Movie.objects.get(pk= id)
    #
    #     if title is not None:
    #         return Movie.objects.get(title= title)
    #
    #     #if title is not None:
    #      #   return Movie.objects.get(title='title')
    #
    #     return None


class CreateMovie(graphene.Mutation):
    class Arguments:
        title= graphene.String(required= True)
        year = graphene.Int()

    movie = graphene.Field(MovieType)

    def mutate(self,info,title,year):
        movie=Movie.objects.create(title=title,year=year)
        return CreateMovie(movie=movie)

class MovieUpdateMutation(graphene.Mutation):
    class Arguments:
        title= graphene.String()
        year = graphene.Int()
        id = graphene.ID(required=True)

    movie=graphene.Field(MovieType)

    def mutate(self,info,id,title,year):

        movie=Movie.objects.get(pk=id)


        if title is not None:
            movie.title=title

        if year is not None:
            movie.year=year
        movie.save()

        return MovieUpdateMutation(movie=movie)

class MovieDeleteMutation(graphene.Mutation):
    class Arguments:
        id = graphene.ID(required=True)

    movie=graphene.Field(MovieType)

    def mutate(self,info,id):
        movie=Movie.objects.get(pk=id)

        movie.delete()
        return MovieDeleteMutation(movie=None)


class Mutation :
    token_auth = graphql_jwt.ObtainJSONWebToken.Field()

    create_movie= CreateMovie.Field()
    update_movie=MovieUpdateMutation.Field()
    delete_movie = MovieDeleteMutation.Field()



