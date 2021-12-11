## Disable new user registration. New user accounts must be created from within
## Django Admin Panel by an existing administrator.
## https://stackoverflow.com/questions/29794052/how-could-one-disable-new-account-creation-with-django-allauth-but-still-allow
from allauth.account.adapter import DefaultAccountAdapter


class NoNewUsersAccountAdapter(DefaultAccountAdapter):

    def is_open_for_signup(self, request):
        """
        Checks whether or not the site is open for signups.

        Next to simply returning True/False you can also intervene the
        regular flow by raising an ImmediateHttpResponse

        (Comment reproduced from the overridden method.)
        """
        return False
