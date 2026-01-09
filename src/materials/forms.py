from django import forms
from .models import Material


class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ["title", "description", "grade", "subject", "material_type", "file", "external_url"]

    def clean(self):
        cleaned = super().clean()
        file = cleaned.get("file")
        url = (cleaned.get("external_url") or "").strip()

        if not file and not url:
            raise forms.ValidationError("Укажите либо файл, либо ссылку.")

        if file and url:
            raise forms.ValidationError("Укажите что-то одно: либо файл, либо ссылку.")

        cleaned["external_url"] = url
        return cleaned