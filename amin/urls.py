from django.urls import path
from .views import (
                    UserWithCars,RedAndBlueCars,OlderOwner,RoadCreate,
                    HeavyCarsInNarrowRoads,
                    UpdateCarLocations, CarLocationWithOwner,
                    TollStationVehicle,LocationLightVehicle,Tollviolation,Moghtader
               )

urlpatterns = [
    
    # لیست کاربران به همراه خودروهایشان    
    path('users/', UserWithCars.as_view(), name='users-with-cars'),

    # نمایش خودروهایی که رنگ آن‌ها قرمز یا آبی است
    path('cars/red-blue/', RedAndBlueCars.as_view(), name='red-blue-cars'),

    # نمایش خودروهایی که صاحبان آن‌ها سن بالایی دارند
    path('cars/older-owners/', OlderOwner.as_view(), name='cars-older-owners'),

    # ایجاد جاده‌های جدید در سیستم
    path('roads/', RoadCreate.as_view(), name='road-create'),

    # نمایش خودروهای سنگین که در جاده‌های باریک قرار دارند
    path('cars/heavy-in-narrow-roads/', HeavyCarsInNarrowRoads.as_view(),
          name='heavy-cars-in-narrow-roads'),

    # به‌روزرسانی موقعیت مکانی یک خودرو خاص با استفاده از شناسه آن
    path('cars/<int:car_id>/locations/', UpdateCarLocations.as_view(), 
          name='update-car-locations'),

    # به‌روزرسانی موقعیت مکانی خودروها
    path("car-locations/", UpdateCarLocations.as_view(), name="update-car-locations"),

    # نمایش موقعیت مکانی خودروهای یک مالک خاص بر اساس شناسه مالک
    path("car-locations/owner/<int:owner_id>/", UpdateCarLocations.as_view(), 
          name="car-locations-by-owner"), 

    # نمایش موقعیت خودروها به همراه اطلاعات مالک آن‌ها
    path('car-locations-with-owner/', CarLocationWithOwner.as_view(), 
          name='car-location-with-owner'),

    # نمایش لیست ایستگاه‌های عوارضی به همراه خودروهای موجود در آن‌ها
    path('toll-stations/', TollStationVehicle.as_view(), name='tollstation-list'),

    # نمایش موقعیت مکانی خودروهای سبک در نزدیکی ایستگاه عوارضی مشخص
    path('light-vehicles/', LocationLightVehicle.as_view(), name='light-vehicles'),
    
    # نمایش مالکانی که بدهی عوارضی دارند
    path('overdue/' ,Tollviolation.as_view(), name='Violating_owner' ),
     
    path('mogh/', Moghtader.as_view() , name='مقتدر اونجا چیکار میکنه')

]

