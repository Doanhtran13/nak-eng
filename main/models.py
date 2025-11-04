from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
# Create your models here.

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username','email','first_name','last_name','password1','password2']


class TestResult(models.Model):
	user = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL)
	session_key = models.CharField(max_length=64, null=True, blank=True)
	score = models.FloatField()
	level = models.CharField(max_length=32)
	recommendation = models.TextField()
	details = models.TextField(blank=True, default='')
	created_at = models.DateTimeField(auto_now_add=True)

	class Meta:
		indexes = [
			models.Index(fields=['session_key', '-created_at']),
		]

	def __str__(self):
		owner = self.user.username if self.user else (self.session_key or 'anon')
		return f"TestResult(owner={owner}, score={self.score}, level={self.level})"