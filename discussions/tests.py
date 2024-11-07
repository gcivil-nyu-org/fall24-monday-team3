from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Topic, Discussion

User = get_user_model()


class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Test Topic")
        self.assertEqual(self.topic.slug, "test-topic")


class DiscussionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
        )
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="This is a test discussion.",
            topic=self.topic,
            author=self.user
        )

    def test_discussion_creation(self):
        self.assertEqual(self.discussion.title, "Test Discussion")
        self.assertEqual(self.discussion.content, "This is a test discussion.")
        self.assertEqual(self.discussion.topic, self.topic)
        self.assertEqual(self.discussion.author, self.user)


class DiscussionListViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="This is a test discussion.",
            topic=self.topic,
            author=self.user
        )

    def test_discussion_list_view(self):
        response = self.client.get(reverse('discussions:discussion_list'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/discussion_list.html')
        self.assertContains(response, "Test Discussion")


class DiscussionDetailViewTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser', password='12345'
            )
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="This is a test discussion.",
            topic=self.topic,
            author=self.user
        )

    def test_discussion_detail_view(self):
        response = self.client.get(
            reverse('discussions:discussion_detail', args=[self.discussion.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'discussions/discussion_detail.html')
        self.assertContains(response, "Test Discussion")
