# in api/admin.py

from django.contrib import admin
from django.utils.html import format_html
from .models import Document

# This creates a custom view for the Document model in the admin
class DocumentAdmin(admin.ModelAdmin):
    list_display = ('original_filename', 'owner', 'uploaded_at', 'has_signature')
    readonly_fields = ('signature_image',) # Makes the signature display read-only

    # This function displays the signature image
    def signature_image(self, obj):
        if obj.signature:
            return format_html('<img src="{}" style="max-width: 400px; height: auto;" />', obj.signature)
        return "No Signature"
    signature_image.short_description = 'Signature Preview'
    
    # This function shows a checkmark in the list view if a signature exists
    def has_signature(self, obj):
        return bool(obj.signature)
    has_signature.boolean = True

# Register the custom admin view
admin.site.register(Document, DocumentAdmin)
