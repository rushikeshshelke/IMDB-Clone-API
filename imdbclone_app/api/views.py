from imdbclone_app.models import WatchList, StreamingPlatform, Review
from imdbclone_app.api.serializers import (
    WatchListSerializer,
    StreamingPlatformSerializer,
    ReviewSerializer
)
from rest_framework.response import Response
# from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import mixins
from rest_framework import generics
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated
from imdbclone_app.api.permissions import AdminOrReadOnly, ReviewUserOrReadOnly, AdminOnly
from rest_framework.authentication import BasicAuthentication
from rest_framework.throttling import UserRateThrottle, AnonRateThrottle, ScopedRateThrottle
from imdbclone_app.api.throttling import (
    ReviewCreateThrottle,
    ReviewListThrottle
)
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from imdbclone_app.api.pagination import WatchListPagination, WatchListLOPagination, WatchListCPPagination

## Generic views with mixins

# class ReviewList(mixins.ListModelMixin, mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer
    
#     def get(self, request, *args, **kwargs):
#         return self.list(request, *args, **kwargs)
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


# class ReviewDetail(mixins.RetrieveModelMixin, generics.GenericAPIView):
#     queryset = Review.objects.all()
#     serializer_class = ReviewSerializer

#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)
    
#     def delete(self, request, *args, **kwargs):
#         return self.destroy(request, *args, **kwargs)


## Generic view class

class UserReviewDetails(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated, AdminOnly]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        username = self.kwargs['username']
        return Review.objects.filter(review_user__username=username)


class MovieReviewDetails(generics.ListAPIView):
    
    permission_classes = [IsAuthenticated]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        username = self.request.query_params.get('username',None)
        return Review.objects.filter(review_user__username=username)


class ReviewList(generics.ListAPIView):
    # queryset = Review.objects.all()
    permission_classes = [IsAuthenticated]
    throttle_classes = [AnonRateThrottle, ReviewListThrottle]
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['review_user__username','active']
    
    def get_queryset(self):
        pk = self.kwargs['pk']
        return Review.objects.filter(watchlist=pk)
        

class ReviewDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [ReviewUserOrReadOnly]
    throttle_classes = [ScopedRateThrottle]
    throttle_scope = 'review-detail'
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    

class ReviewCreate(generics.CreateAPIView):
    
    permission_classes = [IsAuthenticated]
    throttle_classes = [ReviewCreateThrottle]
    serializer_class = ReviewSerializer
    
    def get_queryset(self):
        return Review.objects.all()
        
    def perform_create(self, serializer):
        pk = self.kwargs['pk']
        movie = WatchList.objects.get(pk=pk)
        
        user = self.request.user
        review_queryset = Review.objects.filter(watchlist=movie,review_user=user)
        
        if review_queryset.exists():
            raise ValidationError("You have already reviewed this watchlist!")

        if movie.total_reviews == 0:
            movie.avg_rating = serializer.validated_data['rating']
        else:
            movie.avg_rating = (movie.avg_rating + serializer.validated_data['rating']) / 2
        
        movie.total_reviews += 1
        movie.save()
        serializer.save(watchlist=movie, review_user=user)


class WatchListGV(generics.ListAPIView):
    permission_classes = [AdminOrReadOnly]
    serializer_class = WatchListSerializer
    # Filtering
    # filter_backends = [DjangoFilterBackend]
    # filterset_fields = ['title','active', 'platform__name']
    
    # Searching
    filter_backends = [filters.SearchFilter]
    search_fields = ['title','platform__name']
    pagination_class = WatchListCPPagination
    
    queryset = WatchList.objects.all()   
    

class WatchListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    def get(self,request):
        try:
            movies = WatchList.objects.all()
        except WatchList.DoesNotExist:
            content = {"error":"Movies not found"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
        
        serializer = WatchListSerializer(movies, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)  
        
    def post(self, request):
        serializer = WatchListSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class WatchDetailsAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
        except WatchList.DoesNotExist:
            content = {"error": "Movie not found"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)

        serializer = WatchListSerializer(movie)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        try:
            movie = WatchList.objects.get(pk=pk)
            serializer = WatchListSerializer(movie,data=request.data)
        except WatchList.DoesNotExist:
            serializer = WatchListSerializer(data=request.data)
            
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)        

    def delete(self, request, pk):
        movie = WatchList.objects.get(pk=pk)
        movie.delete()
        content = {"message": "Movie deleted successfully"}
        return Response(content,status=status.HTTP_204_NO_CONTENT)

class StreamingPlatformListAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request):
        try:
            platform = StreamingPlatform.objects.all()
        except StreamingPlatform.DoesNotExist:
            content = {"message": "Streaming platforms not found"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamingPlatformSerializer(platform,many=True)
        
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StreamingPlatformSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class StreamingPlatformDetailsAV(APIView):
    permission_classes = [AdminOrReadOnly]
    
    def get(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            content = {"error": "Streaming platform not found"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
        
        serializer = StreamingPlatformSerializer(platform)
        
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        platform = StreamingPlatform.objects.get(pk=pk)
        serializer = StreamingPlatformSerializer(platform,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, pk):
        try:
            platform = StreamingPlatform.objects.get(pk=pk)
        except StreamingPlatform.DoesNotExist:
            content = {"error": "Streaming platform not exists"}
            return Response(content,status=status.HTTP_404_NOT_FOUND)
        
        platform.delete()
        content = {"message":"Streaming platform deleted successfully"}
        return Response(content,status=status.HTTP_204_NO_CONTENT)

# @api_view(['GET','POST'])
# def movieList(request):
    
#     if request.method == 'GET':
#         try:
#             movies = Movie.objects.all()
#         except Movie.DoesNotExist:
#             content = {"error":"Movies not found"}
#             return Response(content,status=status.HTTP_404_NOT_FOUND)
        
#         serializer = WatchListSerializer(movies, many=True)
#         return Response(serializer.data,status=status.HTTP_200_OK)    

#     if request.method == 'POST':
#         serializer = WatchListSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

# @api_view(['GET','PUT','DELETE'])
# def movieDetails(request, pk):
    
#     if request.method == 'GET':
#         try:
#             movie = Movie.objects.get(pk=pk)
#         except Movie.DoesNotExist:
#             content = {"error": "Movie not found"}
#             return Response(content,status=status.HTTP_404_NOT_FOUND)

#         serializer = WatchListSerializer(movie)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     if request.method == 'PUT':
#         movie = Movie.objects.get(pk=pk)
#         serializer = WatchListSerializer(movie,data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data,status=status.HTTP_201_CREATED)
#         else:
#             return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
                
#     if request.method == 'DELETE':
#         movie = Movie.objects.get(pk=pk)
#         movie.delete()
#         content = {"message": "Movie deleted successfully"}
#         return Response(content,status=status.HTTP_204_NO_CONTENT)