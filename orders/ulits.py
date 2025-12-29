# send email when order confirm
from django.core.mail import send_mail

def send_order_email(order):
    subject = f"Order Confirmation - #{order.id}"

    message = f"""
Hi {order.user.username},

Your order #{order.id} has been placed successfully.

Total Amount: Rs {order.total_price}
Payment Method: {order.payment_method.upper()}

Thank you for shopping with SmartCart!
"""

    send_mail(
        subject,
        message,
        None,
        [order.user.email],
        fail_silently=False,
    )
