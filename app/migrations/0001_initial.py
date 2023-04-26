# Generated by Django 3.2.18 on 2023-04-26 12:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('userauth', '0004_auto_20230426_1322'),
    ]

    operations = [
        migrations.CreateModel(
            name='ClassRoom',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
            ],
            options={
                'verbose_name_plural': 'Student Class',
            },
        ),
        migrations.CreateModel(
            name='Subjects',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256)),
                ('class_offered', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='app.classroom')),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='userauth.teacher')),
            ],
            options={
                'verbose_name_plural': 'Subjects',
            },
        ),
    ]