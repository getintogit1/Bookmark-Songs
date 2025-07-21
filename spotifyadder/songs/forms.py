
from django import forms
from .models import Song

import re

class SongCreateForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title","album", "artist", "description"]
      



    def clean_title(self):
        title = self.cleaned_data.get("title", "")
        bad_words = ["Music Video", "Official", "Explicit", "feat", "featuring", "ft", "feature"]
        for w in bad_words:
            pattern = r"\b{}\b".format(re.escape(w))
            title = re.sub(pattern, "", title, flags=re.IGNORECASE)

        title = re.sub(r"\s{2,}", " ", title).strip()
        return title

class SongEditForm(forms.ModelForm):
    class Meta:
        model = Song
        fields = ["title","album", "artist", "description", "image"]
