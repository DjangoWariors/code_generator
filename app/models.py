import secrets
import string

from django.db import models


class UniqueCode(models.Model):
    unique_code = models.CharField(max_length=255, unique=True, blank=True, db_index=True)
    brand = models.CharField(max_length=20, blank=True, null=True)
    code_batch = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.unique_code} - {self.brand} - {self.code_batch}"
