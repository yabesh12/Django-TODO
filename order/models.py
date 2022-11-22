from django.db import models
from django.db.models.fields import CharField

PAY_CHOICES = (
    ("PENDING", "Pending"),
    ("SUCCESS", "Success"),
    ("FAILED", "Failed"),

)


class Order(models.Model):
    name = CharField(max_length=254, blank=False, null=False)
    email = models.EmailField(max_length=200, blank=True, null=True)
    mobile_no = models.PositiveIntegerField(blank=True, null=True)
    amount = models.FloatField(null=False, blank=False)
    status = models.CharField(max_length=250, choices=PAY_CHOICES, default="PENDING")
    provider_order_id = models.CharField(max_length=200, unique=True)
    payment_id = models.CharField(max_length=200, unique=True)
    signature_id = models.CharField(max_length=200, unique=True)
    created = models.DateTimeField(auto_now_add=True)

    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id}-{self.name}-{self.status}"


class Payment(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    item_order_id = models.CharField(max_length=250, blank=True, null=True)
    payment_id = models.CharField(max_length=250, unique=True)
    razorpay_id = models.CharField(max_length=250, blank=True, null=True)
    amount = models.CharField(max_length=250, blank=True, null=True)
    json_data = models.JSONField()
    payment_status = models.CharField(max_length=200, choices=PAY_CHOICES, default="PENDING")
    payment_signature = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    edited = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.payment_id)


TRANS_CHOICES = (
    ("PENDING", "Pending"),
    ("SUCCESS", "Success"),
    ("FAILED", "Failed"),

)


class Transactions(models.Model):
    payment = models.ForeignKey(Payment, on_delete=models.PROTECT, related_name="transactions")
    transaction_payment_id = models.CharField(max_length=250, unique=True)
    transaction_id = models.CharField(max_length=250, null=True, blank=True)
    status = models.CharField(max_length=200, choices=TRANS_CHOICES, default="PENDING")
    transaction_status = models.CharField(max_length=250, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    edited = models.DateTimeField(auto_now=True)
    # shipping = models.ForeignKey(Shipping, related_name="shipping_transaction", on_delete=models.PROTECT, blank=True,
    #                              null=True)
    # token = models.CharField(max_length=128, blank=True, default="", null=True)
    # kind = models.CharField(max_length=10, choices=TransactionKind.CHOICES, blank=True, null=True)
    is_success = models.BooleanField(default=False)
    currency = models.CharField(max_length=10)
    amount = models.FloatField(default=0.0)
    # error = models.CharField(choices=[(tag, tag.value) for tag in TransactionError], max_length=256, null=True,
    #                          blank=True, )
    signature_verified = models.BooleanField(default=False)
    signature = models.TextField(blank=True, null=True)
    order_id = models.CharField(max_length=128, blank=True, null=True)
    method = models.CharField(max_length=128, blank=True, null=True)
    amount_refunded = models.FloatField(blank=True, null=True)
    refund_status = models.CharField(max_length=128, blank=True, null=True)
    amount_transferred = models.FloatField(default=0.0, null=True, blank=True)
    captured = models.BooleanField(blank=True, null=True)
    description = models.CharField(max_length=128, blank=True, null=True)
    card_id = models.CharField(max_length=128, blank=True, null=True)
    card_holder_name = models.CharField(max_length=256, blank=True, null=True)
    card_network = models.CharField(max_length=256, blank=True, null=True)
    card_type = models.CharField(max_length=256, blank=True, null=True)
    card_issuer = models.CharField(max_length=256, blank=True, null=True)
    card_emi = models.BooleanField(default=False)
    card_last4 = models.IntegerField(blank=True, null=True)
    card_international = models.BooleanField(default=False, blank=True, null=True)
    bank = models.CharField(max_length=128, blank=True, null=True)
    wallet = models.CharField(max_length=128, blank=True, null=True)
    vpa = models.CharField(max_length=128, blank=True, null=True)
    email = models.CharField(max_length=128, blank=True, null=True)
    contact = models.CharField(max_length=128, blank=True, null=True)
    fee = models.FloatField(blank=True, null=True)
    tax = models.FloatField(blank=True, null=True)
    error_code = models.CharField(max_length=128, blank=True, null=True)
    error_description = models.CharField(max_length=128, blank=True, null=True)
    error_source = models.CharField(max_length=128, blank=True, null=True)
    error_step = models.CharField(max_length=128, blank=True, null=True)
    error_reason = models.CharField(max_length=128, blank=True, null=True)
    payment_token = models.CharField(max_length=256, blank=True)
    customer_id = models.CharField(max_length=256, null=True, blank=True)
    refund_id = models.CharField(max_length=256, null=True, blank=True)
    json_transaction_data = models.JSONField(blank=True, null=True)

    # gateway_response = JSONField(encoder=DjangoJSONEncoder)

    def __str__(self):
        return str(self.payment)
