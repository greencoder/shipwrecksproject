# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('wrecks', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='wreck',
            old_name='source_id',
            new_name='source_identifier',
        ),
    ]
