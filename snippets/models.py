from django.db import models




class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)

    # owner = models.ForeignKey(
    #     'auth.User', related_name='snippets', on_delete=models.CASCADE)
    # highlighted = models.TextField()

    class Meta:
        ordering = ('created', )
