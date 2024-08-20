# Generated by Django 5.1 on 2024-08-14 20:22

import uuid
import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_app', '0004_alter_ticket_user_assigned'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Ticket'
        ),
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100)),
                ('user_create', models.IntegerField()),
                ('category', models.UUIDField()),
                ('severity', models.IntegerField()),
                ('description', models.CharField(max_length=1024)),
                ('created_at', models.DateTimeField(default=datetime.datetime.now)),
                ('updated_at', models.DateTimeField(null=True)),
                ('user_assigned', models.IntegerField()),
                ('status', models.CharField(max_length=40)),
            ],
            options={
                'db_table': 'tickets',
            },
        ),
        # migrations.AlterField(
        #     model_name='ticket',
        #     name='user_assigned',
        #     field=models.IntegerField(null=True),
        # ),
        # migrations.AlterField(
        #     model_name='ticket',
        #     name='user_create',
        #     field=models.IntegerField(),
        # ),
    ]
