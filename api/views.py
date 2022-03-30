from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.db.models import Q
from django.http import JsonResponse
from base.models import Item
from base.forms import ItemForm

from .serializers import ItemSerializer


@api_view(['GET'])
def getClothes(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    items = Item.objects.filter(
        Q(topic__name__icontains=q) | 
        Q(item_name__icontains=q) |
        Q(description__icontains=q)
    ).values()
    serializer = ItemSerializer(items, many=True)
    return Response(serializer.data)

@api_view(['GET','POST'])
def createItem(request):
    if request.method == 'POST':
        form = ItemForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return JsonResponse({'ItemCreated':True})
    return JsonResponse({'ItemCreated':False})