from django.contrib.auth.models import User
from django.db import models


class Contact(models.Model):
    """Contact model."""
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True, null=True)
    last_name = models.CharField(max_length=200)
    nickname = models.CharField(max_length=100, blank=True)
    designation = models.CharField(max_length=200, blank=True)
    company = models.CharField(max_length=255, blank=True)
    user = models.ForeignKey(User, blank=True, null=True, related_name='user_contacts', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'contacts_people'
        app_label = 'contact'

    def __str__(self):
        return self.fullname

    @property
    def fullname(self):
        return "%s %s %s" % (self.first_name, self.middle_name, self.last_name)

    def to_representation(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'middle_name': self.middle_name,
            'nickname': self.nickname,
            'designation': self.designation,
            'company': self.company,
            'phone_numbers': [phone.to_representation() for phone in self.contact_phone_number.all()],
            'email_addresses': [email.to_representation() for email in self.contact_email_address.all()]
        }
