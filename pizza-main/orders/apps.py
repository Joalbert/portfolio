from django.apps import AppConfig


class OrdersConfig(AppConfig):
    name = 'orders'
    default_auto_field = 'django.db.models.BigAutoField'

    def ready(self):
        import orders.signals
        return super().ready()
