from rest_framework import viewsets
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.blog.models import Category, Blog, Comment
from apps.blog.serializers import CategorySerializer, BlogSerializer, CommentSerializer
from apps.common.permissions import ReadOnly


# Create your views here.
class CategoryViewSet(viewsets.ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()


class BlogListView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        blogs = Blog.objects.all()
        return Response(BlogSerializer(blogs, many=True).data)
    
    def post(self,request):
        validated_data = request.serializer.validated_data

        # Create blog
        blog = Blog.objects.create(
            **validated_data
        )

        blog.save()

        return Response(BlogSerializer(blog).data)


class BlogItemView(GenericAPIView):
    serializer_class = BlogSerializer
    permission_classes = (ReadOnly,)

    def get(self, request, pk):
        blog_post = get_object_or_404(Blog.objects.filter(pk=pk))

        comments=Comment.objects.get(blog=pk)

        return Response(BlogSerializer(blog_post).data)
    

class CommentViewSet(viewsets.ModelViewSet):
    serializer_class=CommentSerializer
    queryset = Comment.objects.all()

    def post(blog_id, text):
        
        # Create comment
        comment = Comment.objects.create(
           blog=blog_id,
           text=text
        )

        comment.save()

        return Response(CommentSerializer(comment).data)



