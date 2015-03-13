from uliweb import settings
from celery import Celery

app = None


def after_init_apps(sender):
    global app
    app = Celery('uliweb')

    from celery.schedules import crontab

    celery_config = settings.CELERY
    for key in settings.CELERY.CELERYBEAT_SCHEDULE.keys():
        cron_args = settings.CELERY.CELERYBEAT_SCHEDULE[
            key].get('schedule', '')
        if isinstance(cron_args, dict):
            settings.CELERY.CELERYBEAT_SCHEDULE[key]['schedule'] = crontab(
                **cron_args)

    # finding tasks in installed apps
    installed_apps = [item[0] if isinstance(item,
                                            tuple) else item for item in settings.GLOBAL.INSTALLED_APPS]

    app.config_from_object(dict(settings.CELERY))
    app.autodiscover_tasks(lambda: installed_apps)
