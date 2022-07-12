from __future__ import absolute_import, unicode_literals
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
# from .pika_producers import RabbitMQProducer
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

# Get current site url
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
            aid=data['id'],
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

    return {'App name': data['name'], 'status': F'{data["profiles"]} profiles created successfully'}


@app.task
@transaction.atomic
def update_openuserapp(data):
    current_openuser = User.objects.filter(cid=data['uid'], aid=data['id'])

    # datas to update
    new_app_name: str = data.get('name', None)
    new_profiles: int = data.get('profiles', current_openuser.count())
    new_profile_password: int = data.get('profile_password', None)

    if (new_profile_password) and (not current_openuser[0].check_password(new_profile_password)):
        for _ in current_openuser:
            _.set_password(new_profile_password)
            _.save()
        return {'Creator': data['uid'], "App ID": data['id'], 'Detail': 'Updated openuser password'}

    if (new_app_name) and (new_app_name != current_openuser[0].app_name):
        for _ in current_openuser:
            _.app_name = new_app_name
            _.save()
        return {'Creator': data['uid'], "App ID": data['id'], 'Detail': 'Updated openuser app name'}

    if int(new_profiles) > int(current_openuser.count()):
        # if the number of new profiles is more than the current profiles, then
        # perform a create operation for the specied number more than the initial.
        profiles: int = int(new_profiles) - int(current_openuser.count())

        for _ in range(profiles):
            new_openuser = User.objects.create(
                cid=data['uid'],
                app_name=data['name'],
                aid=data['id'],
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

            new_openuser.set_password(data['profile_password'])
            new_openuser.save()

        return {'Creator': data['uid'], "App ID": data['id'], 'Detail': F'Created {profiles} more openuser profiles'}

    if int(new_profiles) < current_openuser.count():
        # if the number of new profiles is less than the current profiles,
        # then perform a delete operation for the specied numbers less than
        # the initial.
        profiles: int = int(current_openuser.count()) - int(new_profiles)

        for _ in current_openuser[:profiles]:
            _.delete()
        return {'Creator': data['uid'], "App ID": data['id'], 'Detail': F'Deleted {profiles} openusers profile'}

    else:
        return {'Creator': data['uid'], "App ID": data['id'], 'Status': 'Error no openusers found'}


@app.task
def delete_openuserapp(data):
    """
    Celery task to delete a creators openuserapp instance, along with all
    profiles.
    """
    openuser = User.objects.filter(cid=data['uid'], aid=data['id'])
    profiles = openuser.count()
    openuser.delete()

    return {
        'Creator id': data['uid'],
        'App id': data['id'],
        'status': F'{profiles} Deleted successfully'
    }


# @app.task
# def activate_creators_openuserapp(data):
#     """
#     Celery task that executes a method to publish an update message to our
#     message broker concerning the newly created openuserapp.
#     """
#     RabbitMQProducer().publish_activate_openuserapp(data)
