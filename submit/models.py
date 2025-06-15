from django.db import models

# Create your models here.

class CodeSubmission(models.Model):
    language_choices = [
        ('py', 'Python'),
        ('cpp', 'C++'),
        ('java', 'Java'),
        ('c', 'C'),
        ('js', 'JavaScript'),
    ]
    code = models.TextField()
    language = models.CharField(max_length=10, choices=language_choices)
    input_data = models.TextField(null=True, blank=True)
    output_data = models.TextField(null=True, blank=True)
    error_message = models.TextField(null=True, blank=True)
    submission_time = models.DateTimeField(auto_now_add=True)
    result = models.TextField(null=True, blank=True)
    status = models.CharField(max_length=20, default='pending')  # e.g., 'pending', 'completed', 'error'
    
    def __str__(self):
        return f"Submission {self.id} - {self.language} - {self.status}"