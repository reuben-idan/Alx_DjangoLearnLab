from django.db import migrations, models
import taggit.managers

class Migration(migrations.Migration):
    dependencies = [
        ('blog', '0001_initial'),
        ('taggit', '0005_auto_20220424_2025'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='tags',
            field=taggit.managers.TaggableManager(blank=True, help_text='A comma-separated list of tags', through='taggit.TaggedItem', to='taggit.Tag', verbose_name='Tags'),
        ),
    ]
