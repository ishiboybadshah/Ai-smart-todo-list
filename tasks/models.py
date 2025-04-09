from django.db import models
from datetime import date



import openai
from django.conf import settings


    

class Task(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    due_date = models.DateField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    priority = models.CharField(max_length=10, blank=True)

    def __str__(self):
        return self.title
    from django.db import models

    def save(self, *args, **kwargs):
        if not self.priority:
            self.priority = self.get_ai_priority()
        super().save(*args, **kwargs)

    def get_ai_priority(self):
        openai.api_key = settings.DEEPINFRA_API_KEY
        openai.api_base = "https://api.deepinfra.com/v1/openai"

        prompt = f"""
        You are a smart assistant. Based on the following task details, assign a priority: High, Medium, or Low.
        
        Title: {self.title}
        Description: {self.description}
        Due Date: {self.due_date}

        Just return the priority only.
        """

        try:
            response = openai.ChatCompletion.create(
                model="mistralai/Mistral-7B-Instruct-v0.1",
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            result = response['choices'][0]['message']['content'].strip()
            return result if result in ['High', 'Medium', 'Low'] else 'Medium'
        except Exception as e:
            print("AI priority error:", e)
            return 'Medium'
