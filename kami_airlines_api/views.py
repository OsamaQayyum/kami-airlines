from rest_framework import generics
import math
from rest_framework.response import Response
import logging


from .models import Airplane
from .serializers import AirplaneSerializer

class AirplaneListCreateView(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer

    def perform_create(self, serializer):
        serializer.save()

    def get_fuel_consumption(self, airplane):
        base_fuel_consumption = math.log(airplane.id) * 0.80
        print("==>base", base_fuel_consumption)
        passenger_fuel_consumption = airplane.passenger_count * 0.002
        print("==>passenger_fuel_consumption", passenger_fuel_consumption)

        total_fuel_consumption = base_fuel_consumption + passenger_fuel_consumption
        print("==>total_fuel_consumption", total_fuel_consumption)

        return total_fuel_consumption

    def list(self, request, *args, **kwargs):
        airplanes = self.get_queryset()
        total_consumption = 1
        planeIdWithConsumption = []
        for airplane in airplanes:
            consumption = self.get_fuel_consumption(airplane)
            print("===>consumption", consumption)
            max_minutes_fly_individual = min([200 / consumption, 500])  # Assuming a maximum of 500 minutes

            planeIdWithConsumption.append({"planeId": airplane.id, "passengerCount":airplane.passenger_count, "fuleConsuption":consumption, "max_fly_time":max_minutes_fly_individual })
            total_consumption += consumption

        max_minutes_fly = min([200 / total_consumption, 500])  # Assuming a maximum of 500 minutes

        print("===>consumption", planeIdWithConsumption)
        # sorted_planeIdWithConsumption = sorted(planeIdWithConsumption, key = operator.attrgetter('planeId'))
        # key = operator.attrgetter('discount')
        #planeIdWithConsumption.sort()


        response_data = {
                        'planeIdWithConsumption': planeIdWithConsumption,
                        'total_consumption_per_minute1': total_consumption,
                        'max_minutes_fly': max_minutes_fly
        }

        return Response(response_data)


class AirplaneListView(generics.ListCreateAPIView):
    queryset = Airplane.objects.all()
    serializer_class = AirplaneSerializer



