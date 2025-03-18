from django.core.serializers import serialize
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication

from polls.models import Task
from polls.pagination import TaskPagination
from polls.scheduler import TaskScheduler
from polls.serializers import TaskSerializer

from rest_framework.filters import OrderingFilter
from django.core.cache import caches

# in-memory global cache
cache = caches['default']  # Explicitly initialize cache

class Home(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        content = {'message': "Hello, world. You're at the polls index."}
        return Response(content)

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    pagination_class = TaskPagination
    filter_backends = [OrderingFilter]
    ordering_fields = ['priority', 'timestamp']

    def get_queryset(self):
        user = self.request.user
        priority = self.request.query_params.get('priority')
        status = self.request.query_params.get('status')
        queryset = Task.objects.filter(user=user)

        if priority:
            queryset = queryset.filter(priority=priority)
        if status:
            queryset = queryset.filter(status=status)

        return queryset

    def retrieve(self, request, pk=None):
        user_id = request.user.id
        cache_key = f'task_{user_id}_{pk}'
        task = cache.get(cache_key)
        if not task:
            print("Cache miss for key: " + cache_key)
            task = Task.objects.get(id=pk, user=request.user)
            cache.set(cache_key, task, timeout=60)
        else:
            print("Cache hit for key: " + cache_key)
        serializer = self.get_serializer(task)
        return Response(serializer.data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def perform_update(self, serializer):
        user = self.request.user
        serializer.save(user=user)

    def perform_destroy(self, instance):
        user_id = instance.user.id
        task_id = instance.id
        cache_key = f'task_{user_id}_{task_id}'
        cache.delete(cache_key)
        instance.delete()

    @action(detail=False, methods=['get'], url_path='next_tasks')
    def next_tasks(self, request, *args, **kwargs):
        task_scheduler = TaskScheduler(user_id=request.user.id)
        next_tasks = task_scheduler.get_next_tasks()
        serializer = self.get_serializer(next_tasks, many=True)
        return Response(serializer.data)
