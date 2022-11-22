import json

# from order.forms import OrderForm
from core.views import *
# Create your views here.
from order.models import Order, Payment, Transactions


def order_payment(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        mobile = request.POST.get("mobile")
        amount = request.POST.get("amount")
        payment_id = request.POST.get("razorpay_payment_id", "")
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        razorpay_order = client.order.create(
            {"amount": int(amount) * 100, "currency": "INR", "payment_capture": "1"}
        )
        order = Order.objects.create(
            name=name, email=email, mobile_no=mobile, amount=amount, status="SUCCESS",
            provider_order_id=razorpay_order["id"]
        )
        payment = Payment()
        payment.order = order
        payment.payment_id = payment_id
        payment.item_order_id = razorpay_order["id"]
        payment.razorpay_id = razorpay_order['id']
        payment.json_data = razorpay_order
        payment.payment_status = "SUCCESS"
        payment.save()
        return render(
            request,
            "order/payment_page.html",
            {
                # "callback_url": "http://" + "127.0.0.1:8000" + "/order/callback/",
                "callback_url": "https://" + "406d-223-226-4-20.ngrok.io" + "/order/callback/",
                "razorpay_key": settings.RAZOR_KEY_ID,
                "order": order,
            },
        )
    return render(request, "order/payment.html")


@csrf_exempt
def callback(request):
    def verify_signature(response_data):
        print(request.POST)
        print(response_data)
        client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
        return client.utility.verify_payment_signature(response_data)

    if "razorpay_signature" in request.POST:
        payment_id = request.POST.get("razorpay_payment_id", "")
        provider_order_id = request.POST.get("razorpay_order_id", "")
        signature_id = request.POST.get("razorpay_signature", "")
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.signature_id = signature_id
        order.save()
        payment = Payment.objects.get(order_id=order.id)
        # payment.order = order
        payment.payment_id = order.payment_id
        payment.razorpay_id = provider_order_id
        payment.amount = order.amount
        payment.payment_signature = order.signature_id
        payment.json_data = request.body.decode('utf-8')
        payment.save()
        # transaction = Transactions.objects.get(payment=payment_id)

        if not verify_signature(request.POST):
            order.status = "FAILURE"
            payment.status = "FAILURE"
            order.save()
            return render(request, "core/payment_fail.html", context={"status": order.status})
        else:
            order.status = "SUCCESS"
            payment.status = "SUCCESS"
            payment.save()
            return render(request, "core/payment_success.html", context={"status": order.status})
            # return JsonResponse({'status': 'ok'})
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        order = Order.objects.get(provider_order_id=provider_order_id)
        order.payment_id = payment_id
        order.status = "FAILURE"
        order.save()
        return render(request, "core/payment_fail.html", context={"status": order.status})

# @csrf_exempt
# def callback(request):
#     print(request.POST)
#     client = razorpay.Client(auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))
#     result = client.utility.verify_payment_signature(request.POST)
#     if result:
#         payment_id = request.POST.get("razorpay_payment_id", "")
#         provider_order_id = request.POST.get("razorpay_order_id", "")
#         signature_id = request.POST.get("razorpay_signature", "")
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.signature_id = signature_id
#         order.status = "SUCCESS"
#         order.save()
#         payment = Payment.objects.get(order_id=order.id)
#         # payment.order = order
#         payment.payment_id = order.payment_id
#         payment.razorpay_id = provider_order_id
#         payment.amount = order.amount
#         payment.payment_signature = order.signature_id
#         payment.json_data = request.body.decode('utf-8')
#         payment.status = "SUCCESS"
#         payment.save()
#         return render(request, "core/payment_success.html", context={"status": order.status})
#     else:
#         payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
#         provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
#             "order_id"
#         )
#         order = Order.objects.get(provider_order_id=provider_order_id)
#         order.payment_id = payment_id
#         order.status = "FAILURE"
#         order.save()
#         return render(request, "core/payment_fail.html", context={"status": order.status})
#



@csrf_exempt
def payment_verification(request):
    if request.method == "POST":
        print(request.body)
        key = "deepsense"
        message = request.body.decode('utf-8')
        received_signature = request.headers.get("X-Razorpay-Signature")
        verify = razorpay_client.utility.verify_webhook_signature(message, received_signature, key)

        try:
            if verify:
                # payment = json.loads(message.decode("utf-8").replace("'", '"'))
                res = json.loads(message)
                payload = res.get('payload')
                payment = payload.get('payment')
                entity = payment.get('entity')
                # payment_id = entity['id']
                error_code = entity.get('error_code')
                error_description = entity.get('error_description')
                error_source = entity.get('error_source')
                error_step = entity.get('error_step')
                error_reason = entity.get('error_reason')
                payment_id = entity.get('id')
                payment_status = entity.get('status')
                item_order_id = entity.get('order_id')
                payment_method = entity.get('method')
                amount_transferred = entity.get('amount')
                captured = entity.get('captured')
                amount_refunded = entity.get('amount_refunded')
                refund_status = entity.get('refund_status')
                currency = entity.get('currency')
                description = entity.get('description')
                card = entity.get('card')
                card_name = card.get('name')
                card_network = card.get('network')
                card_type = card.get('type')
                card_issuer = card.get('issuer')
                card_last4 = card.get('last4')
                card_emi = card.get('emi')
                card_international = card.get('international')
                card_id = entity.get('card_id')
                bank = entity.get('bank')
                wallet = entity.get('wallet')
                vpa = entity.get('vpa')
                email = entity.get('email')
                contact = entity.get('contact')
                fee = entity.get('fee')
                tax = entity.get('tax')
                data = entity.get('acquirer_data')
                transaction_id = data.get('upi_transaction_id')
                payment = Payment.objects.get(item_order_id=item_order_id)
                payment.payment_id = payment_id
                payment.save()
                new_transaction, _ = Transactions.objects.get_or_create(transaction_payment_id=payment_id, payment=payment)
                new_transaction.transaction_status = payment_status
                new_transaction.transaction_status = entity.get('status')
                new_transaction.status = "SUCCESS"
                new_transaction.is_success = True
                new_transaction.currency = currency
                new_transaction.signature_verified = True
                new_transaction.signature = received_signature
                new_transaction.order_id = item_order_id
                new_transaction.method = payment_method
                new_transaction.amount_refunded = amount_refunded
                new_transaction.refund_status = refund_status
                new_transaction.amount = amount_transferred
                new_transaction.captured = captured
                new_transaction.description = description
                new_transaction.transaction_id = transaction_id
                new_transaction.card_id = card_id
                new_transaction.card_holder_name = card_name
                new_transaction.card_network = card_network
                new_transaction.card_emi = card_emi
                new_transaction.card_type = card_type
                new_transaction.card_international = card_international
                new_transaction.card_issuer = card_issuer
                new_transaction.card_last4 = card_last4
                new_transaction.bank = bank
                new_transaction.wallet = wallet
                new_transaction.vpa = vpa
                new_transaction.fee = fee
                new_transaction.tax = tax
                new_transaction.email = email
                new_transaction.contact = contact
                new_transaction.error_code = error_code
                new_transaction.error_step = error_step
                new_transaction.error_reason = error_reason
                new_transaction.error_source = error_source
                new_transaction.error_description = error_description
                new_transaction.json_transaction_data = message
                new_transaction.save()
                print(new_transaction.transaction_status)
            else:
                pass
        except Exception as e:
            print(e)

    else:
        pass

    return JsonResponse({"status": "ok"})
