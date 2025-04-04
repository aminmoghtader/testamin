from django.db import models

############################################################################
"""مدل زیر اطلاعات کاربران را شامل نام، کد ملی، سن و مجموع عوارض پرداختی ذخیره می‌کند"""
############################################################################

class User(models.Model):
    name = models.CharField(max_length=100, null=True, blank=True)
    national_code = models.CharField(max_length=10, unique=True)
    age = models.IntegerField()
    total_toll_paid = models.IntegerField()

###################################################################################
"""مدل زیر اطلاعات خودروها را شامل مالک، نوع، رنگ، طول و حجم بار (در صورت وجود) مدیریت می‌کند"""
###################################################################################

class Car(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='ownerCar')
    type = models.CharField(max_length=20)
    color = models.CharField(max_length=10)
    length = models.FloatField()
    load_valume = models.FloatField(null=True, blank=True)

###################################################################################
"""موقعیت ‌های ثبت‌شده خودروها را با ذخیره شناسه خودرو، موقعیت مکانی و تاریخ ثبت مدیریت می‌کند"""
###################################################################################

class CarLocation(models.Model):
    car = models.ForeignKey(Car, on_delete=models.CASCADE, related_name="locations")
    location = models.CharField(max_length=255)
    date = models.DateTimeField()


############################################################################
"""
    مدل زیر اطلاعات مربوط به جاده‌ها را شامل نام، عرض جاده و داده‌های هندسی ذخیره می‌کند
                    و ارتباطی چند به چند با کاربران دارد
"""
############################################################################

class Road(models.Model):
    users = models.ManyToManyField(User, related_name="roads")  # ارتباط چند به چند بین کاربران و جاده‌ها
    name = models.CharField(max_length=255, null=True)
    width = models.FloatField()
    geom = models.TextField(null=True)  # به دلیل محدودیت های پایگاه داده محلی از این فیلد استفاده شده
    
####################################################################
"""
    ارتباط میان کاربران، خودروها و جاده‌هایی که در آن‌ها تردد داشته‌اند را نگهداری کرده
                    و از ثبت داده‌های تکراری جلوگیری می‌کند
"""
####################################################################

class UserRoad(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    road = models.ForeignKey(Road, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('user', 'car', 'road')  # از ذخیره داده‌های تکراری جلوگیری می‌کند

##########################################################
""" 
    اطلاعات مربوط به عوارضی و خودروها، شامل شناسه خودرو
        نوع، موقعیت مکانی، نزدیک‌ ترین عوارضی و میزان 
             عوارض پرداخت‌ نشده را مدیریت می‌کند
"""      
##########################################################

class TollStationAndVehicle(models.Model):

    VEHICLE_TYPES = [
        ('car', 'Car'),
        ('truck', 'Truck'),
        ('bus', 'Bus'),
    ]

    name = models.CharField(max_length=255)
    toll_per_cross = models.PositiveIntegerField()
    car_id = models.PositiveIntegerField(unique=True)
    owner_national_code = models.CharField(max_length=10)
    vehicle_type = models.CharField(max_length=10, choices=VEHICLE_TYPES)
    latitude = models.FloatField()
    longitude = models.FloatField()
    nearest_toll = models.PositiveIntegerField()
    distance_to_nearest_toll = models.PositiveIntegerField()
    unpaid_toll = models.PositiveIntegerField(default=0)
    overdue_toll = models.PositiveIntegerField(default=0)

