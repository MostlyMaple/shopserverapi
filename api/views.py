from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.db.models import Q
from django.http import JsonResponse
from base.models import Item
from base.forms import ItemForm
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework import status
from .serializers import ItemSerializer
from .serializers import UserSerializer
from .serializers import UserSerializerWithToken

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)

        serializer = UserSerializerWithToken(self.user).data

        for k, v in serializer.items():
            data[k] = v

        return data

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer

@api_view(['GET'])
def apiOverview(request):
    api_urls = {
        'Search':'/search/<str:pk>',
        'Item Detail':'/get-item/<str:pk>',
        'Create Item':'/create-item',
        'Update Item':'/update-item/<str:pk>',
        'Delete Item':'/delete-item/<str:pk>',
    }
    return Response(api_urls)


"""
Search: Returns specific item queries, ?q=<>
"""
@api_view(['GET'])
def search(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    items = Item.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(item_name__icontains=q) |
        Q(description__icontains=q)
    ).values()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

"""
Item Functions

"""

@api_view(['GET'])
def getItem(request, pk):
    curItem = Item.objects.get(id=pk)
    serializer = ItemSerializer(curItem, many=False)
    return Response(serializer.data)




@api_view(['GET','POST'])
@permission_classes([IsAdminUser])
def createItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'ItemCreated':True})
    return JsonResponse({'ItemCreated':False})




@api_view(['POST'])
@permission_classes([IsAdminUser])
def createItem(request):
    serializer = ItemSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)




@api_view(['POST'])
@permission_classes([IsAdminUser])
def updateItem(request, pk):
    curItem = Item.objects.get(id=pk)
    serializer = ItemSerializer(instance=curItem, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)




@api_view(['DELETE'])
@permission_classes([IsAdminUser])
def deleteItem(request, pk):
    curItem = Item.objects.get(id=pk)
    curItem.delete()
    return JsonResponse("Item Deleted!")


"""
User Functions
"""
@api_view(['POST'])
def registerUser(request):
    data = request.data

    try:
        user = User.objects.create(
            first_name=data['name'],
            username=data['email'],
            email=data['email'],
            password=make_password(data['password'])
        )
        serializer = UserSerializerWithToken(user, many=False)
        return Response(serializer.data)
    except:
        message = {'detail':'User with this email already exists'}
        return Response(message, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def getUserProfile(request):
    user = request.user
    serializer = UserSerializer(user, many=False)
    return Response(serializer.data)



@api_view(['GET'])
@permission_classes([IsAdminUser])
def getUsers(request):
    users = User.objects.all()
    serializer = UserSerializer(users, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes([IsAdminUser])
def updateUser(request, pk):
    curUser = User.objects.get(id=pk)
    serializer = UserSerializer(instance=curUser, data=request.data)
    if serializer.is_valid():
        serializer.save()
    return Response(serializer.data)