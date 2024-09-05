from django.http import JsonResponse


def handler404(request, exception):
    message=('Route not found')
    response=JsonResponse({"error": message})
    response.status_code=404
    return response

def handler500(request):
    message=('internal server error')
    response=JsonResponse(data={"error":message})
    response.status_code=500
    return response