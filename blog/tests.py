from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import Post
# Create your tests here.
class BlogTest(TestCase):
    def setUp(self) -> None:
        self.user = get_user_model().objects.create(
            username = 'test user',
            email = 'test@email.com',
            password = 'testpassword'
        )

        self.post: Post = Post.objects.create(
            title='Test blog Title', 
            author = self.user,
            body = 'Test Body Title')
    
    def test_post_model_repr(self):
        post = Post.objects.get(id = self.post.id)
        self.assertEqual(post.title, 'Test blog Title')

    def test_home_page_access(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_home_page_reverse_lookup(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)

    def test_home_page_template(self):
        response = self.client.get(reverse('home'))
        self.assertTemplateUsed(response, 'home.html')

    def test_home_page_content(self):
        response = self.client.get(reverse('home'))
        self.assertContains(response, 'Test blog Title')
        self.assertContains(response, 'Test Body Title')

    def test_post_detail_page_access(self):
        response = self.client.get('/post/1/')
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_reverse_lookup(self):
        response = self.client.get(reverse('post_detail', args=[str(self.post.id)]))
        self.assertEqual(response.status_code, 200)

    def test_post_detail_page_template(self):
        response = self.client.get(reverse('post_detail', args=[str(self.post.id)]))
        self.assertTemplateUsed(response, 'post_detail.html')

    def test_post_detail_page_content(self):
        response = self.client.get(reverse('post_detail', kwargs={'pk': self.post.pk}))
        self.assertContains(response, 'Test blog Title')
        self.assertContains(response, 'Test Body Title')

    def test_post_detail_incorrect_access(self):
        response = self.client.get('/post/1000/')
        self.assertEqual(response.status_code, 404)