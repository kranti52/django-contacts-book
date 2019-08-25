from django.core.paginator import Paginator, EmptyPage
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Contact


class ContactListView(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        filter_email = request.GET.get('email')
        try:
            contacts = Contact.objects.filter(user=request.user)
            if filter_email:
                contacts = contacts.filter(contact_email_address__email_address=filter_email)
            contacts = contacts.order_by('id')
            paginator = Paginator(contacts, 10)
        except Contact.DoesNotExist:
            return Response({'error': 'Not Found'}, status=status.HTTP_404_NOT_FOUND)
        if not filter_email:
            page = int(request.GET.get('page', 1))
        else:
            page = 1
        try:
            page_contacts = paginator.page(page)
        except EmptyPage:
            return Response({'error': 'Page Not Found'}, status=status.HTTP_404_NOT_FOUND)

        contact_data = []
        for contact in page_contacts:
            contact_data.append(contact.to_representation())
        response = {
            'current_page': page,
            'next_page': page_contacts.next_page_number() if page_contacts.has_next() else None,
            'previous_page': page_contacts.previous_page_number() if page_contacts.has_previous() else None,
            'total_page': paginator.num_pages,
            'total_contacts': paginator.count,
            'contacts': contact_data
        }
        return Response(response)
