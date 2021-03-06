from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views import generic
from django.db.utils import IntegrityError
from marketing.models import Interaksi
from marketing.forms import InteraksiForm


class InteraksiListView(generic.ListView):
    queryset = Interaksi.objects.all().order_by("-created_at")
    template_name = "marketing/interaksi_list.html"


@staff_member_required(login_url="accounts:login")
def createInteraksi(request):
    if request.method == "POST":
        if request.POST["no_hp"]:
            # format no hp to 62xxx
            request.POST["no_hp"][0][1:].replace(" ", "").replace("-", "")
            request.POST._mutable = True
            if request.POST["no_hp"].startswith("0"):
                request.POST["no_hp"] = "62" + request.POST["no_hp"][1:].replace(
                    " ", ""
                ).replace("-", "")
            elif request.POST["no_hp"].startswith("+"):
                request.POST["no_hp"] = (
                    request.POST["no_hp"][1:].replace(" ", "").replace("-", "")
                )
            elif request.POST["no_hp"].startswith("6"):
                request.POST["no_hp"] = (
                    request.POST["no_hp"].replace(" ", "").replace("-", "")
                )

        form = InteraksiForm(request.POST)
        if form.is_valid():
            interaksi = form.save(commit=False)
            interaksi.tim_marketing = request.user
            try:
                interaksi.save()
            except IntegrityError:
                messages.error(request, "Data sudah ada pada hari ini")
                return redirect("marketing:list_interaksi")

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


@staff_member_required(login_url="accounts:login")
def interaksi_bulanan(request):
    return render(request, "marketing/interaksi_graph.html")
