from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.conf import settings
from .models import Cart, Medicine, Order, Bill, BillItem
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
import csv
import io
from django.core.paginator import Paginator
import pandas as pd
import os
from django.http import JsonResponse
import json
from django.utils import timezone
from django.db import transaction
from fuzzywuzzy import process
import uuid
import random
import razorpay

@login_required(login_url='/login/')
def home(request):
    query = request.GET.get('q')

    if query:
        medicines = Medicine.objects.filter(
            Q(name__icontains=query) | Q(company__icontains=query)
        )
        all_names = Medicine.objects.values_list('name', flat=True)

        match = process.extractOne(query, all_names)

        if match:
            best_match, score = match

            if score > 70:  
                medicines = medicines | Medicine.objects.filter(
                    name__icontains=best_match
                )
    else:
        medicines = Medicine.objects.all()

    paginator = Paginator(medicines, 12)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'home.html', {'page_obj': page_obj})


def login_view(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)
            user = authenticate(request, username=user.username, password=password)
        except User.DoesNotExist:
            user = None

        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            return render(request, 'login.html', {'error': 'Invalid Credentials ❌'})

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('/login/')


def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already exists ❌'})

        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already exists ❌'})

        if password != confirm_password:
            return render(request, 'signup.html', {'error': 'Passwords do not match ❌'})

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        login(request, user)
        return redirect('/')

    return render(request, 'signup.html')

@login_required(login_url='/login/')
def profile_view(request):
    user = request.user
    message = None
    error = None

    if request.method == "POST":
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        password2 = request.POST.get('password2', '')

        if username and username != user.username:
            if User.objects.filter(username=username).exclude(pk=user.pk).exists():
                error = 'Username already exists ❌'
            else:
                user.username = username

        if email and email != user.email:
            if User.objects.filter(email=email).exclude(pk=user.pk).exists():
                error = 'Email already exists ❌'
            else:
                user.email = email

        if password or password2:
            if password != password2:
                error = 'Passwords do not match ❌'
            elif len(password) < 6:
                error = 'Password must be at least 6 characters ❌'
            else:
                user.set_password(password)

        if not error:
            user.save()

            if password:
                login(request, user)

            message = 'Profile updated successfully ✅'

    return render(request, 'profile.html', {'message': message, 'error': error})

@login_required(login_url='/login/')
def add_to_cart(request):
    if request.method == "POST":
        medicine_id = request.POST['medicine_id']
        medicine = get_object_or_404(Medicine, id=medicine_id)

        cart_item = Cart.objects.filter(user=request.user, medicine=medicine).first()

        if cart_item:
            cart_item.quantity += 1
            cart_item.save()
        else:
            Cart.objects.create(
                user=request.user,
                medicine=medicine,
                quantity=1
            )

        return redirect('/')
    
@login_required(login_url='/login/')    
def cart_view(request):
    cart_items = Cart.objects.filter(user=request.user)

    grand_total = 0
    has_prescription_items = False

    for item in cart_items:
        item.total = item.quantity * item.medicine.price
        grand_total += item.total
        if item.medicine.requires_prescription:
            has_prescription_items = True

    return render(request, 'cart.html', {
        'cart_items': cart_items,
        'grand_total': grand_total,
        'has_prescription_items': has_prescription_items
    })

def remove_from_cart(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        cart_item = Cart.objects.get(id=item_id, user=request.user)
        cart_item.delete()
        return redirect('/cart/')
    
def update_cart(request):
    if request.method == "POST":
        item_id = request.POST['item_id']
        action = request.POST['action']

        cart_item = Cart.objects.filter(id=item_id, user=request.user).first()

        if cart_item:
            if action == "increase":
                cart_item.quantity += 1
                cart_item.save()

            elif action == "decrease":
                cart_item.quantity -= 1
                if cart_item.quantity <= 0:
                    cart_item.delete()
                else:
                    cart_item.save()

        return redirect('/cart/')

@login_required(login_url='/login/')
def create_payment(request):
    cart_items = Cart.objects.filter(user=request.user)

    print("Cart items:", cart_items)
    print("Count:", cart_items.count())

    if not cart_items.exists():
        return redirect('/cart/')

    total = sum(item.quantity * item.medicine.price for item in cart_items)
    amount_paise = int(total * 100)

    client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

    payment = client.order.create({
        "amount": amount_paise,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "payment.html", {
        "cart_items": cart_items,   
        "payment": payment,
        "total": total,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })
            
from django.views.decorators.csrf import csrf_exempt
import json

@csrf_exempt
def verify_payment(request):
    data = json.loads(request.body)

    try:
        orders = Order.objects.filter(
            user=request.user,
            payment_status="pending"
        )

        for order in orders:
            order.razorpay_payment_id = data.get('razorpay_payment_id')
            order.razorpay_signature = data.get('razorpay_signature')
            order.payment_status = "success"
            order.status = "pending"
            order.save()

        return JsonResponse({"status": "success"})

    except:
        return JsonResponse({"status": "failed"})
        
@login_required
def payment_success(request):
    cart_items = Cart.objects.filter(user=request.user)

    for item in cart_items:
        Order.objects.create(
            user=request.user,
            medicine=item.medicine,
            quantity=item.quantity,
            prescription_file=item.prescription_file,  
            payment_status="paid",
            status="pending"
        )

    cart_items.delete()

    return redirect('order_success')

def payment_failed(request):
    return render(request, 'failed.html')

@require_POST
@login_required(login_url='/login/')
def checkout(request):
    cart_items = Cart.objects.filter(user=request.user)

    if not cart_items.exists():
        return redirect('/cart/')

    for item in cart_items:
        if item.medicine.requires_prescription:
            return redirect('upload_prescriptions')   

    return redirect('create_payment')

@login_required(login_url='/login/')
def upload_prescriptions(request):
    cart_items = Cart.objects.filter(user=request.user)
    
    prescription_items = []
    for item in cart_items:
        if item.medicine.requires_prescription:
            prescription_items.append(item)
    
    if not prescription_items:
        return redirect('/checkout/')
    
    if request.method == "POST":
        for item in prescription_items:
            file_key = f'prescription_{item.id}'
            prescription_file = request.FILES.get(file_key)

            if not prescription_file:
                return render(request, 'upload_prescriptions.html', {
                    'prescription_items': prescription_items,
                    'error': 'Upload all prescriptions'
                })

            item.prescription_file = prescription_file
            item.save()

        return redirect('create_payment')

    return render(request, 'upload_prescriptions.html', {
        'prescription_items': prescription_items
    })

def order_success(request):
    return render(request, 'success.html')

@login_required(login_url='/login/')
def orders_view(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    for order in orders:
        order.total = order.quantity * order.medicine.price

    paginator = Paginator(orders, 10)  
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'orders.html', {'page_obj': page_obj})


@login_required(login_url='/login/')
def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.total = order.quantity * order.medicine.price
    return render(request, 'order_detail.html', {'order': order})


def dashboard(request):
    if not request.user.is_superuser:
        return redirect('/')   

    medicines = Medicine.objects.all()
    return render(request, 'dashboard.html', {'medicines': medicines})

def add_medicine(request):
    if request.method == "POST" and request.user.is_superuser:
        name = request.POST['name']
        price = request.POST['price']
        company = request.POST['company']
        size = request.POST['size']
        image = request.POST['image']
        requires_prescription = request.POST.get('requires_prescription') == 'on'

        Medicine.objects.create(
            name=name,
            price=price,
            company=company,
            size=size,
            image=image,
            requires_prescription=requires_prescription
        )

    return redirect('/dashboard/')


@login_required
def upload_medicines_csv(request):
    if not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        
        if csv_file.name.endswith(('.xlsx', '.xls')):
            df = pd.read_excel(csv_file)
            for _, row in df.iterrows():
                Medicine.objects.create(
                    name=row['name'],
                    price=float(row['price']),
                    company=row['company'],
                    size=row['size'],
                    image=row['image']
                )
        else:
            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.DictReader(io_string)
            
            for row in reader:
                Medicine.objects.create(
                    name=row['name'],
                    price=float(row['price']),
                    company=row['company'],
                    size=row['size'],
                    image=row['image']
                )
        
        return redirect('/dashboard/')

    return redirect('/dashboard/')


def delete_medicine(request):
    if request.method == "POST" and request.user.is_superuser:
        med_id = request.POST['med_id']
        medicine = Medicine.objects.filter(id=med_id).first()

        if medicine:
            medicine.delete()

    return redirect('/dashboard/')

def edit_medicine(request, id):
    if not request.user.is_superuser:
        return redirect('/')

    medicine = Medicine.objects.filter(id=id).first()

    if request.method == "POST":
        medicine.name = request.POST['name']
        medicine.price = request.POST['price']
        medicine.company = request.POST['company']
        medicine.size = request.POST['size']
        medicine.image = request.POST['image']
        medicine.requires_prescription = request.POST.get('requires_prescription') == 'on'

        medicine.save()
        return redirect('/dashboard/')

    return render(request, 'edit_medicine.html', {'medicine': medicine})

def medicine_detail(request, id):
    medicine = Medicine.objects.filter(id=id).first()
    return render(request, 'medicine_detail.html', {'medicine': medicine})

def admin_orders(request):
    if not request.user.is_superuser:
        return redirect('/')

    orders = Order.objects.all().order_by('-created_at')

    for order in orders:
        order.total = order.quantity * order.medicine.price

    paginator = Paginator(orders, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'admin_orders.html', {'page_obj': page_obj})

@login_required(login_url='/login/')
def admin_order_detail(request, order_id):
    if not request.user.is_superuser:
        return redirect('/')

    order = get_object_or_404(Order, id=order_id)
    order.total = order.quantity * order.medicine.price

    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
            return redirect('admin_order_detail', order_id=order.id)

    return render(request, 'admin_order_detail.html', {'order': order})


@login_required(login_url='/login/')
def update_order_status(request, order_id):
    if not request.user.is_superuser:
        return redirect('/')

    if request.method == 'POST':
        order = get_object_or_404(Order, id=order_id)
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()

    return redirect('admin_orders')


def add_to_bill(request):
    if request.method == "POST":
        medicine_id = request.POST['medicine_id']
        quantity = int(request.POST['quantity'])

        bill_items = request.session.get('bill_items', [])

        bill_items.append({
            "medicine_id": medicine_id,
            "quantity": quantity
        })

        request.session['bill_items'] = bill_items

    return redirect('/billing/')

def billing(request):
    medicines = Medicine.objects.all().order_by('name')

    bill_items = request.session.get('bill_items', [])
    customer = request.session.get('customer')

    detailed_items = []
    grand_total = 0

    for item in bill_items:
        medicine = Medicine.objects.filter(id=item['medicine_id']).first()

        if medicine:
            total = medicine.price * item['quantity']
            grand_total += total

            detailed_items.append({
                'name': medicine.name,
                'price': medicine.price,
                'quantity': item['quantity'],
                'total': total
            })

    return render(request, 'billing.html', {
        'medicines': medicines,
        'bill_items': detailed_items,
        'grand_total': grand_total,
        'customer': customer
    })
    
def set_customer(request):
    if request.method == "POST":
        request.session['customer'] = {
            "name": request.POST['customer_name'],
            "mobile": request.POST['mobile'],
            "email": request.POST.get('email')
}
    return redirect('/billing/')

def add_to_bill(request):
    if request.method == "POST":
        medicine_id = request.POST['medicine_id']
        quantity = request.POST.get('quantity')

        if not quantity:
            return redirect('/billing/')

        quantity = int(quantity)

        if quantity <= 0:
            return redirect('/billing/')

        bill_items = request.session.get('bill_items', [])

        bill_items.append({
            "medicine_id": medicine_id,
            "quantity": quantity
        })

        request.session['bill_items'] = bill_items

    return redirect('/billing/')


from datetime import datetime

def generate_bill(request):
    customer = request.session.get('customer')
    bill_items = request.session.get('bill_items', [])

    if not customer or not bill_items:
        return redirect('/billing/')

    bill = Bill.objects.create(
        customer_name=customer['name'],
        mobile=customer['mobile'],
        email=customer.get('email'),
        total_amount=0
    )

    grand_total = 0

    for item in bill_items:
        medicine = Medicine.objects.filter(id=item['medicine_id']).first()

        if medicine:
            total = medicine.price * item['quantity']
            grand_total += total

            BillItem.objects.create(
                bill=bill,
                medicine=medicine,
                quantity=item['quantity'],
                price=medicine.price
            )

    bill.total_amount = grand_total
    bill.save()

    items = BillItem.objects.filter(bill=bill)

    pdf = generate_pdf(bill, items)

    request.session['bill_items'] = []
    request.session['customer'] = {}

    filename = f"bill_{bill.id}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return redirect(f'/invoice/{bill.id}/')

def generate_pdf(bill, items):
    template = get_template('invoice_pdf.html')

    html = template.render({
        'bill': bill,
        'items': items,
        'current_datetime': timezone.now()
    })

    result = BytesIO()
    pisa.CreatePDF(html, dest=result)

    result.seek(0)  
    return result

def invoice(request, id):
    bill = Bill.objects.filter(id=id).first()
    items = BillItem.objects.filter(bill=bill)
    for item in items:
        item.total = item.price * item.quantity
    return render(request, 'invoice.html', {
        'bill': bill,
        'items': items
    })

def remove_from_bill(request):
    if request.method == "POST":
        index = int(request.POST['index'])

        bill_items = request.session.get('bill_items', [])

        if 0 <= index < len(bill_items):
            bill_items.pop(index)

        request.session['bill_items'] = bill_items

    return redirect('/billing/')

def update_bill(request):
    if request.method == "POST":
        index = int(request.POST['index'])
        quantity = int(request.POST['quantity'])

        bill_items = request.session.get('bill_items', [])

        if 0 <= index < len(bill_items):

            if quantity <= 0:
                bill_items.pop(index)
            else:
                bill_items[index]['quantity'] = quantity

        request.session['bill_items'] = bill_items

    return redirect('/billing/')

def download_invoice(request, id):
    bill = Bill.objects.filter(id=id).first()
    items = BillItem.objects.filter(bill=bill)
    for item in items:
        item.total = item.price * item.quantity
    pdf = generate_pdf(bill, items)

    filename = f"bill_{bill.id}_{datetime.now().strftime('%Y%m%d_%H%M')}.pdf"

    response = HttpResponse(pdf.getvalue(), content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="{filename}"'

    return response

from .forms import MedicineForm
def add_form_demo(request):
    if request.method == "POST":
        form = MedicineForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponse("Saved Successfully")
    else:
        form = MedicineForm()
    return render(request, 'form_demo.html', {'form': form})