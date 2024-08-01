from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from ..models.commerce import Commerce
from ..serializers.commerce import CommerceSerializer
from ..services.commerce import create_commerce, get_all_commerces, update_commerce, delete_commerce, get_commerce_by_id

class CommerceListCreateView(generics.GenericAPIView):
    serializer_class = CommerceSerializer

    def get(self, request, *args, **kwargs):
        commerces = get_all_commerces()
        serializer = self.get_serializer(commerces, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        commerce = create_commerce(serializer.validated_data)
        return Response(CommerceSerializer(commerce).data, status=status.HTTP_201_CREATED)

class CommerceDetailView(generics.GenericAPIView):
    serializer_class = CommerceSerializer

    def get(self, request, commerce_id, *args, **kwargs):
        commerce = get_commerce_by_id(commerce_id)
        if not commerce:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(CommerceSerializer(commerce).data)

    def put(self, request, commerce_id, *args, **kwargs):
        commerce = get_commerce_by_id(commerce_id)
        if not commerce:
            return Response(status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        updated_commerce = update_commerce(commerce_id, serializer.validated_data)
        return Response(CommerceSerializer(updated_commerce).data)

    def delete(self, request, commerce_id, *args, **kwargs):
        commerce = delete_commerce(commerce_id)
        if not commerce:
            return Response(status=status.HTTP_404_NOT_FOUND)
        return Response(status=status.HTTP_204_NO_CONTENT)