from djongo import models


class Note(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        verbose_name='User'
    )
    headline = models.CharField(max_length=70, verbose_name='Headline')
    text = models.TextField(verbose_name='Text')

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'
