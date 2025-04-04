from rest_framework import serializers
from .models import User, Car , Road ,TollStationAndVehicle,CarLocation


####################################################
class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = '__all__'

class UserWithCarsSerializer(serializers.ModelSerializer):
    national_code = serializers.IntegerField(required=False)
    age = serializers.IntegerField(required=False)
    total_toll_paid = serializers.FloatField(required=False)

    class Meta:
        model = User
        fields = ['name', 'national_code', 'age', 'total_toll_paid']
############################################################

class RoadSerializer(serializers.ModelSerializer):
    users = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), 
                                               many=True, required=False)

    class Meta:
        model = Road
        fields = '__all__'
####################################################


class CarLocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarLocation
        fields = ['id', 'car', 'location', 'date']
####################################################


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
####################################################


class TollStationSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStationAndVehicle
        fields = ['car_id','vehicle_type','distance_to_nearest_toll']
####################################################
class OverdueSerializer(serializers.ModelSerializer):
    class Meta:
        model = TollStationAndVehicle
        fields = ['car_id','overdue_toll','name',
                  'owner_national_code','toll_per_cross','unpaid_toll']