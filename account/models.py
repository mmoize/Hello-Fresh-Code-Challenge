from django.db.models.signals import post_save
from django.db import models
from django.contrib.auth.models import User
from django_extensions.db.models import (ActivatorModel,TimeStampedModel)
from menu_plan.models import Weeklymenu
import datetime



class Profile(TimeStampedModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    username = models.CharField(max_length=255, blank=True)
    weekly_menu = models.ManyToManyField(Weeklymenu, blank=True)
    
    def __str__(self):
        return self.user.username

# Profile creation signal: After user signs up, this signal automatically creats
# the Profile  for that user.
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.username = instance.username


        # Customer needs 52 weeks of weely menu recipes.
        # Code below calculates the Dates from the time of profile
        today = datetime.date.today()
        i = 1
        week_count =  53 # Adding 53 weeks, due to the fact that python will start at 0
        for week in range(week_count):
            if week == 0:  # Don't mind the zero here
              pass
            else:
                # Code below calculates the date from today.
                coming_weeks_date = today + datetime.timedelta(days=week*7)
                # Creating Weekly menu object with 3 available data.
                WeeklyMenu_Obj = Weeklymenu.objects.create(
                    week_date = coming_weeks_date,
                    week_number = i,
                    customer = profile
                )
                # Adding the created weekly menu obj to the profile instance
                profile.weekly_menu.add(WeeklyMenu_Obj)
                i +=1

        
        profile.save()
post_save.connect(create_user_profile, sender=User, dispatch_uid="users-profilecreation-signal")