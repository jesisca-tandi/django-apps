from django.db import models

# Create your models here.

class Item(models.Model):
	i_id 		= models.IntegerField(primary_key=True)
	i_im_id 	= models.CharField(unique=True, max_length=8)
	i_name		= models.CharField(max_length=50)
	i_price 	= models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		managed 	= False
		db_table 	= 'item'

class Stock(models.Model):
	w 	= models.ForeignKey('Warehouse', models.DO_NOTHING, primary_key=True)
	i 	= models.ForeignKey(Item, models.DO_NOTHING)
	s_qty 	= models.SmallIntegerField()

	class Meta:
		managed 	= False
		db_table 	= 'stock'
		unique_together	= (('w', 'i'),)


class Warehouse(models.Model):
	w_id 		= models.IntegerField(primary_key=True)
	w_name 		= models.CharField(max_length=50, blank=True, null=True)
	w_street 	= models.CharField(max_length=50, blank=True, null=True)
	w_city 		= models.CharField(max_length=50, blank=True, null=True)
	w_country 	= models.CharField(max_length=50, blank=True, null=True)

	class Meta:
		managed 	= False
		db_table 	= 'warehouse'




