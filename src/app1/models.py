from django.db import models

# Create your models here.

class ProductRecordLog(models.Model):
    id = models.AutoField(primary_key=True, db_column='ID')
    unit_id = models.IntegerField(db_column='UnitID', null=True, blank=True)
    unit_name = models.CharField(db_column='UnitName', max_length=255, null=True, blank=True)
    product_barkod_no = models.CharField(db_column='ProductBarkodNo', max_length=200, null=True, blank=True)
    is_emri_no = models.CharField(db_column='IsEmriNo', max_length=200, null=True, blank=True)
    model = models.CharField(db_column='Model', max_length=200, null=True, blank=True)
    model_aciklamasi = models.CharField(db_column='ModelAciklamasi', max_length=500, null=True, blank=True)
    test_sonucu = models.IntegerField(db_column='TestSonucu', null=True, blank=True)
    kayit_tarihi = models.DateTimeField(db_column='KayitTarihi', null=True, blank=True)
    model_suresi_sn = models.IntegerField(db_column='ModelSuresiSN', null=True, blank=True)

    class Meta:
        managed = False  # Since this is an existing table in the database
        db_table = 'ProductRecordLog'

    def __str__(self):
        return f"{self.unit_name} - {self.model} - {self.kayit_tarihi}"
