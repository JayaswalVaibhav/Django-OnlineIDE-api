from django.shortcuts import render
from django.http import HttpResponse
from rest_framework.viewsets import ModelViewSet
from .serializers import UserSerializer, SubmissionCodeSerializer
from .models import SubmissionCode
# Create your views here.
from .utils import create_code_file, execute_file
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from rest_framework import permissions
from django.contrib.auth.models import User
from django.contrib.auth import login
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from multiprocessing import Process


def hello_world(request):
    return HttpResponse("Welcome to online IDE")

# removed becasue we are using knox
# class UserViewSet(ModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


@api_view(http_method_names=["POST"])
@permission_classes((permissions.AllowAny,))
def register(request):
    serializer = UserSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = serializer.save()
    return Response(UserSerializer(user).data, status=201)


class LoginView(KnoxLoginView):
    permission_classes = (permissions.AllowAny,)

    def post(self, request, format=None):
        serializer = AuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        login(request, user)
        return super(LoginView, self).post(request, format=None)


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticated,)
    queryset = User.objects.all()

    def list(self, request, *args, **kwargs):
        return Response(UserSerializer(request.user).data, status=200)


class SubmissionCodeViewSet(ModelViewSet):
    queryset = SubmissionCode.objects.all()
    serializer_class = SubmissionCodeSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        queryset = queryset.filter(user=request.user)
        return Response(self.get_serializer(queryset, many=True).data, status=200)

    def create(self, request, *args, **kwargs):
        request.data['status'] = "P"
        request.data["user"] = request.user.pk
        file_name = create_code_file(request.data.get('code'), request.data.get('language'))

        # the below one is a blocking code -- wait for the execute to complete
        # request will timeout if you infinite loop
        # problem with this -- it is holding other request

        # we will use the concepts of multiprocessing
        serializer = SubmissionCodeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission = serializer.save()

        p = Process(target=execute_file, args=(file_name, request.data.get('language'), submission.pk))
        p.start() # start in a new process and there it will execute

        # request.data['user_output'] = output
        # return super().create(request, args, kwargs)
        return Response({
            "Message": "Successfully submitted"
        }, status=200)
