from django.urls import path
# from imdbclone_app.api.views import movieDetails, movieList
from imdbclone_app.api.views import (
    WatchDetailsAV,
    WatchListAV,
    StreamingPlatformListAV,
    StreamingPlatformDetailsAV,
    ReviewList,
    ReviewDetail,
    ReviewCreate,
    UserReviewDetails,
    MovieReviewDetails,
    WatchListGV
)

urlpatterns = [
    # path('list/',movieList, name='movie-list'),
    # path('<int:movieID>',movieDetails, name="movie-details"),
    path('list/',WatchListAV.as_view(), name='watchlist-list'),
    path('list2/',WatchListGV.as_view(),name='watchlist-list'),
    path('<int:pk>/',WatchDetailsAV.as_view(), name='watchlist-detail'),
    
    path('streaming/',StreamingPlatformListAV.as_view(), name='streamingplatform-list'),
    path('streaming/<int:pk>',StreamingPlatformDetailsAV.as_view(), name='streamingplatform-detail'),
    
    # path('reviews/',ReviewList.as_view(), name='review-list'),
    # path('reviews/<int:pk>',ReviewDetail.as_view(), name='review-detail'),
    
    path('<int:pk>/reviews/',ReviewList.as_view(), name='review-list'),
    path('<int:pk>/review-create/',ReviewCreate.as_view(), name='review-create'),
    path('review/<int:pk>/',ReviewDetail.as_view(), name='review-detail'),
    
    path('reviews/<str:username>/',UserReviewDetails.as_view(), name='user-review-detail'),
    path('reviews/',MovieReviewDetails.as_view(), name='movie-review-detail'),
]