from django.shortcuts import render
from .serializer import taskserializer,userserializer,messageserializer
from rest_framework.pagination import PageNumberPagination 
from .models import tasks,message
from django.contrib.auth.models import User
from rest_framework import generics,permissions
from rest_framework.views import APIView
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from django_filters.rest_framework import DjangoFilterBackend

# Create your views here.
class logoutview(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data['refresh']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response( status=status.HTTP_400_BAD_REQUEST)

class usercreate(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=userserializer
    permission_classes=[permissions.AllowAny]

class listtasks(generics.ListCreateAPIView):
    serializer_class=taskserializer
    permission_classes=[permissions.IsAuthenticated]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['IS_COMPLETED', 'is_important', 'is_due','task_status']
    search_fields = ['title', 'description']
    def get_queryset(self):
        return tasks.objects.filter(user=self.request.user).order_by('-is_due','IS_COMPLETED','-is_important')
    def perform_create(self,serializer): 
        serializer.save(user=self.request.user)

class taskdetail(generics.RetrieveUpdateDestroyAPIView):
    queryset=tasks.objects.all()
    serializer_class=taskserializer
    permission_classes=[permissions.IsAuthenticated]
    lookup= 'id'
    def get_queryset(self):
        return tasks.objects.filter(user=self.request.user)


@api_view(["GET"])
@permission_classes([permissions.IsAuthenticated])
def setduemessage(request):
    user=request.user
    user_tasks=tasks.objects.filter(user=user)
    paginator = PageNumberPagination()
    for task in user_tasks:
        if task.istaskdue():
            new_message=message.objects.create(
                user=user,
                hedder="Task Due Reminder",
                content=f'The task "{task.title}" is due.Please take necessary action'
            )
            print(f'Task "{task.title}" is due.')
    messages=message.objects.filter(user=user).order_by('is_read','-timestamp')
    all_param = request.query_params.get('all')
    if all_param == 'true':
        serializer = messageserializer(messages,many=True)
        print('all is true')
        return Response(serializer.data,status=status.HTTP_200_OK)
    paginated_messages = paginator.paginate_queryset(messages, request)
    serializer = messageserializer(paginated_messages,many=True)
    return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(["patch"])
@permission_classes([permissions.IsAuthenticated])
def markasread(request,id):
    try:
        msg=message.objects.get(id=id)
        msg.is_read=True
        msg.save()
        return Response({"detail":"Message marked as read"},status=status.HTTP_200_OK)
    except message.DoesNotExist:
        return Response({"detail":"Message not found"},status=status.HTTP_404_NOT_FOUND)


@api_view(["patch"])
@permission_classes([permissions.IsAuthenticated])
def markallasread(request):
    user=request.user
    user_messages=message.objects.filter(user=user)
    for msg in user_messages:
        msg.is_read=True
        msg.save()
    return Response({"detail":"All messages marked as read"},status=status.HTTP_200_OK)