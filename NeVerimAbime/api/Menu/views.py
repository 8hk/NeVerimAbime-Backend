from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK, HTTP_201_CREATED
from rest_framework.response import Response
import sys
# Create your views here.
from api.MealItem.models import MealItem
from api.Menu.models import Menu
from api.Menu.serializers import MenuSerializer
from api.models import User
from api.recipe.models import Recipe
from rest_framework.decorators import api_view, action
from rest_framework import viewsets, serializers, permissions
class MenuViewSet(viewsets.ModelViewSet):

    serializer_class = MenuSerializer
    queryset = Menu.objects.all()
    def create(self, request, *args, **kwargs):
        # logger = logging.getLogger('django')
        try:
            user = User.objects.get(id=request.user.id)
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            menu= Menu.objects.create(
                name=request.data['name'],
                menu_owner=user
            )

            for meal in request.data['createMealItems']:
                if len(meal['name'])>0:
                    recipe = Recipe.objects.get(uuid=meal['recipe'])

                    dummyMeal = MealItem.objects.create(
                        name=meal['name'],
                        recipe=recipe,
                        amount=meal['amount'],
                        price=meal['price'],
                        description=meal['description'],
                        meal_item_owner=user)

                    menu.meal_items.add(dummyMeal)
                    menu.save()



            return Response(menu.uuid, status=HTTP_201_CREATED)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Menu throws error", status=HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="getmenus", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getmenus(self, request, *args, **kwargs):
        try:
            menus = Menu.objects.filter(menu_owner=User.objects.get(id=request.query_params['id']))
            menu_serializer = MenuSerializer(menus, many=True)
            return Response(menu_serializer.data, status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Menu throws error", status=HTTP_400_BAD_REQUEST)

    @action(methods=["get"], url_path="getmenu", detail=False, permission_classes=[permissions.IsAuthenticated])
    def getmenu(self, request, *args, **kwargs):
        try:
            menu = Menu.objects.get(uuid=request.query_params['uuid'])
            menu_serializer = MenuSerializer(menu, many=False)
            return Response(menu_serializer.data, status=HTTP_200_OK)
        except:
            for error in sys.exc_info():
                print(str(error))
            return Response(data="Menu throws error", status=HTTP_400_BAD_REQUEST)
