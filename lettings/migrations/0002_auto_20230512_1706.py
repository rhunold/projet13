# Generated by Django 3.0 on 2023-05-12 17:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('lettings', '0001_initial'),
    ]

    # operations = [
    #     migrations.RunSQL("""
    #     INSERT INTO lettings_address(
    #         id,
    #         number,
    #         street,
    #         city,
    #         state,
    #         zip_code,
    #         country_iso_code
    #     )
    #     SELECT
    #         id,
    #         number,
    #         street,
    #         city,
    #         state,
    #         zip_code,
    #         country_iso_code
    #     FROM
    #         oc_lettings_site_address;
    #     INSERT INTO lettings_letting(
    #         id,
    #         title,
    #         address_id
    #     )
    #     SELECT
    #         id,
    #         title,
    #         address_id
    #     FROM
    #         oc_lettings_site_letting;
    #     """, reverse_sql="""
    #     INSERT INTO oc_lettings_site_address(
    #         id,
    #         number,
    #         street,
    #         city,
    #         state,
    #         zip_code,
    #         country_iso_code
    #     )
    #     SELECT
    #         id,
    #         number,
    #         street,
    #         city,
    #         state,
    #         zip_code,
    #         country_iso_code
    #     FROM
    #         lettings_address;
    #     INSERT INTO oc_lettings_site_letting(
    #         id,
    #         title,
    #         address_id
    #     )
    #     SELECT
    #         id,
    #         title,
    #         address_id
    #     FROM
    #         lettings_letting;
    #     """)
    # ]