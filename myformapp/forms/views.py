from datetime import datetime, timedelta
from rest_framework import generics
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, CreateAPIView, \
    RetrieveUpdateAPIView
import numpy as np
import pandas as pd
from .models import *
from .serializers import *
# Create your views here.


class CreateForm(APIView):
	def post(self, request, *args, **kwargs):
		name = request.data.get("form_name")
		file=request.FILES['file']
		f = pd.read_csv(file)

		for index, data in f.iterrows():
			if pd.isna(data['type']) or data['type'] not in ['text', 'date', 'number', 'singleSelect']:
				return Response({"msg": "type should be either 'text', 'date', 'number', 'singleSelect'", "error": True}, status=status.HTTP_400_BAD_REQUEST)
			if data['type'] == "singleSelect":
				if data['options'] in ["", None] or pd.isna(data['options']):
					return Response({"msg": "options should be there in case of singleSelect type", "error": True}, status=status.HTTP_400_BAD_REQUEST)
			if pd.isna(data['mandatory']) or data['mandatory'] not in [True, False]:
				return Response({"msg": "mandatory is not blank it should be either True or False", "error": True}, status=status.HTTP_400_BAD_REQUEST)
			if pd.isna(data['field_name']):
				return Response({"msg": "field_name is not blank", "error": True}, status=status.HTTP_400_BAD_REQUEST)

		form = Form.objects.create(name = name)
		for index, data in f.iterrows():
			options = data['options'] if pd.isna(data['options']) == False else None
			q = Questions.objects.create(form=form, field_name=data['field_name'], field_type=data['type'], options=options, mandatory=data['mandatory'])
		return Response({"msg": "Created Success", "error": False, "uuid": form.uuid}, status=status.HTTP_201_CREATED)

class GetFormData(RetrieveAPIView):
	queryset = Form.objects.all()
	serializer_class = DetailFormViewSerializer
	pagination_class = None
	lookup_field = "uuid"

class SaveResponseForm(CreateAPIView):
	queryset = ResponseForm.objects.all()
	serializer_class = SaveResponseFormSerializer
	lookup_field = "uuid"

	def create(self, request, uuid, *args, **kwargs):
		try:
			form = Form.objects.get(uuid = uuid)
		except:
			return Response({"msg": "Invalid form id"}, status = status.HTTP_400_BAD_REQUEST)
		for ans in request.data.get("answeres"):
			try:
				question = Questions.objects.get(id=ans['question'])
			except:
				return Response({"msg": "Invalid question id", "error": True}, status=status.HTTP_400_BAD_REQUEST)
			if question.field_type == "singleSelect" and ans['ans'] not in question.options.split(","):
				return Response({"msg": "invalid ans it should be in {}".split(question.options.split(",")), "error": True}, status=status.HTTP_400_BAD_REQUEST)
		data = request.data.copy()
		data['form'] = form.id
		serializer = self.get_serializer(data=data)
		serializer.is_valid(raise_exception=True)
		self.perform_create(serializer)
		return Response(serializer.data, status=status.HTTP_201_CREATED)

class ResponseListView(ListAPIView):
	queryset = ResponseForm.objects.filter()
	serializer_class = ResponseListViewSerializer
	lookup_field = "uuid"

	def get_queryset(self, *args, **kwargs):
		return ResponseForm.objects.filter(form__uuid=self.uuid)
	def list(self, request, uuid, *args, **kwargs):
		self.uuid = uuid
		return super().list(request, *args, **kwargs)

class ResponseDetailView(APIView):
	def get(self, request, id, *args, **kwargs):
		queryset = ResponseForm.objects.get(id=id)
		serializer = ResponseListViewSerializer(queryset)
		response = {"response": serializer.data, "error": False}
		return Response(response)