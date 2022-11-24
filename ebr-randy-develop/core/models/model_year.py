from django.db import models
# from . import Review

class ModelYear(models.Model):
    year = models.PositiveIntegerField(null=True, blank=True)
    
    create_at = models.DateField(auto_now_add=True)
    update_at = models.DateField(auto_now=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return str(self.year)

    class Meta:
	    db_table = "model_year_changes"