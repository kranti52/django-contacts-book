from rest_framework import serializers

from ..models import Contact


class ContactInfoSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField(required=False, max_length=200)
    middle_name = serializers.CharField(required=False, allow_blank=True, max_length=200)
    last_name = serializers.CharField(required=False, max_length=200)
    nickname = serializers.CharField(required=False, allow_blank=True, max_length=100)
    company = serializers.CharField(required=False, allow_blank=True, max_length=255)
    designation = serializers.CharField(required=False, allow_blank=True, max_length=200)

    def __init__(self, instance, data=None, user=None, many=False):
        super().__init__(instance=instance, data=data, many=many)
        self.user = user

    def update(self, instance, validated_data):
        contact = instance
        if validated_data.get('first_name'):
            contact.first_name = validated_data['first_name']
        if validated_data.get('last_name'):
            contact.last_name = validated_data['last_name']
        if 'middle_name' in validated_data:
            contact.middle_name = validated_data['middle_name'] if validated_data['middle_name'] else ""
        if 'nickname' in validated_data:
            contact.nickname = validated_data['nickname'] if validated_data['nickname'] else ""
        if 'company' in validated_data:
            contact.company = validated_data['company'] if validated_data['company'] else ""
        if 'designation' in validated_data:
            contact.designation = validated_data['designation'] if validated_data['designation'] else ""
        contact.save()
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
        }

    class Meta:
        model = Contact
        fields = ('first_name', 'middle_name', 'last_name', 'nickname', 'company', 'designation')
