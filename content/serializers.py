from rest_framework import serializers

from content.models import PostImage, Post


class PostImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImage
        fields = ("id", "post", "image")


class PostSerializer(serializers.ModelSerializer):
    images = PostImageSerializer(many=True, read_only=True)
    uploaded_images = serializers.ListField(
        child=serializers.ImageField(allow_empty_file=False, use_url=False),
        write_only=True,
        required=False,
    )
    created_at = serializers.DateTimeField(read_only=True)
    liked_by = serializers.SlugRelatedField(
        read_only=True, many=True, slug_field="full_name"
    )

    class Meta:
        model = Post
        fields = (
            "id",
            "content",
            "created_at",
            "liked_by",
            "hashtags",
            "images",
            "uploaded_images",
        )

    def create(self, validated_data):
        uploaded_images = validated_data.pop("uploaded_images", None)
        liked_by_data = validated_data.pop("liked_by", [])

        post = Post.objects.create(**validated_data)

        if uploaded_images:
            for image in uploaded_images:
                PostImage.objects.create(post=post, image=image)

        post.liked_by.set(liked_by_data)

        return post


class PostListSerializer(PostSerializer):
    likes_count = serializers.IntegerField(
        source="liked_by.count", read_only=True
    )
    owner = serializers.CharField(read_only=True, source="owner.full_name")

    class Meta:
        model = Post
        fields = (
            "id",
            "owner",
            "content",
            "created_at",
            "liked_by",
            "likes_count",
            "hashtags",
            "images",
        )
