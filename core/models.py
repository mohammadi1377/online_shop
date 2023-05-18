from django.db import models
from jalali_date import date2jalali,datetime2jalali


class BaseModel(models.Model):
	is_deleted = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

	def get_jalai_date(self):
		return datetime2jalali(self.created_at), datetime2jalali(self.updated_at)

	class Meta:
		abstract = True






