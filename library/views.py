import django.contrib.auth
from django.shortcuts import render

# Create your views here.
from rest_framework.decorators import api_view
from rest_framework.response import Response
import rest_framework
from rest_framework import status
from .models import User, Book
from .serializers import UserSerializer,BookSerializer
from django.shortcuts import get_object_or_404
from rest_framework import permissions
from rest_framework import renderers
from django.contrib.auth import authenticate, login
from rest_framework import authentication
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template import loader
from rest_framework import status, permissions, serializers
from rest_framework.response import Response
from rest_framework.views import APIView


from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ViewSet, ModelViewSet
from rest_framework.permissions import AllowAny,IsAdminUser
from .models import User
from .serializers import UserSerializer


class UserViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [TokenAuthentication]

    def get_permissions(self):
        permission_classes = []
        if self.action == 'create':
            permission_classes = [IsAdminUser]
        elif self.action == 'retrieve' or self.action == 'update' or self.action == 'partial_update':
            permission_classes = [IsAdminUser]
        elif self.action == 'destroy':
            permission_classes = [IsAdminUser]
        return [permission() for permission in permission_classes]


class LoginView(ViewSet):
    serializer_class = AuthTokenSerializer

    def create(request):
        return ObtainAuthToken().post(request)


class LogoutView(APIView):
    def get(self, request, format=None):
        request.user.auth_token.delete()
        return Response(status=status.HTTP_200_OK)


# @api_view(["POST"])
# #@permission_classes([AllowAny])
# def Register_Users(request):
#         data = []
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             account = serializer.save()
#           #  account.is_active = True
#             account.save()
#             token = Token.objects.get_or_create(user=account)[0].key
#             data["message"] = "user registered successfully"
#             data["email"] = account.email
#             data["username"] = account.username
#             data["token"] = token
#
#         else:
#             data = serializer.errors


#        return Response(data)

def books(request):
  books = Book.objects.all().values()
  template = loader.get_template('books.html')
  context = {
    'books': books,
  }
  return HttpResponse(template.render(context, request))


@api_view(['POST'])
def view_login(request):
        username = request.POST.get('username','shalini')
        email = request.POST.get('email', 'abc@gmail.com')
        password = request.POST.get('password', 'password')
        user = authenticate(request, email=email, username=username, password=password)
        if user is not None:
          #  login(request,user)
            return (Response(status.HTTP_200_OK, template_name ="login.html"))

        else:
            # Return an 'invalid login' error message.
            return (Response(status.HTTP_400_BAD_REQUEST))


@api_view(['GET'])
def admin(request):
    api_urls = {
        'all_items': '/',
        'Add': '/create',
        'Update': '/update/pk',
        'Delete': '/book/pk/delete'
    }
   # render(request, 'home.html')
    return Response(api_urls, template_name='home.html')
#return render(request, "index.html")

@api_view(['POST'])
def add_books(request):
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    book = BookSerializer(data=request.data)

    # validating for already existing data
    if Book.objects.filter(**request.data).exists():
        raise rest_framework.serializers.ValidationError('This data already exists')
    #render(request, 'add_book.html')

    if book.is_valid():
        book.save()
        return Response(book.data, template_name='add_book.html')
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
def view_books(request):

    items = Book.objects.all()
    print(type(items))
    result = []

    for item in items:
            #if BookSerializer(items).is_valid():
            data = BookSerializer(item)
            #print(data.data)
            result.append(data.data)
            #render(request, 'view_book.html')
            renderer_classes = renderers.TemplateHTMLRenderer
            template_name = 'login.html'

    return Response(result, template_name='login.html')



@api_view(['POST'])
def update_books(request, pk):
   # permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    book = Book.objects.get(pk=pk)
    data = BookSerializer(instance=book, data=request.data)

    if data.is_valid():
        data.save()
        return Response(data.data)
    else:
        return Response(status=status.HTTP_404_NOT_FOUND)

@api_view(['DELETE'])
def delete_books(request, pk):
        book = get_object_or_404(Book, pk=pk)
        book.delete()
        return Response(status=status.HTTP_202_ACCEPTED)
