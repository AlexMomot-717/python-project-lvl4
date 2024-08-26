from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.utils.translation import gettext as _
from django.views import View
from task_manager.labels.forms import LabelForm
from task_manager.labels.models import Label
from task_manager.users.views import UserLoginRequiredMixin


class LabelsListView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        labels = Label.objects.all()
        return render(
            request,
            "labels_list.html",
            context={
                "labels": labels,
            },
        )


class LabelFormCreateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest) -> HttpResponse:
        form = LabelForm()
        return render(request, "create_label.html", {"form": form})

    def post(self, request: HttpRequest) -> HttpResponse:
        form = LabelForm(request.POST)
        if form.is_valid():
            form.save()
            message = _("label created successfully.")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("labels_list")
        return render(request, "create_label.html", {"form": form})


class LabelFormUpdateView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        label_id = kwargs.get("id")
        label = get_object_or_404(Label, pk=label_id)
        form = LabelForm(instance=label)
        context = {"form": form, "label_id": label_id}
        return render(request, "update_label.html", context=context)

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        label_id = kwargs.get("id")
        label = get_object_or_404(Label, pk=label_id)
        form = LabelForm(request.POST, instance=label)
        if form.is_valid():
            form.save()
            message = _("label has been updated successfully")
            messages.add_message(request, messages.SUCCESS, message)
            return redirect("labels_list")
        context = {"form": form, "label_id": label_id}
        return render(request, "update_label.html", context=context)


class LabelFormDeleteView(UserLoginRequiredMixin, View):
    def get(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        label_id = kwargs.get("id")
        label = get_object_or_404(Label, pk=label_id)
        return render(request, "delete_label.html", {"label": label})

    def post(self, request: HttpRequest, **kwargs: int | str) -> HttpResponse:
        label_id = kwargs.get("id")
        label = get_object_or_404(Label, pk=label_id)
        tasks_with_this_label = get_object_or_404(Label, pk=label_id).task_set.all()
        if tasks_with_this_label:
            message = _("It is not possible to delete the label because it is in use")
            messages.add_message(request, messages.ERROR, message)
        else:
            label.delete()
            message = _("label has been deleted successfully")
            messages.add_message(request, messages.SUCCESS, message)
        return redirect("labels_list")
