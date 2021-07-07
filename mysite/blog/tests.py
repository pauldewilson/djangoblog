from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

def create_test_user(test_username):
    """
    Creates a test user
    """
    return User.objects.create(username=test_username)

class PostTestCases(TestCase):


    def test_can_create_post_object(self):

        test_user = create_test_user('TEST USER')

        new_post = Post(title='test create', author=test_user)
        new_post.save()

        response_post = Post.objects.get(id=1)

        self.assertEqual(response_post, new_post)
    
    def test_created_post_title_returned_correctly(self):

        test_new_title = 'ABC123'

        test_user = create_test_user('TEST USER')

        new_post = Post(title=test_new_title, author=test_user)
        new_post.save()

        response_post = Post.objects.get(id=1)

        self.assertEqual(test_new_title, response_post.title)