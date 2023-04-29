from django.db import models
from accounts.models import Account

class WhtsappCampaign(models.Model):
    STATUS_CHOICES = (
        ('Submitted', 'Submitted'),
        ('Rejected', 'Rejected'),
        ('Stopped', 'Stopped'),
        ('Processing', 'Processing'),
        ('Completed', 'Completed'),
    )

    user = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True, null=True)
    numbers = models.TextField()
    message = models.TextField()
    image1 = models.ImageField(upload_to='wapp_camp_img/', blank=True, null=True)
    image2 = models.ImageField(upload_to='wapp_camp_img/', blank=True, null=True)
    image3 = models.ImageField(upload_to='wapp_camp_img/', blank=True, null=True)
    image4 = models.ImageField(upload_to='wapp_camp_img/', blank=True, null=True)
    video = models.FileField(upload_to='wapp_camp_video/', blank=True, null=True)
    pdf = models.FileField(upload_to='wapp_camp_pdf/', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Submitted", null=True, blank=True)

    def __str__(self):
        return f'{self.created_at} - {self.user.username}'