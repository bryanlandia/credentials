"""
Helper methods for credential app.
"""
import datetime
import hashlib
import logging
from itertools import groupby

import jwt
from django.conf import settings
from django.core.cache import cache
from edx_rest_api_client.client import EdxRestApiClient

log = logging.getLogger(__name__)


def validate_duplicate_attributes(attributes):
    """
    Validate the attributes data

    Arguments:
        attributes (list): List of dicts contains attributes data

    Returns:
        Boolean: Return True only if data has no duplicated namespace and name

    """

    def keyfunc(attribute):  # pylint: disable=missing-docstring
        return attribute['name']

    sorted_data = sorted(attributes, key=keyfunc)
    for __, group in groupby(sorted_data, key=keyfunc):
        if len(list(group)) > 1:
            return False
    return True


def get_user_data(username):
    """ Retrieve the user detail from the User API.

    If the API call is successful, the returned data will be cached for the
    duration of USER_CACHE_TTL (in seconds). Failed API responses will NOT
    be cached.

    Arguments:
        username (str): Unique identifier of the user for retrieval

    Returns:
        dict, representing user data returned by the User API.
    """
    return {
        "username": "clintonb",
        "bio": None,
        "requires_parental_consent": False,
        "name": "Clinton Blackburn",
        "country": "US",
        "is_active": True,
        "profile_image": {
            "image_url_full": "https://d1kekzok76m982.cloudfront.net/stage/8f5d3a898012008f48d321b042e53b3d_500.jpg?v=1460425196",
            "image_url_large": "https://d1kekzok76m982.cloudfront.net/stage/8f5d3a898012008f48d321b042e53b3d_120.jpg?v=1460425196",
            "image_url_medium": "https://d1kekzok76m982.cloudfront.net/stage/8f5d3a898012008f48d321b042e53b3d_50.jpg?v=1460425196",
            "image_url_small": "https://d1kekzok76m982.cloudfront.net/stage/8f5d3a898012008f48d321b042e53b3d_30.jpg?v=1460425196",
            "has_image": True
        },
        "year_of_birth": 1986,
        "level_of_education": None,
        "accomplishments_shared": False,
        "goals": "",
        "language_proficiencies": [
            {
                "code": "en"
            }
        ],
        "gender": None,
        "account_privacy": "all_users",
        "mailing_address": "1234 Anylane\r\nTempe, AZ 85234\r\n",
        "email": "cblackburn@edx.org",
        "date_joined": "2014-06-09T15:24:23Z"
    }
    cache_key = 'user.api.data.{hash}'.format(hash=_make_hash(username))
    user = cache.get(cache_key)

    if user:
        return user

    user_api = get_user_api_client()
    user = user_api.accounts(username).get()
    cache.set(cache_key, user, settings.USER_CACHE_TTL)

    return user


def get_user_api_client():
    """
    Return api client to communicate with the user api by using the credentials
    service user in the LMS.
    """
    user_api_url = settings.USER_API_URL
    service_username = settings.CREDENTIALS_SERVICE_USER
    jwt_audience = settings.USER_JWT_AUDIENCE
    jwt_secret_key = settings.USER_JWT_SECRET_KEY

    # user api don't accept url with trailing slash so make `append_slash` False
    return _get_service_user_api_client(
        user_api_url, service_username, jwt_audience, jwt_secret_key, append_slash=False
    )


def _get_service_user_api_client(api_url, service_username, jwt_audience, jwt_secret_key, **kwargs):
    """
    Helper method to get edx rest api client for the provided service user
    which is present on the system from 'api_url'.

    Arguments:
        api_url (str): Absolute url of the api
        service_username (str): Username of the service user
        jwt_audience (str): JWT key for the api auth
        jwt_secret_key (str): JWT secret key for the api auth

    """
    now = datetime.datetime.utcnow()
    expires_in = getattr(settings, 'OAUTH_ID_TOKEN_EXPIRATION', 30)
    payload = {
        'preferred_username': service_username,
        'username': service_username,
        'iss': settings.SOCIAL_AUTH_EDX_OIDC_URL_ROOT,
        'exp': now + datetime.timedelta(seconds=expires_in),
        'iat': now,
        'aud': jwt_audience,
    }

    try:
        jwt_data = jwt.encode(payload, jwt_secret_key)
        api_client = EdxRestApiClient(api_url, jwt=jwt_data, **kwargs)
    except Exception:  # pylint: disable=broad-except
        log.exception("Failed to initialize the API client with url '%s'.", api_url)
        return

    return api_client


def _make_hash(key):
    """
    Returns the string based on a the hash of the provided key.
    """
    return hashlib.md5(key).hexdigest()
