# Generated by Django 3.0 on 2023-05-12 17:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]


    # operations = [
    #     migrations.RunSQL("""
    #     INSERT INTO profiles_profile(
    #         id,
    #         favorite_city,
    #         user_id
    #     )
    #     SELECT
    #         id,
    #         favorite_city,
    #         user_id
    #     FROM
    #         oc_lettings_site_profile;
    #     """, reverse_sql="""
    #     INSERT INTO oc_lettings_site_profile(
    #         id,
    #         favorite_city,
    #         user_id
    #     )
    #     SELECT
    #         id,
    #         favorite_city,
    #         user_id
    #     FROM
    #         profiles_profile;
    #     """)
    # ]
