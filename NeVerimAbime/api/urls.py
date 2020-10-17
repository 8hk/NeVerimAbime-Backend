from django.urls import path
from rest_framework.routers import DefaultRouter

from .CaloriesPerDay.views import CaloriesPerDayViewSet
from .Comments.views import CommentsViewSet
from .Likes.views import LikeViewSet
from .MealItem.views import MealItemViewSet
from .Menu.views import MenuViewSet
from .ingredient.views import IngredientViewSet, nutrient_view
from .nutrient.views import NutrientViewSet
from .recipe.views import RecipeViewSet
from .tag.views import TagViewSet
from .views import (
    UserViewSet, UserListView,
)

router = DefaultRouter()

router.register(r'users', UserViewSet)
router.register(r'recipe', RecipeViewSet)
router.register(r'nutrient', NutrientViewSet)
router.register(r'ingredient', IngredientViewSet)
router.register(r'comments', CommentsViewSet)
router.register(r'tag', TagViewSet)
router.register(r'menu', MenuViewSet)
router.register(r'mealitem', MealItemViewSet)
router.register(r'cpd', CaloriesPerDayViewSet)
router.register(r'likes', LikeViewSet)
urlpatterns = router.urls
