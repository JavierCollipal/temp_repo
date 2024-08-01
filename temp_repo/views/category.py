from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models.category import Category
from ..serializers.category import CategorySerializer
from ..services.category import create_category, get_all_categories, update_category, delete_category, get_category_by_id

class CategoryListCreateView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, *args, **kwargs):
        categories = get_all_categories()
        serializer = self.get_serializer(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        category = create_category(serializer.validated_data)
        return Response(CategorySerializer(category).data, status=status.HTTP_201_CREATED)

class CategoryDetailView(generics.GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request, category_id, *args, **kwargs):
        category = get_category_by_id(category_id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(CategorySerializer(category).data)

    def put(self, request, category_id, *args, **kwargs):
        category = get_category_by_id(category_id)
        if not category:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_category = update_category(category_id, serializer.validated_data)
        return Response(CategorySerializer(updated_category).data)

    def delete(self, request, category_id, *args, **kwargs):
        category = delete_category(category_id)
        if not category:
           return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)