# backend/app/services/translation_service.py
from typing import Dict

class TranslationService:
    def __init__(self):
        self.translations: Dict[str, Dict[str, str]] = {
            "fr": {
                "period": "Les menstruations sont un processus naturel mensuel...",
                "cycle": "Le cycle menstruel dure généralement 28 jours...",
                "symptoms": "Les symptômes courants comprennent...",
                "help": "CouldYou? fournit des produits menstruels...",
            }
        }

    def translate(self, text: str, target_lang: str) -> str:
        if target_lang == "en":
            return text

        if target_lang in self.translations:
            # Basic translation lookup
            for key, value in self.translations[target_lang].items():
                if key in text.lower():
                    return value

        return text  # Fallback to original text if no translation found
