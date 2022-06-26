from rest_framework import status, permissions, generics, filters
from rest_framework.response import Response
from drf_app.permissions import IsOwnerOrReadOnly
# from rest_framework.views import APIView
from django.db.models import Count
from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend

from .models import Post
from .serializers import PostSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    serializer_class = PostSerializer
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    filter_backends = [
        filters.OrderingFilter,
        filters.SearchFilter,
        DjangoFilterBackend
    ]

    ordering_fields = [
        'likes_count',	
        'comments_count',	
        'likes__created_at',
    ]

    search_fields = ['owner__username', 'title']

    filterset_fields = [	
        'owner__followed__owner__profile',	
        'likes__owner__profile',	
        'owner__profile',	
    ]
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
    # serializer_class = PostSerializer
    # permission_classes = [
    #     permissions.IsAuthenticatedOrReadOnly
    # ]

    # def get(self, request):

    #     posts = Post.objects.all()
    #     serializer = PostSerializer(
    #         posts, many=True, context={'request': request}
    #     )
    #     return Response(serializer.data)

    # def post(self, request):
    #     serializer = PostSerializer(
    #         data=request.data, context={'request': request}
    #     )

    #     if serializer.is_valid():
    #         serializer.save(owner=request.user)
    #         return Response(
    #             serializer.data, status=status.HTTP_201_CREATED
    #         )

    #     return Response(
    #         serializer.errors, status=status.HTTP_400_BAD_REQUEST
    #     )


class PostDetail(generics.RetrieveDestroyAPIView):

    serializer_class = PostSerializer
    permission_classes = [IsOwnerOrReadOnly]
    queryset = Post.objects.annotate(
        comments_count=Count('comment', distinct=True),
        likes_count=Count('likes', distinct=True),
    ).order_by('-created_at')

    # def get_object(self, pk):
    #     try:
    #         post = Post.objects.get(pk=pk)
    #         self.check_object_permissions(self.request, post)
    #         return post
    #     except Post.DoesNotExist:
    #         raise Http404

    # def get(self, request, pk):
    #     post = self.get_object(pk)
    #     serializer = PostSerializer(post, context={'request': request})
    #     return Response(serializer.data)

    def put(self, request, pk):
        post = self.get_object(pk)
        serializer = PostSerializer(post,
                                    data=request.data,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def delete(self, request, pk):
    #     post = self.get_object(pk)
    #     post.delete()
    #     return Response(
    #         status=status.HTTP_204_NO_CONTENT
    #     )
