from django.test import TestCase

from django.utils.timezone import now
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from blog.models import Author, Post, Comment


class AuthorModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_user(
            username='john',
            email='jlennon@beatles.com',
            password='glass onion',
            first_name='John',
            last_name='Wick',
        )
        Author.objects.create(
            user=new_user,
            bio='This is me, from the movies.'
        )

    def test_user_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('user').verbose_name
        self.assertEquals(field_label, 'user')

    def test_bio_label(self):
        author = Author.objects.get(id=1)
        field_label = author._meta.get_field('bio').verbose_name
        self.assertEquals(field_label, 'bio')

    def test_bio_max_length(self):
        author = Author.objects.get(id=1)
        max_length = author._meta.get_field('bio').max_length
        self.assertEquals(max_length, 500)

    def test_object_name_is_first_name_with_last_name(self):
        author = Author.objects.get(id=1)
        expected_object_name = '%s %s' % (author.user.first_name, author.user.last_name)
        self.assertEquals(expected_object_name, str(author))

    def test_get_absolute_url(self):
        author = Author.objects.get(id=1)
        self.assertEquals(author.get_absolute_url(), '/blog/author/1')

    def test_get_full_name(self):
        author = Author.objects.get(id=1)
        expected_full_name = '%s %s' % (author.user.first_name, author.user.last_name)
        self.assertEquals(expected_full_name, str(author))


class PostModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_user(
            username='john',
            email='jlennon@beatles.com',
            password='glass onion',
            first_name='John',
            last_name='Wick'
        )
        new_author = Author.objects.create(
            user=new_user,
            bio='This is me, from the movies.'
        )
        Post.objects.create(
            title='This the post title',
            content='This is the post content.',
            published_at=now(),
            author=new_author
        )

    def test_title_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('title').verbose_name
        self.assertEquals(field_label, 'title')

    def test_content_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'content')

    def test_published_at_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('published_at').verbose_name
        self.assertEquals(field_label, 'published at')

    def test_author_label(self):
        post = Post.objects.get(id=1)
        field_label = post._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_title_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('title').max_length
        self.assertEquals(max_length, 200)

    def test_content_max_length(self):
        post = Post.objects.get(id=1)
        max_length = post._meta.get_field('content').max_length
        self.assertEquals(max_length, 4000)

    def test_object_name_is_post_title(self):
        post = Post.objects.get(id=1)
        expected_object_name = post.title
        self.assertEquals(expected_object_name, str(post))

    def test_get_absolute_url(self):
        post = Post.objects.get(id=1)
        self.assertEquals(post.get_absolute_url(), '/blog/post/1')


class CommentModelTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_user(
            username='john',
            email='jlennon@beatles.com',
            password='glass onion',
            first_name='John',
            last_name='Wick'
        )
        new_author = Author.objects.create(
            user=new_user,
            bio='This is me, from the movies.'
        )
        new_post = Post.objects.create(
            title='This the post title',
            content='This is the post content.',
            published_at=now(),
            author=new_author
        )
        Comment.objects.create(
            content='This is the comment content.',
            published_at=now(),
            post=new_post,
            author=new_user
        )

    def test_content_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('content').verbose_name
        self.assertEquals(field_label, 'Comment')

    def test_published_at_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('published_at').verbose_name
        self.assertEquals(field_label, 'published at')

    def test_post_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('post').verbose_name
        self.assertEquals(field_label, 'post')

    def test_author_label(self):
        comment = Comment.objects.get(id=1)
        field_label = comment._meta.get_field('author').verbose_name
        self.assertEquals(field_label, 'author')

    def test_content_max_length(self):
        comment = Comment.objects.get(id=1)
        max_length = comment._meta.get_field('content').max_length
        self.assertEquals(max_length, 500)

    def test_object_name_is_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_object_name = comment.content
        self.assertEquals(expected_object_name, str(comment))

    def test_get_absolute_url(self):
        comment = Comment.objects.get(id=1)
        self.assertEquals(comment.get_absolute_url(), '/blog/post/1')


class PostListViewTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        new_user = User.objects.create_user(
            username='john',
            email='jlennon@beatles.com',
            password='glass onion',
            first_name='John',
            last_name='Wick'
        )
        new_author = Author.objects.create(
            user=new_user,
            bio='This is me, from the movies.'
        )
        Post.objects.create(
            title='This the post title',
            content='This is the post content.',
            published_at=now(),
            author=new_author
        )
        number_of_posts = 13
        for post_number in range(number_of_posts):
            Post.objects.create(
                title='This the post title %s' % post_number,
                content='This is the post content %s.' % post_number,
                published_at=now(),
                author=new_author
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'blog/post_list.html')

    def test_pagination_is_five(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue('is_paginated' in response.context)
        self.assertTrue(response.context['is_paginated'] == True)
        self.assertTrue(len(response.context['post_list']) == 5)
