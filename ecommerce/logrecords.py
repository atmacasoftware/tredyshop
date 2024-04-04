from django.http import HttpResponse


def log_records(current_time, message, status):
    f = open(f'log_{current_time}.txt', 'w+', encoding='utf-8')
    f.write(message)
    f.close()
    return HttpResponse()