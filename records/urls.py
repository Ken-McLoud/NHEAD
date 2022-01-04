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
urlpatterns.append(path("editfamily/<int:pk>", views.editfamilyview, name="editfamily"))

# added by autocrud
urlpatterns.append(
    path("deletefamily/<int:pk>", views.DeleteFamilyView.as_view(), name="deletefamily")
)


# added by autocrud
urlpatterns.append(path("createkid/", views.createkidview, name="createkid"))

# added by autocrud
urlpatterns.append(
    path("kidmodel/<int:pk>", views.DetailKidView.as_view(), name="kidmodel")
)

# added by autocrud
urlpatterns.append(path("kidmodels", views.ListKidView.as_view(), name="kidmodels"))

# added by autocrud
urlpatterns.append(
    path("editkid/<int:pk>", views.EditKidView.as_view(), name="editkid")
)

# added by autocrud
urlpatterns.append(
    path("deletekid/<int:pk>", views.DeleteKidView.as_view(), name="deletekid")
)

# added by autocrud
urlpatterns.append(path("myfamily/", views.MyFamilyView.as_view(), name="myfamily"))

urlpatterns.append(
    path("inline_add_kid/<int:family_pk>", views.inline_add_kid, name="inline_add_kid")
)

urlpatterns.append(
    path(
        "inline_edit_family/<int:family_pk>",
        views.inline_edit_family,
        name="inline_edit_family",
    )
)
