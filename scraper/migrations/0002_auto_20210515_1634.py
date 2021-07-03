# Generated by Django 3.0.3 on 2021-05-15 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('scraper', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='totalmodel',
            name='market',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='newtotal', to='scraper.MarketModel'),
        ),
        migrations.CreateModel(
            name='NewTotalModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_listings', models.IntegerField(blank=True, default=0, null=True)),
                ('total_value', models.BigIntegerField(blank=True, default=0, null=True)),
                ('total_sqm', models.IntegerField(blank=True, default=0, null=True)),
                ('market', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='total', to='scraper.MarketModel')),
            ],
        ),
    ]