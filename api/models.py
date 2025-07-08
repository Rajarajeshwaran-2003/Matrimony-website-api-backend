from django.db import models

class UserProfile(models.Model):
    # Basic User Info
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)  # Hashed password
    gender = models.CharField(max_length=10)
    dob = models.DateField()
    phone = models.CharField(max_length=10)
    city = models.CharField(max_length=100)

    # Profile Info
    age = models.PositiveIntegerField(default=25)
    profession = models.CharField(max_length=150, default="Not specified")
    education = models.CharField(max_length=150, default="Not specified")
    interests = models.TextField(default="None", help_text="Comma-separated interests")
    photo = models.ImageField(upload_to='profile_photos/', null=True, blank=True)

    def __str__(self):
        return self.email
