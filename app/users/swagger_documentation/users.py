from typing import List, Optional

from drf_yasg import openapi

from app.sending.serializers import DisableNotificationsSerializer
from config.settings import SWAGGER_TAGS, NOTIFICATION_CLASSES

DEFAULT_TAG = SWAGGER_TAGS.get("users")


class BaseSwaggerSchema:
    operation_description: str
    request_body: Optional[openapi.Schema]
    manual_parameters: Optional[List[openapi.Parameter]]
    responses: openapi.Responses


class TokenJWTCreateDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    operation_id = "jwt-create"
    operation_summary = "Получение токена авторизации"
    operation_description = (
        "Используйте этот метод для получения JWT токена авторизации.\n"
        "Полученный токен необходимо передавать в заголовках методов "
        "требующий авторизации в формате:\n- **authorization: "
        "JWT \\<token\\>**\n\nПри использовании метода выполняется проверка "
        "на наличие в куки ключа заказа (если ключ найден, то "
        "**авторизующийся пользователь станет владельцем заказа**, а заказ "
        "автоматически активируется если все обязательные поля заполнены) "
    )
    responses = {
        200: openapi.Response(
            "При верно введенных данных возвращается refresh и "
            "access токены",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "refresh": openapi.Schema(
                        type=openapi.TYPE_STRING, title="токен обновления"
                    ),
                    "access": openapi.Schema(
                        type=openapi.TYPE_STRING, title="JWT токен авторизации"
                    ),
                },
            ),
        ),
        401: openapi.Response(
            "При  неверно введенной связке логин-пароль возвращается ответ о"
            " том, что запрошенный пользователь не найден",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING, title="Описание ошибки"
                    )
                },
            ),
        ),
    }


class TokenJWTVerify(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    method = "post"


class TokenJWTRefresh(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("auth")]
    method = "post"


class UserActivationDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Активация аккаунта пользователя"
    operation_description = (
        "Используйте этот метод для активации аккаунта.\n При успешной "
        "активации пользователю будет отправлено на почту уведомление об "
        "активации аккаунта\n"
        "При наличии у пользователя заказа в статусе draft происходит его "
        "активация (при наличии ответов на все обязательные вопросы). "
        "И отправка уведомления о активации заказа."
    )
    method = "post"
    responses = {
        204: openapi.Response(description="No Content"),
        400: openapi.Response(
            "Bad Request",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING, title="Описание ошибки"
                    )
                },
            ),
        ),
        403: openapi.Response(
            "Forbidden",
            openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "detail": openapi.Schema(
                        type=openapi.TYPE_STRING, title="Описание ошибки"
                    )
                },
            ),
        ),
    }


class UsersCreateDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Регистрация пользователя"
    operation_description = (
        "Используйте метод для регистрации пользователя на платформе.\n" ""
    )


class SetUsernameDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = (
        "Смена email авторизованного пользователя *В разработке*"
    )
    operation_description = "**В разработке**"
    deprecated = True


class UsersListDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Список пользователей платформы *В разработке*"
    operation_description = "**В разработке**"
    deprecated = True


class UserMeReadDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("users_service")]
    operation_summary = "Информация об авторизованном пользователе"
    operation_description = (
        "Используйте этот метод для получения информации о авторизованном "
        "пользователе"
    )
    method = "get"


class UserMeDeleteDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("users_service")]
    operation_summary = "Удаление авторизованного пользователя"
    operation_description = "Удаление авторизованного пользователя"
    method = "delete"


class DisableNotificationsDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Отключение уведомлений пользователя"
    operation_description = "Отключение всех типов уведомлений пользователя."
    request_body = DisableNotificationsSerializer()
    method = "post"


class ResendActivationDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Повторная отправка письма для активации аккаунта"
    operation_description = (
        "Используйте этот метод для **повторной отправки электронного"
        " письма с активацией**.\nОбратите внимание, что электронное письмо "
        "не будет отправлено, если пользователь уже активен или у него нет "
        "подходящего пароля."
    )


class SetPasswordDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Изменение пароля авторизованного пользователя"
    operation_description = (
        "Используйте этот метод для для изменения пароля пользователя."
    )


class ResetPasswordDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Сброс пароля пользователя"
    operation_description = (
        "Используйте этот метод для отправки пользователю электронного "
        "письма со ссылкой для сброса пароля."
    )


class ResetPasswordConfirmDocs(BaseSwaggerSchema):
    tags = [DEFAULT_TAG]
    operation_summary = "Подтверждение сброса пароля"
    operation_description = (
        "Используйте этот метод для завершения процесса сброса пароля."
        "HTTP_400_BAD_REQUEST будет поднято, если пользователь вошел в "
        "систему или сменил пароль с момента создания токена."
    )


user_update_request_body = openapi.Schema(
    type=openapi.TYPE_OBJECT,
    required=[
        "email",
        "name",
        "person_telephone",
    ],
    properties={
        "email": openapi.Schema(
            title="Email",
            maxLength=50,
            minLength=5,
            type=openapi.TYPE_STRING,
        ),
        "name": openapi.Schema(
            title="Имя",
            maxLength=20,
            minLength=5,
            type=openapi.TYPE_STRING,
        ),
        "surname": openapi.Schema(
            title="Фамилия",
            maxLength=20,
            minLength=5,
            nullable=True,
            type=openapi.TYPE_STRING,
        ),
        "person_telephone": openapi.Schema(
            title="Номер телефона",
            maxLength=12,
            minLength=12,
            example="+71112223344",
            type=openapi.TYPE_STRING,
        ),
        "notifications": openapi.Schema(
            title="Уведомления",
            nullable=True,
            type=openapi.TYPE_ARRAY,
            items=openapi.Items(
                type=openapi.TYPE_STRING, enum=[*NOTIFICATION_CLASSES]
            ),
        ),
    },
)


class UserMePartialUpdateDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("users_service")]
    operation_summary = (
        "Частичное редактирование авторизованного " "пользователя"
    )
    operation_description = (
        "Используйте этот метод для полное редактирование авторизованного "
        "пользователя.\n\n"
        f"Доступные варианты notifications - {', '.join(NOTIFICATION_CLASSES)}"
    )
    request_body = user_update_request_body
    method = "patch"


class UserMeUpdateDocs(BaseSwaggerSchema):
    tags = [SWAGGER_TAGS.get("users_service")]
    operation_summary = "Полное редактирование авторизованного пользователя"
    operation_description = (
        "Используйте этот метод для полное редактирование авторизованного "
        "пользователя.\n\n"
        f"Доступные варианты notifications - {', '.join(NOTIFICATION_CLASSES)}"
    )
    request_body = user_update_request_body
    method = "put"
