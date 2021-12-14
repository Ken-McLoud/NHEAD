from django.urls import path
from . import views

urlpatterns = []


# added by autocrud
urlpatterns.append(
    path("createfamily", views.CreateFamilyView.as_view(), name="createfamily")
)

# added by autocrud
urlpatterns.append(
    path("familymodel/<int:pk>", views.DetailFamilyView.as_view(), name="familymodel")
)

# added by autocrud
urlpatterns.append(
    path("familymodels", views.ListFamilyView.as_view(), name="familymodels")
)

# added by autocrud
urlpatterns.append(
    path("editfamily/<int:pk>", views.EditFamilyView.as_view(), name="editfamily")
)

# added by autocrud
urlpatterns.append(
    path("deletefamily/<int:pk>", views.DeleteFamilyView.as_view(), name="deletefamily")
)
