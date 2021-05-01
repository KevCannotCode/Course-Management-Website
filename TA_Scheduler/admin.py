from django.contrib import admin
from .models import myAccount
from .models import myCourse
from .models import myLab
from .models import myContact
from .models import myCourseInstructor
from .models import myLabTA
from .models import labToCourse
# Register your models here.
admin.site.register(myAccount)
admin.site.register(myCourse)
admin.site.register(myLab)
admin.site.register(myContact)
admin.site.register(myCourseInstructor)
admin.site.register(myLabTA)
admin.site.register(labToCourse)