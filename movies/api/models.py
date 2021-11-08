from django.db import models


class Director(models.Model):
    name=models.CharField(max_length= 32,unique=True)
    surname = models.CharField(max_length=32)

    def __str__(self):
        return self.name + self.surname

class Movie(models.Model):
    title = models.CharField(max_length= 32)
    year= models.IntegerField(default= 2000)
    director=models.ForeignKey(Director,on_delete=models.PROTECT,blank=True,null=True)

    def __str__(self):
        return self.title + str(self.year)




