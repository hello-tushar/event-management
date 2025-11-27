from django.db import models

class Participant(models.Model):
    name = models.CharField(max_length=80)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=90)
    category = models.ForeignKey("Category", on_delete=models.SET_NULL, null=True, blank=True)
    participants = models.ManyToManyField(Participant, related_name='events')

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name
# INSERT INTO public.event_event(name, description, date, time, location, category_id) VALUES ('Tech Event 25', 'No Description', '2025-12-12', '10:00:00', 'Sylhet, Bangladesh', 1)

