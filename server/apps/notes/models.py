from djongo import models


class Note(models.Model):
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='notes',
        verbose_name='User',
    )
    headline = models.CharField(max_length=70, verbose_name='Headline')
    text = models.TextField(verbose_name='Text')
    tags = models.ManyToManyField(
        'notes.Tag',
        related_name='notes',
        verbose_name='Tags',
    )
    start_at = models.DateTimeField(
        blank=True,
        verbose_name='Date and time of event starting',
    )
    is_watched = models.BooleanField(
        default=False,
        verbose_name='Is notification watched?'
    )

    def __str__(self):
        return self.headline

    class Meta:
        verbose_name = 'Note'
        verbose_name_plural = 'Notes'


class Tag(models.Model):
    name = models.CharField(max_length=50, verbose_name='Name')
    user = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='tags',
        verbose_name='User',
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Tag'
        verbose_name_plural = 'Tags'
