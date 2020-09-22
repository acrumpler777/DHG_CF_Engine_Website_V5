from django.db import models

# Create your models here.
class fileUpload(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    #add a user upload field later
    filetxt = models.FileField(upload_to='', unique=True)
    calculated_file = models.FileField(upload_to='', blank=True)
    sum_file = models.FileField(upload_to='', blank=True)

    def __str__(self):
        return self.filetxt.url

    def delete(self, *args, **kwargs):
        self.filetxt.delete()
        self.calculated_file.delete()
        self.sum_file.delete()
        super().delete(*args, **kwargs)
