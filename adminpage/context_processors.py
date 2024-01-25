from adminpage.models import Notification


def okunmamis_bildirimler(request):
    if request.user.is_authenticated:
        notify = Notification.objects.filter(is_read=False, user=request.user)
        notify_count = Notification.objects.filter(is_read=False, user=request.user).count()
        return dict(notify=notify, notify_count=notify_count)
    else:
        return dict(notify=False)