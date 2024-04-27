# Generated by Django 4.2.6 on 2024-04-26 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_alter_classes_classfee'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='students',
            name='is_finished',
        ),
        migrations.RemoveField(
            model_name='students',
            name='is_received',
        ),
        migrations.AddField(
            model_name='students',
            name='Gender',
            field=models.CharField(blank=True, choices=[(' ', 'Chooces Gender'), ('Male', 'Male'), ('Female', 'Female')], max_length=50, null=True, verbose_name='Student Gender'),
        ),
        migrations.AddField(
            model_name='students',
            name='StudentLocation',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Student Location'),
        ),
    ]