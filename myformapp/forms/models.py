from django.db import models
from myformapp.users.models import User
import uuid as uuid

class Form(models.Model):
	uuid = models.UUIDField(default=uuid.uuid4, editable=False)
	created_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	name = models.CharField(max_length=200, blank=True, null=True)

class Questions(models.Model):
	field_name = models.CharField(max_length=200, blank=True, null=True)
	FIELD_TYPES = (
			("text", "text"),
			("date", "date"),
			("number", "number"),
			("singleSelect", "singleSelect"),
		)
	field_type = models.CharField(max_length=20, choices=FIELD_TYPES, blank=False, null=False)
	options = models.CharField(max_length=200, blank=True, null=True)
	mandatory = models.BooleanField(default=False)
	form = models.ForeignKey(Form, null=False, blank=False, on_delete=models.CASCADE)

class ResponseForm(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	form = models.ForeignKey(Form, null=False, blank=False, on_delete=models.CASCADE)

class Answeres(models.Model):
	response = models.ForeignKey(ResponseForm, null=False, blank=False, on_delete=models.CASCADE)
	question = models.ForeignKey(Questions, null=False, blank=False, on_delete=models.CASCADE)
	ans = models.TextField()
	