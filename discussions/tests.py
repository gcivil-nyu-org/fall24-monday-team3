from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from .models import Topic, Discussion, Reply, Vote
from django.db.models import Count

User = get_user_model()


class TopicModelTest(TestCase):
    def setUp(self):
        self.topic = Topic.objects.create(
            name="Test Topic", slug="test-topic", description="Test description"
        )

    def test_topic_creation(self):
        self.assertEqual(self.topic.name, "Test Topic")
        self.assertEqual(self.topic.slug, "test-topic")
        self.assertEqual(self.topic.description, "Test description")
        self.assertEqual(str(self.topic), "Test Topic")


class DiscussionModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="This is a test discussion.",
            topic=self.topic,
            author=self.user,
        )

    def test_discussion_creation(self):
        self.assertEqual(self.discussion.title, "Test Discussion")
        self.assertEqual(self.discussion.content, "This is a test discussion.")
        self.assertEqual(self.discussion.topic, self.topic)
        self.assertEqual(self.discussion.author, self.user)
        self.assertEqual(self.discussion.views, 0)
        self.assertEqual(str(self.discussion), "Test Discussion")

    def test_discussion_absolute_url(self):
        expected_url = reverse(
            "discussions:discussion_detail", kwargs={"pk": self.discussion.pk}
        )
        self.assertEqual(self.discussion.get_absolute_url(), expected_url)


class ReplyModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="Content",
            topic=self.topic,
            author=self.user,
        )
        self.reply = Reply.objects.create(
            discussion=self.discussion, author=self.user, content="Test reply"
        )

    def test_reply_creation(self):
        self.assertEqual(self.reply.content, "Test reply")
        self.assertEqual(self.reply.author, self.user)
        self.assertEqual(self.reply.discussion, self.discussion)
        expected_str = f"Reply by {self.user} on {self.discussion.title}"
        self.assertEqual(str(self.reply), expected_str)


class VoteModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="Content",
            topic=self.topic,
            author=self.user,
        )
        self.vote = Vote.objects.create(
            user=self.user, discussion=self.discussion, value=Vote.UPVOTE
        )

    def test_vote_creation(self):
        self.assertEqual(self.vote.value, Vote.UPVOTE)
        self.assertEqual(self.vote.user, self.user)
        self.assertEqual(self.vote.discussion, self.discussion)
        expected_str = f"{self.user} voted {Vote.UPVOTE} on {self.discussion.title}"
        self.assertEqual(str(self.vote), expected_str)


class DiscussionViewsTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="Content",
            topic=self.topic,
            author=self.user,
        )

    def test_discussion_list_view(self):
        response = self.client.get(reverse("discussions:discussion_list"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "discussions/discussion_list.html")
        self.assertContains(response, "Test Discussion")

    def test_discussion_detail_view(self):
        response = self.client.get(
            reverse("discussions:discussion_detail", args=[self.discussion.pk])
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "discussions/discussion_detail.html")
        self.assertContains(response, "Test Discussion")

        # Test view count increment
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.views, 1)

    def test_discussion_create_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("discussions:discussion_create"),
            {
                "title": "New Discussion",
                "content": "New content",
                "topic": self.topic.id,
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after creation
        self.assertTrue(Discussion.objects.filter(title="New Discussion").exists())

    def test_discussion_edit_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("discussions:discussion_edit", args=[self.discussion.pk]),
            {
                "title": "Updated Discussion",
                "content": "Updated content",
                "topic": self.topic.id,
            },
        )
        self.assertEqual(response.status_code, 302)
        self.discussion.refresh_from_db()
        self.assertEqual(self.discussion.title, "Updated Discussion")

    def test_discussion_delete_view(self):
        self.client.login(username="testuser", password="12345")
        response = self.client.post(
            reverse("discussions:discussion_delete", args=[self.discussion.pk])
        )
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Discussion.objects.filter(pk=self.discussion.pk).exists())


class VoteViewTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="testuser", password="12345")
        self.topic = Topic.objects.create(name="Test Topic", slug="test-topic")
        self.discussion = Discussion.objects.create(
            title="Test Discussion",
            content="Content",
            topic=self.topic,
            author=self.user,
        )

    def test_vote_discussion(self):
        self.client.login(username="testuser", password="12345")

        # Test upvote
        response = self.client.post(
            reverse("discussions:vote_discussion", args=[self.discussion.pk]),
            {"vote_type": "upvote"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["vote_count"], 1)

        # Test downvote
        response = self.client.post(
            reverse("discussions:vote_discussion", args=[self.discussion.pk]),
            {"vote_type": "downvote"},
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["vote_count"], 1)

        # Test invalid vote type
        response = self.client.post(
            reverse("discussions:vote_discussion", args=[self.discussion.pk]),
            {"vote_type": "invalid"},
        )
        self.assertEqual(response.status_code, 400)
