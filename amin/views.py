from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import User, Car , Road, UserRoad, Road ,TollStationAndVehicle,CarLocation
from .serializers import (
                UserWithCarsSerializer, CarSerializer, RoadSerializer,
                TollStationSerializer,OverdueSerializer,
                CarLocationSerializer,CarLocationWithOwnerSerializer
    
            )
from rest_framework.generics import ListCreateAPIView

"""All APIs have been tested in GNU/Linux terminal and Postman."""
#######################################################################################
""" اکلاس زیر داده‌ها را پردازش کرده و هم کاربران و هم خودروهای مربوطه را ذخیره و به هم مرتبط می‌کند"""
#######################################################################################

class UserWithCars(APIView):

    #متد ارسال درخواست پست برای ثبت  
    def post(self, request):
        # اگر داده‌ها به صورت لیست باشند
        if isinstance(request.data, list):
            users_data = request.data
        else:
            users_data = [request.data]  # اگر داده‌ها یک دیکشنری باشند، آن را در لیست قرار می‌دهیم

        response_data = []
        for user_data in users_data:
            car_data = user_data.pop('ownerCar', [])  # جدا کردن لیست ماشین‌ها

            # سریالایزر برای ثبت کاربر
            user_serializer = UserWithCarsSerializer(data=user_data)
            if user_serializer.is_valid():
                user = user_serializer.save()  # ذخیره کاربر

                # ذخیره خودروها و اتصال به کاربر
                for car in car_data:
                    car['owner'] = user.id  # برای هر خودرو
                    car_serializer = CarSerializer(data=car)
                    if car_serializer.is_valid():
                        car_serializer.save()  # ذخیره خودرو
                    else:
                        return Response(car_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

                # پس از ذخیره کاربر و خودروها، داده‌های کاربر به پاسخ اضافه می‌شود
                response_data.append(UserWithCarsSerializer(user).data)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # بازگشت لیستی از داده‌های کاربران و خودروهای مربوطه
        return Response(response_data, status=status.HTTP_201_CREATED)


##########################################################
    """
    API برای دریافت لیست خودروهایی که رنگ آنها قرمز یا آبی است
    """
##########################################################

class RedAndBlueCars(APIView):

    def get(self, request):
        # فیلتر کردن خودروهایی که رنگ آنها قرمز یا آبی است
        red_and_blue_cars = Car.objects.filter(color__in=['red', 'blue'])
        serializer = CarSerializer(red_and_blue_cars, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


###############################################################################
"""لیست خودرو های متعلق به کاربرانی که سن آن‌ها بیش از 70 سال است را بر می‌ گرداند"""
###############################################################################

class OlderOwner(APIView):

    def get(self, request):
        # فیلتر کردن کاربران با سن بیشتر از 70 سال
        users = User.objects.filter(age__gt=70)
        
        # دریافت خودروهای مرتبط با کاربران فیلتر شده
        cars = Car.objects.filter(owner__in=users)
        
        # استفاده از سریالایزر برای تبدیل داده‌ها به فرمت JSON
        serializer = CarSerializer(cars, many=True)
        
        return Response(serializer.data, status=status.HTTP_200_OK)
    
###########################################################################################################
"""امکان ایجاد و دریافت لیست جاده‌ها را فراهم می‌کند و در صورت عدم وجود نام جاده، مقدار پیش‌ فرض "نامشخص" را تنظیم می‌کند"""
###########################################################################################################

class RoadCreate(ListCreateAPIView):

    queryset = Road.objects.all()
    serializer_class = RoadSerializer

    def create(self, request, *args, **kwargs):
        data = request.data

        # اگر داده‌ها لیستی از جاده‌ها باشند
        if isinstance(data, list):
            roads = []
            for road_data in data:
                if road_data.get("name") is None:
                    road_data["name"] = "نامشخص"  # مقدار پیش‌فرض برای نام

                serializer = self.get_serializer(data=road_data)
                if serializer.is_valid():
                    road = serializer.save()
                    roads.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(roads, status=status.HTTP_201_CREATED)

        # اگر فقط یک جاده ارسال شده باشد
        if data.get("name") is None:
            data["name"] = "نامشخص"

        return super().create(request, *args, **kwargs)


###########################################################################
"""
    خودرو های سنگین (با حجم بار ≥ 300) را که در جاده‌های باریک‌ تر از ۲۰ متر تردد داشته‌اند
        شناسایی و اطلاعات آن‌ها را همراه با لیست جاده‌ های باریک ارائه می‌دهد
"""
###########################################################################

class HeavyCarsInNarrowRoads(APIView):

    def get(self, request):
        # پیدا کردن جاده‌های باریک‌تر از ۲۰ متر
        narrow_roads = Road.objects.filter(width__lt=20)

        # پیدا کردن خودروهای سنگین (load_valume >= 300) که در این خیابان‌ها تردد داشته‌اند
        heavy_cars = Car.objects.filter(
            id__in=UserRoad.objects.filter(road__in=narrow_roads).values_list("car_id", flat=True),
            load_valume__gte=300
        ).distinct()

        car_serializer = CarSerializer(heavy_cars, many=True)
        road_serializer = RoadSerializer(narrow_roads, many=True)

        return Response(
            {
                "heavy_cars": car_serializer.data,
                "narrow_roads": road_serializer.data
            },
            status=status.HTTP_200_OK
        )



###################################################################
"""
    امکان به‌ روزرسانی و حذف موقعیت‌های یک خودرو را فراهم می‌کند
    به‌طوری که موقعیت‌ها می‌توانند به‌ صورت یک آبجکت منفرد
    یا لیستی از موقعیت‌ها ارسال یا حذف شوند
"""
###################################################################

class UpdateCarLocations(APIView):

    def post(self, request, car_id):
        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # اگر داده‌ها لیست باشند
        if isinstance(data, list):  
            for entry in data:
                entry["car"] = car_id  # اضافه کردن car_id به هر ورودی در لیست

            serializer = CarLocationSerializer(data=data, many=True)

        # اگر داده‌ها فقط یک آبجکت باشد
        else:  
            data["car"] = car_id
            serializer = CarLocationSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, car_id):

        try:
            car = Car.objects.get(id=car_id)
        except Car.DoesNotExist:
            return Response({"error": "Car not found"}, status=status.HTTP_404_NOT_FOUND)

        data = request.data

        # اگر داده‌ها لیست باشند
        if isinstance(data, list):  
            for entry in data:
                entry["car"] = car_id  # اضافه کردن car_id به هر ورودی در لیست

            serializer = CarLocationSerializer(data=data, many=True)

        # اگر داده‌ها فقط یک آبجکت باشد
        else:  
            data["car"] = car_id
            serializer = CarLocationSerializer(data=data)

        if isinstance(data, list):
    # حذف موقعیت‌های مشخص‌شده در لیست
            CarLocation.objects.filter(car=car, id__in=[entry["id"] for entry in data]).delete()
        else:
    # حذف موقعیت مشخص‌شده در یک آبجکت
            CarLocation.objects.filter(car=car, id=data["id"]).delete()

        return Response({"message": "Locations deleted successfully"}, status=status.HTTP_200_OK)


    
###############################################################################
""" تمامی موقعیت‌ های ثبت‌ شده خودروها را همراه با اطلاعات مالک آن‌ها بازیابی و ارائه می‌کند"""
###############################################################################

class CarLocationWithOwner(APIView):
    def get(self, request):
        # دریافت تمامی موقعیت‌ها و مربوط به خودروها
        car_locations = CarLocation.objects.all()
        serializer = CarLocationWithOwnerSerializer(car_locations, many=True)
        return Response(serializer.data)


#################################################################################
"""اطلاعات ایستگاه‌ های عوارضی را دریافت کرده و در صورت اعتبار داده‌ ها، آن‌ها را ذخیره می‌کند"""    
#################################################################################

class TollStationVehicle(APIView):

    def post(self, request):
        if isinstance(request.data, list):
                Vehicle_data = request.data
        else:
                Vehicle_data = [request.data]


        Vehicle_serializer = TollStationSerializer(data=Vehicle_data,many=True)
                                                              
        
        if Vehicle_serializer.is_valid():
            tolls = Vehicle_serializer.save()  # ذخیره‌سازی
            
            return Response(TollStationSerializer(tolls, many=True).data, status=status.HTTP_201_CREATED)
        
        return Response(Vehicle_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

##############################################################################################
"""لیست خودروهای سبک (سواری) را که در فاصله ۶۰۰ متری از عوارضی 1 قرار دارند، فیلتر کرده و نمایش می‌ دهد"""
##############################################################################################

class LocationLightVehicle(APIView):

    def get(self, request):
        # فیلتر کردن خودروهای سبک (car) که نزدیک عوارضی 1 و در محدوده 600 متری هستند
        light_vehicles = TollStationAndVehicle.objects.filter(
            vehicle_type='car',
            nearest_toll=1,
            distance_to_nearest_toll__lte=600
        )

        serializer = TollStationSerializer(light_vehicles, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)       

###########################################################################################
"""فهرست مالکانی را که بدهی عوارضی پرداخت‌ نشده دارند، به ترتیب میزان تخلف (بیشترین بدهی) نمایش می‌دهد"""
###########################################################################################

class Tollviolation(APIView):

    def get(self, request):

        toll_vio = TollStationAndVehicle.objects.filter(
            overdue_toll__gt=0).order_by('-overdue_toll')
            
        serializer = OverdueSerializer(toll_vio, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
############################################
"""بررسی وجود نام هایی خاص  """
############################################

class Moghtader(APIView):

    def get(self, request):

        mo = Road.objects.filter(name='مقتدر')
    
        if mo.exists():
            serializer = RoadSerializer(mo, many=True)
            response_data = {
                "message": "مقتدر که بنده باشم در این مختصات نبودم",
                "data": serializer.data
            }
        else:
            response_data = {
                "message": "نام مقتدر وجود ندارد",
                "data": []
            }

        return Response(response_data, status=status.HTTP_200_OK)
        



