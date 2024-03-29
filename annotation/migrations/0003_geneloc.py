# Generated by Django 2.2.5 on 2019-09-18 06:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('annotation', '0002_auto_20190918_1154'),
    ]

    operations = [
        migrations.CreateModel(
            name='GeneLoc',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature', models.CharField(max_length=4)),
                ('seqname', models.CharField(max_length=5)),
                ('start', models.IntegerField()),
                ('end', models.IntegerField()),
                ('strand', models.CharField(max_length=1)),
                ('gene_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='annotation.Gene', verbose_name='Gene-ID')),
                ('tr_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='position', to='annotation.Transcript', verbose_name='Transcript-ID')),
            ],
            options={
                'ordering': ('tr_id', 'feature', 'start', 'end'),
            },
        ),
    ]
