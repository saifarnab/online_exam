# Generated by Django 3.0.8 on 2020-07-09 13:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth_user', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Paper',
            fields=[
                ('paper_id', models.BigAutoField(primary_key=True, serialize=False)),
                ('paper_name', models.CharField(max_length=500)),
                ('date', models.DateField()),
                ('start_time', models.CharField(max_length=50)),
                ('end_time', models.CharField(max_length=50)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('teacher', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth_user.Profile')),
            ],
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_id', models.BigIntegerField()),
                ('question', models.TextField()),
                ('choice', models.CharField(max_length=50)),
                ('answer', models.CharField(max_length=50)),
                ('paper_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='paper.Paper')),
            ],
        ),
    ]
