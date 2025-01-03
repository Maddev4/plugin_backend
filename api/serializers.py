from rest_framework import serializers
from .models import Slide, Deck

class SlideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Slide
        fields = ['slide_id', 'slide_num', 'file_name', 'date_uploaded', 'content']

class DeckSerializer(serializers.ModelSerializer):
    storyline_slides = serializers.SerializerMethodField()

    class Meta:
        model = Deck
        fields = ['deck_id', 'storyline_slides']

    def get_storyline_slides(self, obj):
        sections = ['introSection', 'industryOverview', 'productOverview', 'caseStudy', 'conclusion']
        return {
            section: {
                'main': [],
                'sub': SlideSerializer(obj.slides.filter(content__tags__contains=section), many=True).data
            }
            for section in sections
        } 