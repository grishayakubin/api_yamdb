from rest_framework import routers

from django.urls import include, path

from .views import CategoriesViewSet, GenresViewSet, TitlesViewSet


router = routers.DefaultRouter()
router.register(r'categories', CategoriesViewSet, basename='categories')
router.register(r'genres', GenresViewSet, basename='genres')
router.register(r'titles', TitlesViewSet, basename='titles')

urlpatterns = [
    path('v1/', include(router.urls)),
]
