from django.db import models

class UserRegistrationModel(models.Model):
    loginid = models.CharField(unique=True, max_length=100)
    password = models.CharField(max_length=100)
    name = models.CharField(max_length=100)  
    email = models.CharField(unique=True, max_length=100)
    mobile = models.CharField(unique=True, max_length=100)
    locality = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    address = models.CharField(max_length=1000)
    status = models.CharField(max_length=100)

    def __str__(self):
        return self.loginid

    class Meta:
        db_table = 'UserRegistrations'


class UserTextDataModel(models.Model):
    user = models.ForeignKey(UserRegistrationModel, on_delete=models.CASCADE)
    text_data = models.TextField()
    upload_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Text data uploaded by {self.user.loginid} on {self.upload_date}"

    class Meta:
        db_table='usertestcaptions'
