from __future__ import absolute_import, unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from .producers import RabbitMQProducer
from .models import OpenuserCreator
from django.db import transaction
from src.celery import app
from faker import Faker
import random


# Custom user model
User = get_user_model()

# Faker data
unsplash_random_image = 'https://source.unsplash.com/random/640%C3%97426/?random'
fake = Faker(locale='en_US')
Faker.seed(0)

# others
domain = Site.objects.get_current().domain


@app.task
def new_openusercreator(data):
    """
    Celery task to create a new openusercreator
    """
    creator = OpenuserCreator.objects.create(cid=data['uid'], username=data['username'])
    creator.save()
    return {'creator': creator.cid, 'status': 'Created successfully'}


@app.task
def delete_openusercreator(data):
    """
    Celery task to delete an openusercreator from the system permanently
    """
    try:
        creator = OpenuserCreator.objects.get(cid=data['uid'])
    except OpenuserCreator.DoesNotExist:
        return {'Creator': data['uid'], 'detail': 'Does no exist'}
    else:
        creator.delete()
        return {'Creator': data['uid'], 'detail': 'Deleted successfully'}


@app.task
@transaction.atomic
def new_openuserapp(data):
    """
    Celery task to create new openuserapp profiles for the provided
    creator and app name instance.
    """
    for _ in range(int(data['profiles'])):
        openuser = User.objects.create(
            cid=data['uid'],
            app_name=data['name'],
            username=fake.unique.user_name(),
            email=fake.unique.email(),
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            other_name=fake.last_name(),
            gender=random.choice(['Male', 'Female']),
            dob=fake.date_of_birth(minimum_age=18, maximum_age=99),
            mugshot=unsplash_random_image,
            about=fake.sentence(nb_words=25)
        )

        openuser.set_password(data['profile_password'])
        openuser.save()

    # wait for a successful creation of all profiles, then execute this celery task
    transaction.on_commit(
        lambda: update_creators_openuserapp.delay(data={
            'cid': data['uid'],
            'name': data['name'],
            'status': 'Created',
            'endpoint': F"{domain}/{data['uid']}/{data['name']}/api/<version>/"
        })
    )
    return {'App name': data['name'], 'Profiles': data['profiles'], 'status': 'Created successfully'}


@app.task
def delete_openuserapp(data):
    """
    Celery task to delete a creators openuserapp instance, along with all
    profiles.
    """
    openuser = User.objects.filter(cid=data['uid'], app_name=data['name'])
    profiles = openuser.count()
    openuser.delete()

    return {
        'Creator id': data['uid'],
        'App name': data['name'],
        'Profiles': profiles,
        'status': 'Deleted successfully'
    }


@app.task
def update_creators_openuserapp(data):
    """
    Celery task that executes a method to publish an update message to our
    message broker concerning the newly created openuserapp.
    """
    RabbitMQProducer().publish_update_openuserapp(data)
