from django.db import models

class Family(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        db_table = "families"

    def __str__(self):
        return self.name

class FamilyMember(models.Model):
    family = models.ForeignKey(Family, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=6, choices=[('Male', 'Male'), ('Female', 'Female')])
    mobile_number = models.CharField(max_length=10, unique=True)

    class Meta:
        db_table = "family_members"

    def __str__(self):
        return self.name

    def calculate_age(self):
        import datetime
        today = datetime.date.today()
        age = today.year - self.date_of_birth.year - (
                    (today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
        return age
