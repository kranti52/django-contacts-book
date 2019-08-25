from django.db import models

from .Contact import Contact


class PhoneNumber(models.Model):
    """Phone Number model."""
    PHONE_NUMBER_TYPE_CHOICES = (
        ('home', 'Home'),
        ('mobile', 'Mobile'),
        ('fax', 'Fax'),
        ('work', 'Work'),
        ('other', 'Other')
    )
    type = models.CharField(max_length=10, choices=PHONE_NUMBER_TYPE_CHOICES)
    contact_object = models.ForeignKey(Contact, related_name='contact_phone_number', on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=50)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.phone_number, self.type)

    class Meta:
        db_table = 'contacts_phone_numbers'
        app_label = 'contact'

    def to_representation(self):
        return {
            'id': self.id,
            'type': self.type,
            'phone_number': self.phone_number
        }
