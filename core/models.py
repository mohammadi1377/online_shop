from django.db import models
from jalali_date import date2jalali,datetime2jalali


class BaseModel(models.Model):
<<<<<<< HEAD
	is_deleted = models.BooleanField(default=False)
=======
>>>>>>> develop
	created_at = models.DateTimeField(auto_now_add=True, verbose_name="Created Date")
	updated_at = models.DateTimeField(auto_now=True, verbose_name="Updated Date")

	def get_jalai_date(self):
<<<<<<< HEAD
		return datetime2jalali(self.created_at), datetime2jalali(self.updated_at)
=======
		return date2jalali(self.created_at)

	get_jalai_short_description = "تاریخ شمسی"
>>>>>>> develop

	class Meta:
		abstract = True






