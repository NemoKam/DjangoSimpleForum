from authapp.models import UserRequest

def ip_statistic(get_response):
    def middleware(request):
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        ip = x_forwarded_for.split(',')[0] if x_forwarded_for else request.META.get('REMOTE_ADDR')
        user_req = UserRequest.objects.filter(ip=ip)
        if user_req:
            user_req[0].request_count = user_req[0].request_count + 1
            user_req[0].save()
        else:
            UserRequest.objects.create(ip=ip)
        response = get_response(request)
        return response
    return middleware