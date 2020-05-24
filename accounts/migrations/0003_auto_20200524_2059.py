# Generated by Django 2.1.15 on 2020-05-24 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0002_auto_20200520_1726'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='favorites',
        ),
        migrations.AddField(
            model_name='user',
            name='favorite',
            field=models.CharField(choices=[('Adventure', 'Adventure'), ('Fantasy', 'Fantasy'), ('Animation', 'Animation'), ('Drama', 'Drama'), ('Horror', 'Horror'), ('Action', 'Action'), ('Comedy', 'Comedy'), ('History', 'History'), ('Western', 'Western'), ('Thriller', 'Thriller'), ('Crime', 'Crime'), ('Documentary', 'Documentary'), ('Science Fiction', 'Science Fiction'), ('Mystery', 'Mystery'), ('Music', 'Music'), ('Romance', 'Romance'), ('Family', 'Family'), ('War', 'War'), ('TV Movie', 'TV Movie')], default='Comedy', max_length=20),
            preserve_default=False,
        ),
    ]
