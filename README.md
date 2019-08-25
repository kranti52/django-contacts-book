# django-contacts-book
## Contact Book features:
    1. Authentication
    2. One user can create multiple contacts.
        a) Each contact can have multiple phone numbers and multiple email addresses
        b) One contact can't have duplicate emails, but phone number can be duplicate
        c) One user can not have 2 contacts with same email
    3. Multiple Phone number and email can be added using update. Multiple phone number and email can't be added by
    create api.
    4. Partial update of contact basic info can be done using patch
    5. Any contact can be deleted
    6. There is pagination in list api with next and previous page number.
    7. List api can be used to search contact by email address

## Follow these steps to execute after cloning:
    ### Create Virtual Environment
    python3 -m venv contactbook-venv

    ### Activate virtualenv
    source contactbook-venv/bin/activate

    ### Run migrations
    python manage.py migrate

    ### To test after any changes
    python manage.py test
