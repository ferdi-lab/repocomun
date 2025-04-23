from django.db import models

class UrlMonitor(models.Model):
    url = models.URLField(unique=True)
    last_hash = models.CharField(max_length=64, blank=True, null=True)
    last_checked = models.DateTimeField(auto_now=True)
    has_changes = models.BooleanField(default=False)
    marked_done = models.BooleanField(default=False)

    def __str__(self):
        return self.url
