from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.db import transaction
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods, require_safe
from django.conf.urls import handler500
from .forms import SignUpForm, UserEditForm, WatchForm
from .models import Watch, Order, OrderItem
import json
from django.contrib import messages
from django.http import JsonResponse
from library.email_lib import send_email_notification


@require_safe
def home(request):
    watches = Watch.objects.all()
    return render(request, 'home.html', {"watches": watches})

@require_safe
def aboutus(request):
    return render(request, 'aboutus.html')


@login_required
def orders(request):
    if request.user.username == 'admin':
        orders = Order.objects.filter(status="pending").order_by("-created_at")
    else:
        orders = Order.objects.filter(user=request.user, status="pending").order_by("-created_at")
    return render(request, 'orders.html', {"orders": orders})


@login_required
def history(request):
    if request.user.username == 'admin':
        orders = Order.objects.all().exclude(status="pending").order_by("-created_at")
    else:
        orders = Order.objects.filter(user=request.user).exclude(status="pending").order_by("-created_at")
    return render(request, 'history.html', {"orders": orders})


@login_required
def cancel_order(request, id):
    try:
        order = Order.objects.get(id=id)
        order.status = "canceled"
        order.save()

        email_response = send_email_notification(
            recipient_email=order.user.email,
            order_status="Canceled",
            order_id=order.id
        )

        if email_response["status"] == "success":
            messages.success(request, "Order canceled successfully and notification sent.")
        else:
            messages.error(request, f"Failed to send notification email. Error: {email_response['message']}")
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")

    return redirect('orders')


@require_http_methods(["GET", "POST"])
def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html')
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(username=email, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html')
    return render(request, 'login.html')


@login_required
def logout_user(request):
    logout(request)
    return redirect('login')


@require_http_methods(["GET", "POST"])
@transaction.atomic
def register_user(request):
    try:
        if request.method == 'GET':
            user_form = SignUpForm()
            return render(request, 'signup.html', {"u_form": user_form})
        if request.method == 'POST':
            user_form = SignUpForm(request.POST)
            if user_form.is_valid():
                user = user_form.save()
                user.save()
                return redirect('login')
            else:
                for field in user_form.errors:
                    user_form[field].field.widget.attrs['class'] += ' error'
                return render(request, 'signup.html', {"u_form": user_form})
    except Exception:
        return redirect(handler500)


@login_required
def user_details(request):
    try:
        if request.user.is_authenticated:
            if request.method == "POST":
                user_form = UserEditForm(request.POST, instance=request.user)
                if user_form.is_valid():
                    user_form.save()
                    return redirect('user_details')
                else:
                    for field in user_form.errors:
                        user_form[field].field.widget.attrs['class'] += ' error'
                    return render(request, 'user_details.html', {"u_form": user_form})
            else:
                user_form = UserEditForm(instance=request.user)
            return render(request, 'user_details.html', {"u_form": user_form})
    except Exception:
        return redirect(handler500)


def watch_list(request):
    if request.method == 'GET':
        watches = Watch.objects.all()
        return render(request, 'watch.html', {"watches": watches})
    return render(request, 'watch.html')

@login_required
def add_watch(request):
    if request.method == 'POST':
        form = WatchForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, "Watch added successfully!")
            return redirect('watch')
        else:
            for field in form.errors:
                form[field].field.widget.attrs['class'] += ' error'
    else:
        form = WatchForm()
    return render(request, 'add_watch.html', {'form': form})



@login_required
def watch_form_add_update(request, id=0):
    try:
        if request.method == 'GET':
            if id == 0:
                m_form = WatchForm()
            else:
                watch = Watch.objects.get(id=id)
                m_form = WatchForm(instance=watch)
            return render(request, 'watch_form.html', {'m_form': m_form})
        if request.method == 'POST':
            if id == 0:
                m_form = WatchForm(request.POST, request.FILES)
            else:
                watch = Watch.objects.get(id=id)
                m_form = WatchForm(request.POST, request.FILES, instance=watch)
            if m_form.is_valid():
                m_form.save()
            else:
                for field in m_form.errors:
                    m_form[field].field.widget.attrs['class'] += ' error'
                return render(request, 'watch_form.html', {'m_form': m_form})
            return redirect('watch')
        return render(request, 'add_watch.html')
    except Exception as e:
        print(e)
        return redirect(handler500)


@login_required
def delete_watch(request, id):
    try:
        if request.method == 'GET':
            item = Watch.objects.get(id=id)
            item.delete()
            return redirect('watch')
        return render(request, 'watch.html')
    except Exception:
        return redirect(handler500)


@login_required
def complete_order(request, id):
    try:
        order = Order.objects.get(id=id)
        order.status = "completed"
        order.save()

        email_response = send_email_notification(
            recipient_email=order.user.email,
            order_status="Completed",
            order_id=order.id
        )

        if email_response["status"] == "success":
            messages.success(request, "Order completed successfully and notification sent.")
        else:
            messages.error(request, f"Failed to send notification email. Error: {email_response['message']}")

    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
    except Exception as e:
        messages.error(request, f"An unexpected error occurred: {str(e)}")

    return redirect('orders')


@login_required
def place_order(request):
    if request.method == "POST":
        data = json.loads(request.body)
        cart = data.get("cart", [])
        order = Order.objects.create(user=request.user)

        for item in cart:
            watch = Watch.objects.get(id=item["id"])
            OrderItem.objects.create(order=order, watch=watch, quantity=item["quantity"])

        return JsonResponse({"success": True, "message": "Order placed successfully!"})

    return JsonResponse({"success": False, "message": "Invalid request"}, status=400)
