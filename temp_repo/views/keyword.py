from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models.keyword import Keyword
from ..serializers.keyword import KeywordSerializer
from ..services.keyword import create_keyword, get_all_keywords, update_keyword, delete_keyword, get_keyword_by_id

class KeywordListCreateView(generics.GenericAPIView):
    serializer_class = KeywordSerializer

    def get(self, request, *args, **kwargs):
        keywords = get_all_keywords()
        serializer = self.get_serializer(keywords, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        keyword = create_keyword(serializer.validated_data)
        return Response(KeywordSerializer(keyword).data, status=status.HTTP_201_CREATED)

class KeywordDetailView(generics.GenericAPIView):
    serializer_class = KeywordSerializer

    def get(self, request, keyword_id, *args, **kwargs):
        keyword = get_keyword_by_id(keyword_id)
        if not keyword:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(KeywordSerializer(keyword).data)

    def put(self, request, keyword_id, *args, **kwargs):
        keyword = get_keyword_by_id(keyword_id)
        if not keyword:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_keyword = update_keyword(keyword_id, serializer.validated_data)
        return Response(KeywordSerializer(updated_keyword).data)

    def delete(self, request, keyword_id, *args, **kwargs):
        keyword = delete_keyword(keyword_id)
        if not keyword:
            return Response(status=status.HTTP_404_NOT_FOUND)