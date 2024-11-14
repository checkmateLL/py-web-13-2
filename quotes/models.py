from django.db import models

class Author(models.Model):
    fullname = models.CharField(max_length=200)
    born_date = models.CharField(max_length=200)  # Change to CharField to match the date format from MongoDB
    born_location = models.CharField(max_length=200)
    description = models.TextField()
    mongo_id = models.CharField(max_length=24, unique=True, null=True, blank=True)  # Added field for MongoDB _id

    def __str__(self):
        return self.fullname

class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.CharField(max_length=200)
    mongo_id = models.CharField(max_length=24, unique=True, null=True, blank=True)  # Added field for MongoDB _id

    def __str__(self):
        return self.quote[:50]
