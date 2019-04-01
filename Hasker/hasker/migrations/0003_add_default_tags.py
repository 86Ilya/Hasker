from django.conf import settings
from django.db import migrations


def load_tags_from_sql():
    import os
    from Hasker.settings import BASE_DIR
    sql_statements = open(os.path.join(BASE_DIR, 'Hasker/hasker/sql/create_tags.sql'), 'r').read()
    return sql_statements


def delete_tags_with_sql():
    return 'DELETE from hasker_tag;'


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('hasker', '0002_auto_20190331_1257'),
    ]

    operations = [
        migrations.RunSQL(load_tags_from_sql(), delete_tags_with_sql()),
    ]
