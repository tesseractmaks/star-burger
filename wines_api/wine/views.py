from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wine import models


@api_view(['GET'])
def wine_list(request):
    wines = models.Wine.objects.all()
    dumped_wines = []
    for wine in wines:
        dumped_wines.append({
            "category": wine.get_category_display(),
            "title": wine.title,
            "sort_of_grape": wine.sort_of_grape,
            "price": wine.price,
            "by_stock": wine.by_stock
        })
    # return JsonResponse(dumped_wines, safe=False, json_dumps_params={
    #     'ensure_ascii': False,
    #     'indent': 4,
    # })
    return Response(dumped_wines)
