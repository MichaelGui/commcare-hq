# Generated by Django 2.2.13 on 2020-09-24 17:53

from django.db import migrations, models

OLD_NAME = "fp_casetrans_formid_05e599_idx"
NEW_NAME = "form_proces_form_id_f2403a_idx"


class Migration(migrations.Migration):

    dependencies = [
        ('form_processor', '0091_auto_20190603_2023'),
    ]

    operations = [
        migrations.RunSQL(
            f"ALTER INDEX {OLD_NAME} RENAME TO {NEW_NAME}",
            f"ALTER INDEX {NEW_NAME} RENAME TO {OLD_NAME}",
            state_operations=[
                migrations.RemoveIndex(
                    model_name='casetransaction',
                    name=OLD_NAME,
                ),
                migrations.AddIndex(
                    model_name='casetransaction',
                    index=models.Index(fields=['form_id'], name=NEW_NAME),
                ),
            ]
        )
    ]
