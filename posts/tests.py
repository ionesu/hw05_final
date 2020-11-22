from io import BytesIO
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from posts.models import Post, Group, Comment, Follow
from django.urls import reverse
from urllib.parse import urljoin
from django.core.cache import cache
from django.core.cache.utils import make_template_fragment_key

User = get_user_model()


class BlogTests(TestCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='IvanSushkov')
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)
        cls.unauthorized_client = Client()
        cls.group = Group.objects.create(
            title='test group',
            slug='test_group',
            description='Тестовое описание для тестового поста.'
        )
        cls.text = 'Тестовый текст!'
        cls.edit = 'Измененный тестовый текст!'

    def urls(self):
        urls = [
            reverse('index'),
            reverse('profile', kwargs={'username': self.user.username}),
            reverse('post_view',
                    kwargs={'username': self.user.username, 'post_id': 1}),
            reverse('group_posts', kwargs={'slug': self.group.slug})]
        return urls

    def test_homepage(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_new_post(self):
        self.client.force_login(self.user)
        current_posts_count = Post.objects.count()
        response = self.client.post(
            '/new/',
            {'text': 'Это текст публикации'},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), current_posts_count + 1)

    def test_force_login(self):
        self.client.force_login(self.user)
        response = self.client.get('/new/')
        self.assertEqual(response.status_code, 200)

    def test_unauthorized_user_newpage(self):
        response = self.client.get('/new/')
        self.assertRedirects(
            response,
            '/auth/login/?next=/new/',
            status_code=302,
            target_status_code=200
        )

    def check_post_content(self, url, user, group, text, new_text):
        self.authorized_client.get(url)
        self.assertEqual(user, self.user)
        self.assertEqual(group, self.group)
        self.assertEqual(text, self.text)
        self.assertEqual(new_text, self.edit)

    def test_new_post_authorized_user(self):
        response = self.authorized_client.get('new_post')
        self.assertEqual(response.status_code, 404)
        response = self.authorized_client.post(
            reverse('new_post'),
            data={'text': self.text, 'group': self.group.id},
            follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Post.objects.count(), 1)
        self.check_post_content(
            'new_post',
            self.user,
            self.group,
            self.text,
            self.edit
        )

    def test_new_post_unauthorized_user(self):
        response = self.unauthorized_client.post(
            reverse('new_post'),
            data={'text': self.text, 'group': self.group.id},
            follow=True
        )
        url = urljoin(reverse('login'), '?next=/new/')
        self.assertRedirects(response, url)
        self.assertEqual(Post.objects.count(), 0)

    def test_new_post_location(self):
        self.authorized_client.post(
            reverse('new_post'),
            data={'text': self.text, 'group': self.group.id},
            follow=True
        )
        for url in (self.urls()):
            with self.subTest(url=url):
                self.check_post_content(
                    url,
                    self.user,
                    self.group,
                    self.text,
                    self.edit
                )

    def test_edit_post(self):
        post = Post.objects.create(
            text=self.text,
            group=self.group,
            author=self.user,
        )
        self.authorized_client.post(
            reverse('post_edit',
                    kwargs={'username': post.author,
                            'post_id': post.id}),
            data={'text': self.edit,
                  'group': post.group.id},
            follow=True)
        for url in (self.urls()):
            with self.subTest(url=url):
                self.check_post_content(
                    url,
                    self.user,
                    self.group,
                    self.text,
                    self.edit
                )

    def test_404(self):
        response = self.authorized_client.get("/some_trouble_url/")
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, "misc/404.html")

    def test_index_cache_key(self):
        key = make_template_fragment_key('index_page', [1])
        self.authorized_client.get('index')
        self.assertTrue(bool(cache.get(key)),
                        'нет данных в кеше под ключом "index_page"')
        cache.clear()
        self.assertFalse(bool(cache.get(key)), 'кеш не очищен')

    def test_index_cache(self):
        response = self.authorized_client.get('index')
        self.authorized_client.post(
            '/new/', {'text': 'Тестовый текст кеш поста.'})
        response = self.authorized_client.get('/')
        self.assertNotContains(
            response,
            'Тестовый текст кеш поста.',
            msg_prefix="index page not cached")
        cache.clear()
        response = self.authorized_client.get('/')
        self.assertContains(
            response,
            'Тестовый текст кеш поста.',
            msg_prefix="кеш очищен - пост не на главной странице")

    def test_image_on_pages(self):
        post = Post.objects.create(text="Post with image",
                                   group=self.group,
                                   author=self.user)
        img = BytesIO(
            b'GIF87a\x01\x00\x01\x00\x80\x01\x00\x00\x00\x00ccc,\x00'
            b'\x00\x00\x00\x01\x00\x01\x00\x00\x02\x02D\x01\x00;')
        image_name = 'foo_image.gif'
        img = SimpleUploadedFile(
            image_name, img.read(), content_type='image/gif')
        response = self.authorized_client.post(
            reverse("post_edit",
                    kwargs={"username": self.user.username,
                            "post_id": post.id}),
            data={"text": "Post with image",
                  "image": img}, follow=True)
        for url in self.urls():
            with self.subTest(url=url):
                self.assertEqual(response.status_code, 200)
                self.assertContains(response, "test_id")

    def test_non_image(self):
        with open("posts/urls.py") as file:
            response = self.authorized_client.post(
                "/new/", {"text": "Some text", "image": file}, follow=True)
            self.assertNotContains(response, "test_id")

    def test_check_follow_auth(self):
        follower = User.objects.create_user(
            username="follower",
            password="12345"
        )
        self.authorized_client.post(reverse(
            "profile_follow", kwargs={"username": follower.username, }))
        follow = Follow.objects.first()
        self.assertEqual(Follow.objects.count(), 1)
        self.assertEqual(follow.author, follower)
        self.assertEqual(follow.user, self.user)

    def test_check_follower_see_followed_post(self):
        response = self.authorized_client.get('/follow/')
        self.assertIn(
            self.text, response.context['page'],
            "author followed, but their post not appears on /follow/")

    def test_check_follow_non_unauth(self):
        follower = User.objects.create_user(
            username="follower",
            password="12345"
        )
        self.unauthorized_client.post(reverse(
            "profile_follow", kwargs={"username": follower.username, }))
        self.assertFalse(Follow.objects.filter(
            user=follower,
            author=self.user
            ).exists(),
            "Follow object was not deleted")

    def test_check_unfollow(self):

        follower = User.objects.create_user(
            username="follower",
            password="12345"
        )
        Follow.objects.create(user=self.user, author=follower)
        self.authorized_client.post(reverse(
            "profile_unfollow", kwargs={"username": follower.username, }))
        self.assertFalse(Follow.objects.filter(
            user=follower,
            author=self.user
            ).exists(),
            "Follow object was not deleted")

    def test_check_follower_not_see_followed_post(self):
        response = self.authorized_client.get('/follow/')
        self.assertNotIn(
            self.text, response.context['page'],
            "author not followed, but their post appears on /follow/")

    def test_auth_user_can_comment(self):
        self.author = User.objects.create(
            username="leo",
            password="123456"
        )
        self.post = Post.objects.create(
            text="Test post!",
            author=self.author
        )
        response = self.authorized_client.post(reverse(
            "add_comment", kwargs={
                "username": self.author,
                "post_id": self.post.id
            }),
            data={"text": "Test comment", "author": self.user}, follow=True, )
        self.assertEqual(response.status_code, 200)
        self.comment = Comment.objects.last()
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(self.comment.text, "Test comment")

    def test_non_auth_user_cant_comment(self):
        self.author = User.objects.create(
            username="leo",
            password="123456"
        )
        self.post = Post.objects.create(
            text="Test post!",
            author=self.user
        )
        response = self.unauthorized_client.post(reverse(
            "add_comment", kwargs={
                "username": self.user.username,
                "post_id": self.post.id
            }),
            data={
                "text": "Test comment",
                "author": self.user.id,
                "post": self.post.id
        })
        self.assertEqual(response.status_code, 302)
        self.assertEqual(Comment.objects.count(), 0)
