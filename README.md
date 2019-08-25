# django-contacts-book
Contact Book features:
    1. Authentication
    2. One user can create multiple contacts.
        a) Each contact can have multiple phone number and multiple email address
        b) One user can't have any contact with same email multiple times, infact can't have multiple contact with same
        email but multiple contact can have same phone number and 1 phone number can same phone number.
    3. Multiple Phone number and email can be added using update. Multiple phone number and email can't be added by
    create api.
    4. Partial update of contact basic info can be done using patch
    5. Any contact can be deleted
    6. There is pagination in list api with next and previous page number.
    7. List api can be used to search contact by email address
