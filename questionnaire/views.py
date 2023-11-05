from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from questionnaire.models import QuestionnaireType
from questionnaire.serializers import QuestionnaireTypeSerializer


@api_view(["GET"])
@permission_classes([AllowAny])
def get_questionnaire(request, questionnaire_id):
    questionnaire = QuestionnaireType.objects.get(id=questionnaire_id)
    serializer = QuestionnaireTypeSerializer(instance=questionnaire)
    return Response(serializer.data)
    # response = Response(serializer.data)
    # response.set_cookie("key", "qwertyuio")
    # if 'key' in request.COOKIES:
    #     print(request.COOKIES.get('key'))
    # return response

# @api_view(["GET"])
# def questionnaire_options(request, card_id):
#     """
#     ORDER. STEP 2. Получаем с Front card_id, выводим все доступные анкеты для выбора.
#
#     """
#
#     all_forms = QuestionnaireModel.objects.filter(card_category__id=card_id)
#     result = list()
#     for item in all_forms:
#         result.append({
#             "id": item.id,
#             "questionnaire_type": item.questionnaire_type
#         })
#
#     return Response(result)
#
#
# class CategoryModelListAPIView(ListAPIView):
#     """
#     ORDER - OLD. STEP 2. Получить список категорий (возможных товаров) по id карточки (раздела)
#
#     """
#
#     model = CategoryModel
#     permission_classes = [AllowAny]
#     serializer_class = CategoryModelSeializer
#     throttle_classes = [AnonRateThrottle, UserRateThrottle]
#
#     def get_queryset(self):
#         card_id = self.kwargs["card_id"]
#         return CategoryModel.objects.filter(card__id=card_id).all()
#
#
# class QuestionsModelListAPIView(ListAPIView):
#     """
#     ORDER. STEP 3.1. Получить список вопросов по id категории (товара)
#
#     """
#
#     model = QuestionsProductsModel
#     permission_classes = [AllowAny]
#     serializer_class = QuestionModelSerializer
#     throttle_classes = [AnonRateThrottle, UserRateThrottle]
#
#     def get_queryset(self):
#         category_id = self.kwargs["category_id"]
#         return QuestionsProductsModel.objects.filter(category__id=category_id).all()
#
#
# class AnswerListAPIView(CreateAPIView):
#     """
#     ORDER. STEP 3.2. Создать ответы на вопросы
#
#     """
#
#     permission_classes = [IsAuthenticated]
#     serializer_class = AnswerCreateSerializer
#
#     def get_serializer(self, *args, **kwargs):
#         """if an array is passed, set serializer to many"""
#         if isinstance(kwargs.get("data", {}), list):
#             kwargs["many"] = True
#         return super(AnswerListAPIView, self).get_serializer(*args, **kwargs)
#
#     def create(self, request, *args, **kwargs):
#         user = request.user
#         order = OrderModel.objects.create(user_account=user, state='creating')
#         request.order = order.id
#         return super(AnswerListAPIView, self).create(request, *args, **kwargs)
#
#
# @api_view(['POST'])
# def CreateOrderAnswers(request):
#     """
#     ORDER. STEP 4. Получить описание, сразу создать заказ (статус: Не закончен) и добавить все ответы без order_id.
#
#     """
#
#     # создаем заказ и передаем данные
#     serializer = OrderModelSerializer(data=request.data, context={'request': request, 'state': 'new'})
#     if serializer.is_valid():
#         order_create = serializer.save()
#
#         # если заказ создан, ищем ответы на вопросы (которые без привязки order_id) и записываем их к этому заказу
#         ResponseModel.objects.filter(user_account=request.user.id, order_id=None).update(order_id=order_create.id)
#
#         return Response(serializer.data, status=status.HTTP_200_OK)
#
#     else:
#         return Response(status=status.HTTP_400_BAD_REQUEST)
#
#
# class ImageResponseAPIView(CreateAPIView):
#     """
#     Загрузить изображение к ответу
#
#     """
#
#     permission_classes = [IsAuthenticated]
#     serializer_class = AnswerImageSerializer
