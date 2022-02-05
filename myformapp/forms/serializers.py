from datetime import datetime, timedelta
from rest_framework import serializers
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import PermissionDenied

from .models import *

class QuestionSerializer(serializers.ModelSerializer):
	options = serializers.SerializerMethodField()
	def get_options(self, obj):
		if obj.options:
			return obj.options.split(",")
		return obj.options
	class Meta:
		model = Questions
		fields = ["id", 'field_name', 'field_type', 'options', 'mandatory']

class DetailFormViewSerializer(serializers.ModelSerializer):
	questions = serializers.SerializerMethodField()
	def get_questions(self, obj):
		questions_instance = Questions.objects.filter(form=obj)
		return QuestionSerializer(questions_instance, many=True).data
	class Meta:
		model = Form
		fields = "__all__"

class AnsweresSerializer(serializers.ModelSerializer):
	question = QuestionSerializer()
	class Meta:
		model = Answeres
		fields = "__all__"

class SaveResponseFormSerializer(serializers.ModelSerializer):
	class Meta:
		model = ResponseForm
		fields = "__all__"

	def create(self, validation_data):
		response_form = ResponseForm.objects.create(form=validation_data.pop("form"))
		request = self.context.get("request").data
		answeres = request['answeres']
		for ans in answeres:
			question = Questions.objects.get(id=ans['question'])
			answere = Answeres.objects.create(response=response_form, question=question, ans=ans['ans'])
		return response_form

class ResponseListViewSerializer(serializers.ModelSerializer):
	answeres = serializers.SerializerMethodField()
	def get_answeres(self, obj):
		answeres = Answeres.objects.filter(response=obj)
		return AnsweresSerializer(answeres, many=True).data
	class Meta:
		model = ResponseForm
		fields = "__all__"