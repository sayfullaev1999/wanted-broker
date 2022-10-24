from django.core.management.base import BaseCommand
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


class Command(BaseCommand):
    help = 'Connect to polygon'

    def handle(self, *args, **options):
        async_to_sync(get_channel_layer().send)("polygon", {"type": "connect_polygon"})
        self.stdout.write(self.style.SUCCESS('Successfully connected'))
