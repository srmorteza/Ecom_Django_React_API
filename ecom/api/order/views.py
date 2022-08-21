from rest_framework import viewsets
from django.http import JsonResponse
from django.contrib.auth import get_user_model
from .serializers import OrderSerializer
from .models import Order
from django.views.decorators.csrf import csrf_exempt


def validate_user_session(id, token):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=id)
        if user.session_token == token:
            return True
        else:
            return False

    except UserModel.DoesNotExist:
        return False


@csrf_exempt
def add(request, id, token):
    if not validate_user_session(id, token):
        return JsonResponse('Error': 'Please RE-login', 'code': '1')
    if request.method == 'POST':
        user_id = id
        transaction_id = request.POST('transaction_id')
        amount = request.POST('amount')
        products = request.POST('products')

        total_pro = len(products.split(',')[:-1])
        UserModel = get_user_model()

        try:
            user = UserModel.objects.get(pk=id)

        except UserModel.DoesNotExist:
            return JsonResponse({'Error': 'user dose not exist'})

        order = Order(user=user,
                      product_name=products,
                      total_product=total_pro,
                      transaction_id=transaction_id,
                      total_amount=amount
                      )
        order.save()
        return JsonResponse({'success': True, 'Error': False, 'msg': 'order placed succsesfuly'})


class OrderViewSet(viewsets.ModelViewSet):
    queryset = order.objects.all().order_by('id')
    serializer_class = OrderSerializer
