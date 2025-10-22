import os
import mimetypes
from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.management.base import BaseCommand
from module.models import Module


class Command(BaseCommand):
    help = "Loads data into modules table"

    def handle(self, *args, **options):
        modules = [
            {
                "title": "Send Payment",
                "description": "Easily pay your rent through cash or GCash.",
                "image": "uploads/send-payment-banner.png",
                "redirect_url": "/pay",
                "order": 1,
                "is_active": True
            },
            {
                "title": "Payment History",
                "description": "View and track all your previous rent payments in one place.",
                "image": "uploads/payment-history-banner.png",
                "redirect_url": "/payments",
                "order": 2,
                "is_active": True
            },
            {
                "title": "Submit a Request",
                "description": "Need maintenance, cleaning, or have a concern? Send your request here.",
                "image": "uploads/request-banner.png",
                "redirect_url": "/request",
                "order": 3,
                "is_active": False
            }
        ]

        SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

        for module in modules:
            relative_image_path = module.get('image')
            absolute_image_path = os.path.join(SCRIPT_DIR, relative_image_path)
            module_data = module.copy()

            try:
                with open(absolute_image_path, 'rb') as f:
                    image_content = f.read()

                file_name = os.path.basename(absolute_image_path)

                content_type, _ = mimetypes.guess_type(file_name)

                if not content_type:
                    content_type = 'application/octet-stream'

                uploaded_file = SimpleUploadedFile(
                    name=file_name,
                    content=image_content,
                    content_type=content_type
                )

                module_data['image'] = uploaded_file

                module, created = Module.objects.get_or_create(
                    title=module_data['title'],
                    defaults=module_data
                )

                print(f"✅ Successfully created new Module: {module.title}")
            except Exception as e:
                print(f"❌ Error creating module '{module['title']}': {e}")
