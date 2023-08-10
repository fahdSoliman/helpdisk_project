from django.db import models



class Botpress(models.Model):
    postgresql = 'postgresql'
    sqlite = 'sqlite'
    db_type_list = [(postgresql, 'postgresql'),
                    (sqlite, 'sqlite')]
    

    botpress_base_url = models.URLField(null=True, max_length=200)
    db_url = models.CharField(null=True, max_length=200)
    db_type = models.CharField(choices=db_type_list, default=sqlite, max_length=15)
    db_name = models.CharField(null=True, max_length=200)
    db_username = models.CharField(null=True, max_length=200)
    db_password = models.CharField(null=True, max_length=200)




