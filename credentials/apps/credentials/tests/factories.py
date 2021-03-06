from __future__ import unicode_literals

import uuid

import factory

from credentials.apps.core.tests.factories import SiteFactory
from credentials.apps.credentials import constants
from credentials.apps.credentials import models

PASSWORD = 'dummy-password'


class CertificateTemplateFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.CertificateTemplate

    name = factory.Sequence(lambda n: 'template%d' % n)
    content = '<html></html>'


class AbstractCertificateFactory(factory.django.DjangoModelFactory):
    site = factory.SubFactory(SiteFactory)
    template = factory.SubFactory(CertificateTemplateFactory)


class CourseCertificateFactory(AbstractCertificateFactory):
    class Meta(object):
        model = models.CourseCertificate

    course_id = factory.Sequence(lambda o: 'course-%d' % o)
    certificate_type = constants.CertificateType.HONOR
    is_active = True


class ProgramCertificateFactory(AbstractCertificateFactory):
    class Meta(object):
        model = models.ProgramCertificate

    is_active = True
    program_id = factory.Sequence(int)
    program_uuid = factory.LazyFunction(uuid.uuid4)


class UserCredentialFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.UserCredential

    credential = factory.SubFactory(ProgramCertificateFactory)
    username = factory.Sequence(lambda o: 'robot%d' % o)
    status = models.UserCredential.AWARDED
    download_url = factory.Faker('url')
    uuid = factory.LazyFunction(uuid.uuid4)


class UserCredentialAttributeFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.UserCredentialAttribute

    user_credential = factory.SubFactory(UserCredentialFactory)
    name = factory.Sequence(lambda o: 'name-%d' % o)
    value = factory.Sequence(lambda o: 'value-%d' % o)


class SignatoryFactory(factory.django.DjangoModelFactory):
    class Meta(object):
        model = models.Signatory

    name = factory.Faker('name')
    title = factory.Faker('job')
