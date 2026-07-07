## Promotion Engine Tool

A server‑side tool that selects the **best promotion** for a customer based on product category, customer segment, season, cart value, and business rules. It is designed to be used inside a **Microsoft Foundry multi‑agent system** for WhatsApp commerce (Twilio + Shopify).

## 🎯 Purpose

The Promotion Engine Tool provides **one clear promotion** for a given customer context. It ensures:

- No hallucinated discounts
- No expired promotions
- No invalid offers
- No inconsistent logic

It is the “brain” behind your **Marketing & Promotions Agent**.

## 🧩 How It Fits Into the System

### Customer → WhatsApp → Twilio → Foundry → Marketing Agent → Promotion Engine Tool → Agent → Customer

### Shopify → Promotion Engine Tool

The tool reads:

- Product category
- Customer segment
- Cart value
- Seasonal context
- Inventory (optional)
- Active promotions (JSON or DB)

It returns a **single promotion** or **no promotion**.

## 📦 Features

- Category‑based promotions
- Seasonal promotions (Eid, Diwali, Christmas, etc.)
- Customer segment logic (new, returning, high‑value)
- Cart‑value logic (high cart discounts)
- Inventory‑aware promotions (optional)
- Safety rules (no fake discounts)
- English‑only output (translated later by Multilingual Agent)

## 🧱 Inputs

The Foundry agent calls the tool with:

json

```
{
  "product_id": "12345",
  "category": "sofa",
  "customer_segment": "high_value",
  "cart_value": 850,
  "season": "eid",
  "language": "en",
  "location": "dubai"
}
```

## 📤 Outputs

The tool returns:

json

```
{
  "promotion_id": "eid_sofa_10",
  "title": "Eid Special: 10% Off on Sofas",
  "description": "Celebrate Eid with a special discount on premium sofas.",
  "discount_type": "percentage",
  "discount_value": 10,
  "valid_until": "2026-07-15",
  "terms": "Valid on selected models only.",
  "language": "en"
}
```

If no promotion applies:

json

```
{
  "promotion_id": null,
  "title": "No active promotions",
  "description": "There are no promotions available for this product.",
  "discount_type": "none",
  "discount_value": 0,
  "valid_until": null,
  "terms": "",
  "language": "en"
}
```

## 🧠 Logic Overview

The tool selects promotions using:

- Category match
- Customer segment match
- Seasonal match
- Cart value threshold
- Validity date
- Inventory (optional)
- Highest discount wins
- Seasonal > generic
- High‑value > normal customer

## 🗂 Directory Structure

Code

```
promotion-engine/
│
├── README.md
├── AGENTS.md
├── spec.md
├── plan.md
├── architecture/
│   ├── boundaries.md
│   ├── tradeoffs.md
│   └── data-flow.md
│
├── src/
│   ├── azure-functions/
│   │   └── get_promotions/
│   │       ├── function.json
│   │       ├── index.py
│   │       └── requirements.txt
│   └── data/
│       └── promotions.json
│
└── tests/
    └── test_promotions.py

```

## 🚀 Getting Started

### 1. Clone the repo

Code

```
git clone <your-repo-url>
```

### 2. Install dependencies

Code

```
pip install -r requirements.txt
```

### 3. Run locally

Code

```
func start
```

### 4. Deploy to Azure

Use Azure Function App deployment.

### 5. Connect to Foundry

Add the HTTP endpoint as a tool named **get_promotions**.

## 🔒 Safety Rules

The tool must **never**:

- Invent promotions
- Apply expired discounts
- Apply discounts not in the database
- Translate output (Multilingual Agent handles that)
- Negotiate discounts

## 🧪 Testing

Run unit tests:

Code

```
pytest tests/
```

Tests include:

- Seasonal promotions
- Category promotions
- No promotions
- High cart value
- High‑value customer
- Expired promotions

## 📘 Related Components

- **Marketing & Promotions Agent**
- **Customer Segmentation Tool**
- **Upsell & Cross-sell Agent**
- **Multilingual Messaging Agent**

## 🎯 Status

This tool is the **first building block** of your multi‑agent WhatsApp commerce system.