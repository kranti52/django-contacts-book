from rest_framework import serializers

from ..models import Contact
from ..models import EmailAddress
from ..models import PhoneNumber


class ContactSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=True, max_length=200)
    middle_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    last_name = serializers.CharField(required=True, max_length=200)
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    company = serializers.CharField(required=False, allow_blank=True, max_length=255)
    designation = serializers.CharField(required=False, allow_blank=True, max_length=200)
    phone_number_type = serializers.ChoiceField(required=False, choices=PhoneNumber.PHONE_NUMBER_TYPE_CHOICES)
    phone_number = serializers.CharField(required=False, max_length=50)
    email_type = serializers.ChoiceField(required=True, choices=EmailAddress.EMAIL_TYPE_CHOICES)
    email_address = serializers.EmailField(required=True, max_length=255)

    def __init__(self, instance=None, data=None, user=None, many=False):
        super().__init__(instance=instance, data=data, many=many)
        self.user = user

    def create(self, validated_data):
        user = self.user
        try:
            phone_number = validated_data.pop('phone_number')
        except KeyError:
            phone_number = None

        try:
            phone_number_type = validated_data.pop('phone_number_type')
        except KeyError:
            phone_number_type = 'other'

        try:
            email_address = validated_data.pop('email_address')

        except KeyError:
            email_address = None

        try:
            email_type = validated_data.pop('email_type')
        except KeyError:
            email_type = 'other'

        validation_error = {}
        if user.user_contacts.filter(contact_email_address__email_address=email_address).exists():
            validation_error['email'] = [" Contact already exists. "]

        if validation_error:
            raise serializers.ValidationError(validation_error)

        validated_data['user'] = user
        contact = Contact.objects.create(**validated_data)
        if email_address:
            EmailAddress.objects.create(contact_object=contact, email_address=email_address, type=email_type)
        if phone_number:
            PhoneNumber.objects.create(contact_object=contact, phone_number=phone_number, type=phone_number_type)
        return contact

    def update(self, instance, validated_data):
        user = self.user
        try:
            phone_number = validated_data.pop('phone_number')
        except KeyError:
            phone_number = None

        try:
            phone_number_type = validated_data.pop('phone_number_type')
        except KeyError:
            phone_number_type = 'other'

        try:
            email_address = validated_data.pop('email_address')

        except KeyError:
            email_address = None

        try:
            email_type = validated_data.pop('email_type')
        except KeyError:
            email_type = 'other'
        contact = instance
        validation_error = {}

        if user.user_contacts.filter(contact_email_address__email_address=email_address).exists():
            validation_error['email'] = [" Contact already exists. "]

        if validation_error:
            raise serializers.ValidationError(validation_error)

        contact.first_name = validated_data['first_name']
        contact.last_name = validated_data['last_name']
        contact.middle_name = validated_data['middle_name']
        contact.nickname = validated_data['nickname']
        contact.company = validated_data['company']
        contact.designation = validated_data['designation']
        contact.save()

        if email_address:
            EmailAddress.objects.create(contact_object=contact, email_address=email_address, type=email_type)
        if phone_number:
            PhoneNumber.objects.create(contact_object=contact, phone_number=phone_number, type=phone_number_type)
        return contact

    def to_representation(self, instance):
        return {
            'id': instance.id,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'middle_name': instance.middle_name,
            'nickname': instance.nickname,
            'designation': instance.designation,
            'company': instance.company,
            'phone_numbers': [phone.to_representation() for phone in instance.contact_phone_number.all()],
            'email_addresses': [email.to_representation() for email in instance.contact_email_address.all()]
        }

    class Meta:
        model = Contact
        fields = ('first_name', 'middle_name', 'last_name', 'nickname', 'company', 'designation', 'phone_number_type',
                  'phone_number', 'email_type', 'email_address')
