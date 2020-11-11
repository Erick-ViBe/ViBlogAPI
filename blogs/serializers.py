from rest_framework import serializers

from blogs.models import Tag, Blog, Comment


class TagSerializer(serializers.ModelSerializer):
    """Serializer for Tag objects"""

    class Meta:
        model = Tag
        fields = ('id', 'content')
        read_only_fields = ('id',)


class BlogSerializer(serializers.ModelSerializer):
    """Serializer for Blog objects"""
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Blog
        exclude = ['updated_at', 'likes']
        read_only_fields = ['id', 'author']

    def get_created_at(self, instance):
        """Return correctly date format"""
        return instance.created_at.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        """Return the blog's like count"""
        return instance.likes.count()

    def get_user_has_liked(self, instance):
        """Return if user has liked the blog or not"""
        request = self.context.get("request")
        return instance.likes.filter(pk=request.user.pk).exists()


class MyBlogSerializer(serializers.ModelSerializer):
    """Serializer for retrieve only user blogs"""
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    slug = serializers.SlugField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    tags = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=Tag.objects.all()
    )

    class Meta:
        model = Blog
        exclude = ['updated_at', 'likes']
        read_only_fields = ['id', 'author']

    def get_created_at(self, instance):
        """Return correctly date format"""
        return instance.created_at.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        """Return the blog's like count"""
        return instance.likes.count()


class CommentSerializer(serializers.ModelSerializer):
    """Serializer for blog comments"""
    author = serializers.StringRelatedField()
    created_at = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()
    user_has_liked = serializers.SerializerMethodField()
    blog_slug = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        exclude = ['updated_at', 'likes', 'blog']
        read_only_fields = ['id', 'author']

    def get_created_at(self, instance):
        """Return correctly date format"""
        return instance.created_at.strftime("%B %d, %Y")

    def get_likes_count(self, instance):
        """Return the blog's like count"""
        return instance.likes.count()

    def get_user_has_liked(self, instance):
        """Return if user has liked the blog or not"""
        request = self.context.get("request")
        return instance.likes.filter(pk=request.user.pk).exists()

    def get_blog_slug(self, instance):
        """Return slug blog"""
        return instance.blog.slug
