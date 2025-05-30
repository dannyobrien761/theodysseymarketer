# theodysseymarketer

## Contents:

- <a href="#ux">UX</a>
  - <a href="#user_stories">User stories</a>
  - <a href="#erd">Entity Relationship Diagram (ERD)</a>
  - <a href="#design">Design</a>
- <a href="#marketing">Marketing strategy</a>
- <a href="#testing">Testing</a>
- <a href="#bugs">Bugs</a>
- <a href="#features">Existing Features</a>
- <a href="#f_features">Features left to Implement</a>
- <a href="#technology">Languages, Technologies & Libraries</a>
- <a href="#deployment">Deployment</a>


## <div id="ux">UX</div>
## 🚀 Project Overview
The Odyssey Marketer is a **B2B SaaS marketing platform** that helps businesses automate, manage, and scale their marketing operations.
It is a subscription-Based Marketing SaaS Platform. Admin perspective of dealing with lots of subscription based clients easily sell and onboard clients to service and a user freindly client interface to easily manage subscription account, track payments or cancel subscription. 


Built in Django and integrated with Stripe, it offers subscription-based access to a suite of services, including:
- Website design + hosting
- AI chatbot integrations
- Social media content creation and video editing services

This platform is designed for marketing agencies, SMEs, and freelancers seeking streamlined, plug-and-play marketing solutions.

---

github url:

https://github.com/dannyobrien761/theodysseymarketer


## 📋 <div id="user_stories">User stories</div> 

### ✅ User Stories (Client Perspective)

| **AS A/AN**        | **I WANT TO BE ABLE TO...**                                     | **SO THAT I CAN...**                                                                 |
|--------------------|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Client (User)      | Create an account and log in securely                         | Access my dashboard and manage my subscriptions                                     |
| Client (User)      | View and update my profile (email, phone, company name, etc.) | Keep my contact and business details up to date                                     |
| Client (User)      | View my active subscription plan                              | Understand what service tier I’m paying for (e.g., Basic, Pro, Premium)              |
| Client (User)      | See the benefits included in my subscription plan             | Know exactly what services I’m entitled to (e.g., chatbot integration, video editing)|
| Client (User)      | View my subscription status                                   | Know whether my plan is **active**, **canceled**, or **expired**                    |
| Client (User)      | View the date I started and paid for my subscription          | Track my billing cycle and subscription history                                     |
| Client (User)      | View and download my payment receipts                         | Have a clear record for accounting and tax purposes                                 |
| Client (User)      | Upgrade or downgrade my subscription plan                     | Adjust my service level as my business needs change                                 |
| Client (User)      | Cancel my subscription if needed                              | Stop being billed if I no longer need the service                                   |
| Client (User)      | Access the Stripe checkout to pay                             | Securely subscribe to a plan with my credit/debit card                              |
| Client (User)      | Receive email notifications about payment confirmation        | Get alerted when a subscription is successfully paid                                |
| Client (User)      | Receive alerts when payment fails or subscription expires     | Prevent unexpected service interruptions                                            |
| Client (User)      | Contact support from within the dashboard                     | Get help quickly if I run into issues                                               |
| Client (User)      | Account Required Before Checkout | When a user clicks Subscribe next to a specific plan, then registers, and pays — they should be charged for that exact plan only. and get access to dashboard upon success.
---
### 💼 User Stories (Business Admin Perspective)

| **AS A/AN**        | **I WANT TO BE ABLE TO...**                                     | **SO THAT I CAN...**                                                                 |
|--------------------|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Business Admin     | Add, edit, or delete subscription plans                       | Offer different service tiers to customers                                          |
| Business Admin     | Attach Stripe pricing IDs to plans                           | Integrate plans with Stripe for checkout                                            |
| Business Admin     | View all users and their current subscription status         | Know which clients are active, expired, or canceled                                 |
| Business Admin     | View all payments and filter by status/date                  | Analyze revenue and monitor cash flow                                               |
| Business Admin     | Get notified when a new user signs up or pays                | Take follow-up action (e.g., onboarding email, upsell offers)                       |
| Business Admin     | Update subscription features (e.g., add new services)        | Keep service offerings competitive and relevant                                     |
| Marketing Team     | See contact form inquiries                                   | Follow up with leads and convert them into subscribers                              |

---

### 🔍 Additional Potential User Stories

| **AS A/AN**        | **I WANT TO BE ABLE TO...**                                     | **SO THAT I CAN...**                                                                 |
|--------------------|----------------------------------------------------------------|--------------------------------------------------------------------------------------|
| Client (User)      | Compare all available subscription plans before choosing      | Make an informed purchase decision                                                  |
| Client (User)      | See testimonials or case studies of each service tier         | Build confidence in what I’m subscribing to                                         |
| Client (User)      | Access onboarding resources after payment                     | Start using the service effectively right after subscribing                         |
| Client (User)      | Track service usage metrics (optional future feature)         | Ensure I’m getting value from my subscription                                       |



## <div id="erd">Entity Relationship Diagram (ERD)</div> 

### 🔐 User
- id (PK)
- email (Unique)
- password
- first_name
- last_name
- company_name
- phone_number

⬇️ One-to-One with: `Subscription`

---

### 🧾 SubscriptionPlan
- id (PK)
- name
- price
- billing_cycle [monthly, yearly]
- features (JSONField)
- stripe_price_id

⬇️ One-to-Many with: `Subscription`

---

### 📄 Subscription
- id (PK)
- user_id (FK to User, OneToOne)
- plan_id (FK to SubscriptionPlan)
- start_date
- end_date
- status [active, canceled, expired]
- stripe_subscription_id (from Stripe)

⬇️ One-to-Many with: `Payment`

---

### 💳 Payment
- id (PK)
- user_id (FK to User)
- subscription_id (FK to Subscription)
- amount
- currency
- status [paid, failed, refunded]
- payment_date
- stripe_payment_intent_id

---

### 📬 ContactInquiry
- id (PK)
- name
- email
- message
- created_at


![ERD-png](assets/readme/erd.png)

## <div id="design">Design</div>

Below is the sitemap for the website 
![Site-Map](assets/readme/sitemap.png)

## <div id="marketing">Marketing strategy</div>
### ✅ Marketing Strategy
Our marketing strategy focuses on:
- SEO optimization (robots.txt, sitemap.xml, metadata, and clean URLs)
- Clear onboarding flows that guide users from signup → subscription → dashboard access
- Transparent cancellation + renewal policies to build trust and reduce refund requests
- Leveraging content marketing (blog, insights, case studies) to attract organic leads

---


## <div id="testing">Testing</div>


![stripe-webhook-testing](assets/readme/test-stripe-cli.PNG)

## <div id="features">Features</div>
## 💡 Core Features

✅ User registration + authentication  
✅ Stripe subscription plans (monthly/annual)  
✅ Dashboard access for active subscribers  
✅ Ability to cancel or upgrade plans  
✅ SEO tools: robots.txt + sitemap.xml  
✅ Contact form for support and inquiries  

---

## <div id="technology">technology</div>
## ⚙️ Tech Stack

- Django 5.x
- Stripe API (subscriptions + billing)
- PostgreSQL (production)
- Bootstrap 4 (frontend UI)
- Django-allauth (user authentication)
- Gunicorn + Heroku deployment

---


## <div id="deployment">deployment</div>
## Deployment



- The site was deployed to heroku. The steps to deploy are as follows: 

### Steps:

1. Install dependencies: `gunicorn`, `whitenoise`
2. Add `Procfile` and update `settings.py` for production
3. Run `collectstatic` to prepare static assets
4. Create and configure the Heroku app using the CLI
5. Push the project to Heroku Git
6. Set necessary environment variables on the Heroku dashboard
7. Run database migrations on the Heroku dyno


The live link can be found here - https://marketing-agency-fcc8243e8eeb.herokuapp.com/
