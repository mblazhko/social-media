from datetime import datetime

from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from content.models import Post, Hashtag
from content.serializers import PostListSerializer, PostSerializer

POST_URL = reverse("content:post-list")


def sample_post(user, **params) -> Post:
    defaults = {
        "owner": user,
        "content": "test content",
    }
    defaults.update(params)
    return Post.objects.create(**defaults)


def detail_url(id, api_name):
    return reverse(f"content:{api_name}-detail", args=[id])


class AuthenticatedPostApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = get_user_model().objects.create_user(
            email="user1@test.com",
            first_name="User1_first",
            last_name="User1_last",
            password="testpassword",
        )
        self.user2 = get_user_model().objects.create_user(
            email="user2@test.com",
            first_name="User2_first",
            last_name="User2_last",
            password="testpassword",
        )
        self.client.force_authenticate(self.user1)

    def test_list_post(self):
        sample_post(user=self.user1)
        res = self.client.get(POST_URL)

        post = Post.objects.all()
        serializer = PostListSerializer(post, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_filter_by_first_name(self):
        post1 = sample_post(user=self.user1)
        post2 = sample_post(user=self.user2)

        res1 = self.client.get(POST_URL, {"first_name": "User1_first"})

        serializer1 = PostListSerializer(post1)
        serializer2 = PostListSerializer(post2)

        self.assertIn(serializer1.data, res1.data)
        self.assertNotIn(serializer2.data, res1.data)

    def test_filter_by_last_name(self):
        post1 = sample_post(user=self.user1)
        post2 = sample_post(user=self.user2)

        res1 = self.client.get(POST_URL, {"last_name": "User1_last"})

        serializer1 = PostListSerializer(post1)
        serializer2 = PostListSerializer(post2)

        self.assertIn(serializer1.data, res1.data)
        self.assertNotIn(serializer2.data, res1.data)

    def test_filter_by_created_date(self):
        post1 = sample_post(user=self.user1)
        post2 = sample_post(user=self.user2)

        post1.created_at = datetime(2020, 1, 1, 0, 0, 0)
        post1.save()

        res = self.client.get(POST_URL, {"created_at": "2020-01-01"})

        serializer1 = PostListSerializer(post1)
        serializer2 = PostListSerializer(post2)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_filter_by_hashtags(self):
        post_with_hashtags = sample_post(user=self.user1)
        post_without_hashtags = sample_post(user=self.user2)
        post_with_hashtags.hashtags.add(Hashtag.objects.create(name="test"))

        res = self.client.get(POST_URL, {"hashtags": "1"})

        serializer1 = PostListSerializer(post_with_hashtags)
        serializer2 = PostListSerializer(post_without_hashtags)

        self.assertIn(serializer1.data, res.data)
        self.assertNotIn(serializer2.data, res.data)

    def test_retrieve_post_detail(self):
        post = sample_post(user=self.user1)

        url = detail_url(id=post.id, api_name="post")
        res = self.client.get(url)

        serializer = PostSerializer(post)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_post(self):
        self.assertEqual(Post.objects.count(), 0)
        payload = {"content": "test content"}

        res = self.client.post(POST_URL, payload)
        post = Post.objects.get(id=res.data["id"])

        print(post)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        for key in payload:
            if key == "hashtags":
                hashtags_ids = list(post.hashtags.values_list("id", flat=True))
                self.assertEqual(payload[key], hashtags_ids)
            else:
                self.assertEqual(payload[key], getattr(post, key))
