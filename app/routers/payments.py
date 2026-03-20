import stripe
from fastapi import APIRouter, HTTPException, Request, Header
from pydantic import BaseModel
from app.config import settings

stripe.api_key = settings.STRIPE_SECRET_KEY

router = APIRouter(prefix="/payments")


class CheckoutRequest(BaseModel):
    price_id: str
    success_url: str
    cancel_url: str
    customer_email: str | None = None


@router.post("/checkout")
async def create_checkout_session(body: CheckoutRequest):
    """Create a Stripe Checkout session."""
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            line_items=[{"price": body.price_id, "quantity": 1}],
            mode="payment",
            success_url=body.success_url,
            cancel_url=body.cancel_url,
            customer_email=body.customer_email,
        )
        return {"checkout_url": session.url, "session_id": session.id}
    except stripe.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(alias="stripe-signature"),
):
    """Handle Stripe webhooks. Configure endpoint in Stripe Dashboard."""
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except (ValueError, stripe.SignatureVerificationError):
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    # Handle events
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        # TODO: fulfill order — update DB, send email, etc.
        print(f"Payment completed: {session['id']}")

    elif event["type"] == "payment_intent.payment_failed":
        # TODO: notify user, retry logic
        pass

    return {"status": "ok"}
