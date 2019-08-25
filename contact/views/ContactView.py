from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Contact
from ..serializers import ContactInfoSerializer
from ..serializers import ContactSerializer


class ContactView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request, id):
        try:
            contact = Contact.objects.get(pk=id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response(contact.to_representation())

    def post(self, request):
        serializer = ContactSerializer(data=request.data, user=self.request.user)
        if serializer.is_valid():
            contact = serializer.save()
            if contact:
                return Response(contact.to_representation(), status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, id):
        try:
            contact = Contact.objects.get(pk=id, user=request.user)
            contact.delete()
        except Contact.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'success': True})

    def put(self, request, id):
        try:
            contact = Contact.objects.get(pk=id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactSerializer(instance=contact, data=request.data, user=self.request.user)

        if serializer.is_valid():
            contact = serializer.save()
            if contact:
                return Response(contact.to_representation(), status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, id):
        try:
            contact = Contact.objects.get(pk=id, user=request.user)
        except Contact.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ContactInfoSerializer(instance=contact, data=request.data, user=self.request.user)

        if serializer.is_valid():
            contact = serializer.save()
            if contact:
                return Response(contact.to_representation(), status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
