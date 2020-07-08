from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from marketing.models import Interaksi
from marketing.forms import InteraksiForm


class InteraksiListView(generic.ListView):
    queryset = Interaksi.objects.all().order_by("-created_at")
    template_name = "marketing/interaksi_list.html"


@staff_member_required(login_url="accounts:login")
def createInteraksi(request):
    if request.method == "POST":
        form = InteraksiForm(request.POST)
        if form.is_valid():
            interaksi = form.save(commit=False)
            interaksi.tim_marketing = request.user
            interaksi.save()
            messages.success(request, "Interaksi berhasil ditambahkan")
            return redirect("marketing:list_interaksi")
    else:
        form = InteraksiForm()

    return render(
        request,
        "marketing/add_interaksi.html",
        {"form": form, "title": "Add Interaksi"},
    )


@staff_member_required(login_url="accounts:login")
def editInteraksi(request, pk):
    interaksi = get_object_or_404(Interaksi, pk=pk)
    if request.method == "POST":
        form = InteraksiForm(request.POST, instance=interaksi)
        if form.is_valid():
            form.save()
            messages.success(request, "Pendaftaran berhasil di edit!")
            return redirect("marketing:list_interaksi")
    else:
        form = InteraksiForm(instance=interaksi)

    context = {"form": form, "title": "Update Interaksi"}
    return render(request, "marketing/add_interaksi.html", context)


@staff_member_required(login_url="accounts:login")
def delete_interaksi(request, pk):
    interaksi = get_object_or_404(Interaksi, pk=pk)
    interaksi.delete()
    messages.success(request, "Interaksi berhasil di hapus")
    return redirect("marketing:list_interaksi")
