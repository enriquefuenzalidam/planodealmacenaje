from django.db import models

class LowercaseTextField(models.TextField):
    def to_python(self, value):
        value = super().to_python(value)
        if isinstance(value, str):
            return value.lower()
        return value

class Entry(models.Model):
    title = models.CharField(max_length=100, verbose_name="Title")
    tags = LowercaseTextField(verbose_name="Tags")
    def save(self, *args, **kwargs):
        self.tags = self.tags.lower()
        super().save(*args, **kwargs)
    def __str__(self):
        return self.title.strip().lower()

class Description(models.Model):
    entry = models.ForeignKey(Entry, related_name='descriptions', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Title")
    content = models.TextField(verbose_name="Content")
    def __str__(self):
        title = self.title.strip().lower() if self.title else "untitled"
        content = self.content.strip().lower()
        return f"{title[:50]}{content[:50]}"

class Number(models.Model):
    entry = models.ForeignKey(Entry, related_name='numbers', on_delete=models.CASCADE)
    number_title = models.CharField(max_length=100, verbose_name="Number Title")
    number = models.IntegerField()
    def __str__(self):
        return self.number_title.strip().lower()

class Date(models.Model):
    entry = models.ForeignKey(Entry, related_name='dates', on_delete=models.CASCADE)
    date_title = models.CharField(max_length=100, verbose_name="Date Title")
    date = models.DateField()
    def __str__(self):
        return self.date_title.strip().lower()

class Image(models.Model):
    entry = models.ForeignKey(Entry, related_name='images', on_delete=models.CASCADE)
    image_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="Image Title")
    image = models.ImageField(upload_to='images/')
    def __str__(self):
        return self.image.name.strip().lower()

class File(models.Model):
    entry = models.ForeignKey(Entry, related_name='files', on_delete=models.CASCADE)
    file_title = models.CharField(max_length=100, blank=True, null=True, verbose_name="File Title")
    file = models.FileField(upload_to='files/')
    def __str__(self):
        return self.file.name.strip().lower()
