from rest_framework import serializers
from .models import User, Car , Road ,TollStationAndVehicle,CarLocation

####################################################
"""کلتس زیر تمام فیلدهای آن را به صورت کامل سریالایز می‌کند """
####################################################
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

##############################################################################
"""  برای نمایش اطلاعات کاربر به همراه برخی فیلدهای اختیاری بدون وابستگی مستقیم به خودروها"""
##############################################################################

class UserWithCarsSerializer(serializers.ModelSerializer):
    national_code = serializers.IntegerField(required=False)
    age = serializers.IntegerField(required=False)
    total_toll_paid = serializers.FloatField(required=False)

    class Meta:
        model = User
        fields = ['name', 'national_code', 'age', 'total_toll_paid']


###################################################################
"""سریالایزر برای نمایش و مدیریت اطلاعات مدل Road شامل کاربران مرتبط با جاده"""
###################################################################

class RoadSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                                               many=True, required=False)

    class Meta:
        model = Road
        fields = '__all__'

##############################################################################
"""سریالایزر ساده برای نمایش اطلاعات موقعیت مکانی خودرو شامل شناسه، موقعیت و زمان ثبت"""
##############################################################################

class CarLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarLocation
        fields = ['id', 'car', 'location', 'date']

################################################################################
"""سریالایزری توسعه‌یافته برای نمایش موقعیت خودرو به همراه نام مالک، کد ملی و مجموع عوارض پرداختی"""
#################################################################################

class CarLocationWithOwnerSerializer(serializers.ModelSerializer):
    owner_name = serializers.CharField(source="car.owner.name", read_only=True)
    owner_national_code = serializers.CharField(source="car.owner.national_code",
                                                 read_only=True)
    total_toll_paid = serializers.SerializerMethodField()

    class Meta:
        model = CarLocation
        fields = ["id", "car", "owner_name", "owner_national_code", 
                  "location", "date", "total_toll_paid"]

    def get_total_toll_paid(self, obj):
        """
        محاسبه مجموع عوارض پرداخت‌شده توسط مالک خودروی فعلی
        """
        owner = obj.car.owner
        return owner.total_toll_paid  # مجموع عوارض از مدل User
    
#####################################################################################################
"""سریالایزر برای نمایش اطلاعات پایه‌ای خودروها در ایستگاه‌های عوارضی شامل نوع، شناسه و فاصله تا ایستگاه"""
#####################################################################################################

class TollStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStationAndVehicle
        fields = ['car_id','vehicle_type','distance_to_nearest_toll']

#####################################################################################
"""سریالایزر برای نمایش خودروهایی با عوارض پرداخت‌نشده و دیرکرد به همراه جزئیات کامل"""
####################################################################################
class OverdueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStationAndVehicle
        fields = ['car_id','overdue_toll','name',
                  'owner_national_code','toll_per_cross','unpaid_toll']
