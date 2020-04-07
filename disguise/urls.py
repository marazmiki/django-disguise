from django.urls import path

from .views import Mask, MaskById, Unmask

urlpatterns = [
    path('', Mask.as_view(), name='disguise_mask'),
    path('<int:pk>/', MaskById.as_view(), name='disguise_mask'),
    path('remove/', Unmask.as_view(), name='disguise_unmask'),
]
