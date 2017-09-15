from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True, null=True)

    class Meta:
        ordering = ['user']

    def __str__(self):
        return self.get_full_name()

    def get_absolute_url(self):
        return reverse('author_detail', args=[str(self.id)])

    def get_full_name(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)


class Post(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField(max_length=4000, )
    published_at = models.DateTimeField()
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-published_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.id)])


class Comment(models.Model):
    content = models.TextField(max_length=500, verbose_name='Comment')
    published_at = models.DateTimeField(auto_now=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        ordering = ['published_at']

    def __str__(self):
        return self.content

    def get_absolute_url(self):
        return reverse('post_detail', args=[str(self.post.id)])
