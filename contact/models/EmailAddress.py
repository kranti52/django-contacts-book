from django.db import models

from .Contact import Contact


class EmailAddress(models.Model):
    EMAIL_TYPE_CHOICES = (
        ('home', 'Home'),
        ('work', 'Work'),
        ('other', 'Other')
    )
    type = models.CharField(max_length=10, choices=EMAIL_TYPE_CHOICES)
    contact_object = models.ForeignKey(Contact, related_name='contact_email_address', on_delete=models.CASCADE)
    email_address = models.EmailField(max_length=255, db_index=True)
    date_added = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)

    def __str__(self):
        return "%s (%s)" % (self.email_address, self.type)

    class Meta:
        db_table = 'contacts_email_addresses'
        app_label = 'contact'
        unique_together = (('contact_object', 'email_address'),)

    def to_representation(self):
        return {
            'id': self.id,
            'type': self.type,
            'email_address': self.email_address
        }
