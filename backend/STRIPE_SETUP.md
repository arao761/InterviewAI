# Stripe Payment Integration Setup Guide

This guide will help you set up Stripe payments for the InterviewAI application.

## Prerequisites

1. A Stripe account (sign up at https://stripe.com)
2. Access to Stripe Dashboard
3. Your application running locally or deployed

## Step 1: Get Your Stripe API Keys

1. Log in to your [Stripe Dashboard](https://dashboard.stripe.com)
2. Go to **Developers** → **API keys**
3. You'll see two keys:
   - **Publishable key** (starts with `pk_`) - Safe to use in frontend
   - **Secret key** (starts with `sk_`) - Keep secret, backend only

### Test Mode vs Live Mode

- **Test Mode**: Use test keys for development (cards: 4242 4242 4242 4242)
- **Live Mode**: Use live keys for production (real payments)

Toggle between modes in the Stripe Dashboard.

## Step 2: Create Products and Prices in Stripe

1. Go to **Products** in Stripe Dashboard
2. Click **Add product** for each plan:

### Starter Plan ($9/month)
- **Name**: Starter Plan
- **Pricing**: Recurring
- **Price**: $9.00 USD
- **Billing period**: Monthly
- **Save** and copy the **Price ID** (starts with `price_`)

### Professional Plan ($29/month)
- **Name**: Professional Plan
- **Pricing**: Recurring
- **Price**: $29.00 USD
- **Billing period**: Monthly
- **Trial period**: 14 days (optional)
- **Save** and copy the **Price ID** (starts with `price_`)

## Step 3: Set Up Webhook Endpoint

Webhooks allow Stripe to notify your backend about payment events.

### For Local Development:

1. Install Stripe CLI: https://stripe.com/docs/stripe-cli
2. Login: `stripe login`
3. Forward webhooks: `stripe listen --forward-to localhost:8000/api/v1/payments/webhook`
4. Copy the webhook signing secret (starts with `whsec_`)

### For Production:

1. Go to **Developers** → **Webhooks** in Stripe Dashboard
2. Click **Add endpoint**
3. Endpoint URL: `https://yourdomain.com/api/v1/payments/webhook`
4. Select events to listen to:
   - `checkout.session.completed`
   - `customer.subscription.updated`
   - `customer.subscription.deleted`
   - `invoice.payment_succeeded`
5. Copy the **Signing secret** (starts with `whsec_`)

## Step 4: Configure Environment Variables

Add these to your `.env` file in the `backend/` directory:

```bash
# Stripe Configuration
STRIPE_SECRET_KEY=sk_test_...  # Your Stripe secret key
STRIPE_PUBLISHABLE_KEY=pk_test_...  # Your Stripe publishable key
STRIPE_WEBHOOK_SECRET=whsec_...  # Your webhook signing secret
STRIPE_PRICE_STARTER=price_...  # Price ID for Starter plan
STRIPE_PRICE_PROFESSIONAL=price_...  # Price ID for Professional plan
```

### Frontend Environment Variable

Add to `.env.local` in `v0-interview-prep-app-main/`:

```bash
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=pk_test_...
```

## Step 5: Install Dependencies

```bash
cd backend
source ../venv/bin/activate
pip install stripe
```

## Step 6: Run Database Migrations

```bash
cd backend
source ../venv/bin/activate
alembic upgrade head
```

This will add subscription and payment fields to your database.

## Step 7: Test the Integration

### Test Cards (Test Mode Only)

- **Success**: 4242 4242 4242 4242
- **Decline**: 4000 0000 0000 0002
- **Requires Authentication**: 4000 0025 0000 3155

### Testing Flow

1. Start your application: `./START_HACKATHON.sh`
2. Go to http://localhost:3000/pricing
3. Click "Get Started" or "Start Free Trial"
4. You'll be redirected to Stripe Checkout
5. Use test card: 4242 4242 4242 4242
6. Use any future expiry date, any CVC, any ZIP
7. Complete the payment
8. You'll be redirected back to `/payment/success`

## API Endpoints

### Create Checkout Session
```
POST /api/v1/payments/create-checkout
Body: { "plan": "starter" | "professional" }
Returns: { "checkout_url": "...", "session_id": "..." }
```

### Get Subscription Status
```
GET /api/v1/payments/subscription
Returns: { "plan": "...", "status": "...", ... }
```

### Cancel Subscription
```
POST /api/v1/payments/cancel-subscription
Returns: { "message": "...", "cancel_at": "..." }
```

### Webhook Endpoint
```
POST /api/v1/payments/webhook
(Handled automatically by Stripe)
```

## Security Notes

1. **Never expose your secret key** in frontend code
2. **Always verify webhook signatures** (already implemented)
3. **Use HTTPS in production** (required by Stripe)
4. **Store keys in environment variables**, never in code
5. **Use test mode** during development

## Troubleshooting

### "Stripe is not configured" error
- Check that `STRIPE_SECRET_KEY` is set in `.env`
- Restart the backend server

### Webhook not working
- Verify webhook URL is correct
- Check webhook secret matches
- Use Stripe CLI for local testing: `stripe listen --forward-to localhost:8000/api/v1/payments/webhook`

### Payment succeeds but subscription not updated
- Check webhook is receiving events (Stripe Dashboard → Webhooks → Events)
- Verify webhook secret is correct
- Check backend logs for errors

### Checkout redirects to wrong URL
- Update `CORS_ORIGINS` in config to include your frontend URL
- Check success/cancel URLs in checkout creation

## Next Steps

1. Set up feature gating based on subscription plan
2. Add subscription management UI
3. Implement plan upgrades/downgrades
4. Add email notifications for payment events
5. Set up subscription analytics

## Support

- Stripe Documentation: https://stripe.com/docs
- Stripe Support: https://support.stripe.com
- Test Mode Guide: https://stripe.com/docs/testing

