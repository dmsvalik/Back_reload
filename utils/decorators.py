from functools import wraps
from django.http import HttpResponse
from main_page.models import UserQuota
from orders.models import OrderModel
from config.settings import MAX_SERVER_QUOTA, MAX_STORAGE_QUOTA, MAX_ORDERS
import magic


def check_user_quota(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        user_id = request.user.id
        try:
            user_quota = UserQuota.objects.get(user_id=user_id)
        except UserQuota.DoesNotExist:
            return HttpResponse("The user with the specified ID was not found", status=404)

        if user_quota.total_cloud_size >= MAX_STORAGE_QUOTA:
            return HttpResponse("Please free up space by deleting unnecessary files.", status=403)

        if user_quota.total_server_size >= MAX_SERVER_QUOTA:
            return HttpResponse("Please free up space by deleting unnecessary files.", status=403)

        if user_quota.total_traffic < 0:
            return HttpResponse(
                "The allowed traffic has been exceeded. Wait until next month or contact the administrators.", status=403,
            )

        return func(request, *args, **kwargs)

    return wrapped


def check_file_type(allowed_mime_types):
    def decorator(func):
        @wraps(func)
        def wrapped(request, *args, **kwargs):
            uploaded_file = request.FILES.get("upload_file")
            if "upload_file" not in request.FILES:
                return HttpResponse({'The "upload_file" key is missing in the uploaded files.'}, status=400)

            # Detect the file's MIME type
            file_type = magic.from_buffer(uploaded_file.read(1024), mime=True)

            # Check the MIME type against the list of allowed types
            if file_type not in allowed_mime_types:
                return HttpResponse(f"Unsupported file type: {file_type}", status=400)

            return func(request, *args, **kwargs)

        return wrapped

    return decorator


def check_order_limit(func):
    @wraps(func)
    def wrapped(request, *args, **kwargs):
        user_id = request.user.id
        user_order_count = OrderModel.objects.filter(
            user_id=user_id, offer_status=False
        ).count()
        if user_order_count >= MAX_ORDERS:
            return HttpResponse(
                "The order limit has been exceeded. Maximum number of orders: {}".format(MAX_ORDERS), status=403,
            )

        return func(request, *args, **kwargs)

    return wrapped
