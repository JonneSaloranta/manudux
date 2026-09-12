from django.db import connection
from django.db.utils import Error as DjangoDBError
from django.http import JsonResponse


def healthz(request):
    """Liveness/readiness probe for container orchestration."""
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
    except DjangoDBError:
        return JsonResponse({"status": "error"}, status=503)
    return JsonResponse({"status": "ok"})
