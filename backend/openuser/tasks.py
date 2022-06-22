from django.contrib.auth import get_user_model
from . import producers
from . import models
from celery import shared_task
from faker import Faker
import random


# Custom user model
User = get_user_model()

fake = Faker(locale='en_US')
unsplash_random_image = 'https://source.unsplash.com/random/640%C3%97426/?random'


@shared_task
def create_openuserapp(data):

    for _ in range(int(data['profiles'])):
        openuser = User.objects.create(cid=data['uid'], app_name=data['name'])

        openuser.username = fake.unique.user_name()
        openuser.email = fake.unique.email()
        openuser.first_name = fake.first_name()
        openuser.last_name = fake.last_name()
        openuser.other_name = fake.last_name()
        openuser.gender = random.choice(['Male', 'Female'])
        openuser.dob = fake.date_of_birth(minimum_age=18, maximum_age=99)
        openuser.mugshot = unsplash_random_image
        openuser.about = fake.sentence(nb_words=25)

        openuser.set_password(data['profile_password'])
        openuser.save()

    update_creators_openuserapp.delay({'detail': 'created', 'status': 201})


@shared_task
def update_openusercreators(data):
    creator = models.OpenuserCreator.objects.create(cid=data['uid'], username=data['username'])
    creator.save()
    return {'creator': creator.cid, 'status': 'Created successfully'}


@shared_task
def update_creators_openuserapp(data):
    producers.RabbitMQProducer.publish_update_openuserapp(data)
