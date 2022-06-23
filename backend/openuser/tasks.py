from __future__ import absolute_import, unicode_literals
from django.contrib.auth import get_user_model
from .producers import RabbitMQProducer
from .models import OpenuserCreator
from src.celery import app
from faker import Faker
import random


# Custom user model
User = get_user_model()

# Faker data
fake = Faker(locale='en_US')
Faker.seed(0)
unsplash_random_image = 'https://source.unsplash.com/random/640%C3%97426/?random'


@app.task
def create_openuserapp(data):

    for _ in range(int(data['profiles'])):
        openuser = User.objects.create(
            cid=data['creator'],
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

    return {'App name': data['name'], 'Profiles': data['profiles'], 'status': 'Created successfully'}
    # update_creators_openuserapp.delay({'detail': 'created', 'status': 201})


@app.task
def update_openusercreators(data):
    creator = OpenuserCreator.objects.create(cid=data['uid'], username=data['username'])
    creator.save()
    return {'creator': creator.cid, 'status': 'Created successfully'}


@app.task
def update_creators_openuserapp(data):
    RabbitMQProducer.publish_update_openuserapp(data)
