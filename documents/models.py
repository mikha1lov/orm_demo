from django.contrib.auth.models import User
from django.db import models

from django.db.models.signals import post_save
from django.dispatch import receiver

class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True
        ordering = ['-created_at']


class Project(BaseModel):
    owner = models.ForeignKey(User, related_name='projects', null=True, on_delete=models.SET_NULL)


class Document(BaseModel):
    name = models.CharField(max_length=255)
    project = models.ForeignKey(Project, null=True, on_delete=models.SET_NULL)


class Comment(BaseModel):
    document = models.ForeignKey(Document, related_name='comments', null=True, on_delete=models.SET_NULL)
    text = models.TextField()


class Payment(BaseModel):
    amount = models.DecimalField(decimal_places=2, max_digits=10, default='0.0')
    amount_usd = models.DecimalField(decimal_places=2, max_digits=10, default='0.0')
    document = models.ForeignKey(Document, related_name='payments', null=True, on_delete=models.SET_NULL)


@receiver(post_save, sender=Payment)
def create_payment_comment(sender, instance, created, **kwargs):
    if created:
        Comment.objects.create(document=instance.document, text=f"Новый платеж по документы. Сумма {instance.amount}")
