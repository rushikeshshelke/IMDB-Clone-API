from rest_framework import serializers
from imdbclone_app.models import WatchList, StreamingPlatform, Review

## Model serializer

class ReviewSerializer(serializers.ModelSerializer):
    review_user = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Review
        # fields = "__all__"
        exclude = ['watchlist']
        

class WatchListSerializer(serializers.ModelSerializer):
    # reviews = ReviewSerializer(many=True,read_only=True)
    platform = serializers.CharField(source='platform.name')
    
    class Meta:
        model = WatchList
        fields = "__all__"
        # exclude = ['id']
    
    def create(self, validated_data):
        return WatchList.objects.create(**validated_data)


class StreamingPlatformSerializer(serializers.ModelSerializer):
    watchlist = WatchListSerializer(many=True,read_only=True)
    
    # watchlist = serializers.StringRelatedField(many=True,read_only=True)
    
    # watchlist = serializers.HyperlinkedRelatedField(
    #     many=True,
    #     read_only=True,
    #     view_name='movie-detail'
    # )
    
    class Meta:
        model = StreamingPlatform
        fields = "__all__"


# def name_length(value):
#     if len(value) < 2:
#         raise serializers.ValidationError("Name is too short!")
#     elif len(value) > 30:
#         raise serializers.ValidationError("Name is too long!")    

# class MovieSerializer(serializers.Serializer):
#     id = serializers.IntegerField(read_only=True)
#     name = serializers.CharField(validators=[name_length])
#     description = serializers.CharField()
#     active = serializers.BooleanField()

#     def create(self, validated_data):
#         return Movie.objects.create(**validated_data)
    
#     def update(self, instance, validated_data):
#         instance.name = validated_data.get('name', instance.name)
#         instance.description = validated_data.get('description',instance.description)
#         instance.active = validated_data.get('active',instance.active)
#         instance.save()
        
#         return instance
    
#     ## Field level validations
#     # def validate_name(self, value):
#     #     if len(value) < 2:
#     #         raise serializers.ValidationError("Name is too short!")
#     #     elif len(value) > 30:
#     #         raise serializers.ValidationError("Name is too long!")
#     #     else:
#     #         return value
    
#     ## Object level validations
#     def validate(self, data):
#         if data.get('name') == data.get('description'):
#             raise serializers.ValidationError("name and description should not be same!")
        
#         return data