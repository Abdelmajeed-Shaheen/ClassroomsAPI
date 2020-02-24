from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Classroom
from .forms import ClassroomForm
from rest_framework.generics import ListAPIView, RetrieveAPIView, RetrieveUpdateAPIView, DestroyAPIView, CreateAPIView
from .serializers import ClassroomSerializer , ClassroomDetailsSerializer , ClassroomUpdateSerializer , ClassroomCreateSerializer

def classroom_list(request):
	classrooms = Classroom.objects.all()
	context = {
		"classrooms": classrooms,
	}
	return render(request, 'classroom_list.html', context)


def classroom_detail(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	context = {
		"classroom": classroom,
	}
	return render(request, 'classroom_detail.html', context)


def classroom_create(request):
	form = ClassroomForm()
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Created!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	}
	return render(request, 'create_classroom.html', context)


def classroom_update(request, classroom_id):
	classroom = Classroom.objects.get(id=classroom_id)
	form = ClassroomForm(instance=classroom)
	if request.method == "POST":
		form = ClassroomForm(request.POST, request.FILES or None, instance=classroom)
		if form.is_valid():
			form.save()
			messages.success(request, "Successfully Edited!")
			return redirect('classroom-list')
		print (form.errors)
	context = {
	"form": form,
	"classroom": classroom,
	}
	return render(request, 'update_classroom.html', context)


def classroom_delete(request, classroom_id):
	Classroom.objects.get(id=classroom_id).delete()
	messages.success(request, "Successfully Deleted!")
	return redirect('classroom-list')


class ClassroomAPIList(ListAPIView):
	queryset = Classroom.objects.all()
	serializer_class = ClassroomSerializer


class ClassroomAPIDetails(RetrieveAPIView):
	queryset = Classroom.objects.all()
	serializer_class = ClassroomDetailsSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'classroom_id'

class ClassroomAPIUpdate(RetrieveUpdateAPIView):
	queryset = Classroom.objects.all()
	serializer_class = ClassroomUpdateSerializer
	lookup_field = 'id'
	lookup_url_kwarg = 'classroom_id'


class DeleteClassroom(DestroyAPIView):
	queryset = Classroom.objects.all()
	lookup_field = 'id'
	lookup_url_kwarg = 'classroom_id'


class ClassroomCreateAPI(CreateAPIView):
	serializer_class = ClassroomCreateSerializer

	def perform_create(self, serializer):
		if self.request.user.is_authenticated:
			serializer.save(teacher=self.request.user)
