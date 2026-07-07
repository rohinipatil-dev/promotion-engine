# **Promotion Engine Data Flow**

## **1. Purpose of This Document**

This document describes the **end‑to‑end data flow** of the Promotion Engine Tool — from user intent → agent reasoning → tool call → promotion selection → agent response.

It ensures:

- predictable behavior
- safe tool usage
- clear agent boundaries
- correct Foundry integration
- easy debugging

# **2. High-Level Data Flow Overview**

The Promotion Engine Tool follows a **5‑stage pipeline**:

1. **User Message → Agent Intent Detection**
2. **Agent → Tool Input Construction**
3. **Tool → Promotion Filtering & Scoring**
4. **Tool → JSON Response**
5. **Agent → Customer-Friendly Output**

Below is the full breakdown.

# **3. Stage 1 — User Message → Agent Intent Detection**

### **Input**

User sends a message such as:

> “Any Eid offers on sofas?”

### **Marketing & Promotions Agent Responsibilities**

- Detect promotion intent
- Extract or infer:
  - category
  - customer segment
  - season
  - cart value
  - language
  - location

### **Agent Output**

A structured tool call input:

json

```
{
  "category": "sofa",
  "customer_segment": "high_value",
  "cart_value": 850,
  "season": "eid",
  "language": "en",
  "location": "dubai"
}

```

# **4. Stage 2 — Agent → Tool Input Construction**

The agent constructs a **strict JSON payload** based on:

- **[AGENTS.md](http://AGENTS.md) rules**
- **[spec.md](http://spec.md) contract**
- **[plan.md](http://plan.md) milestones**
- **[boundaries.md](http://boundaries.md) constraints**

### **Validation**

Agent ensures:

- All required fields exist
- No hallucinated fields
- No missing category
- No missing segment
- No missing season

If missing:

> “Which product are you looking for a promotion on?”

# **5. Stage 3 — Tool → Promotion Filtering & Scoring**

The Promotion Engine Tool receives the JSON payload and executes the following pipeline:

### **Step 1 — Load promotions**

Reads from:

`src/data/promotions.json`

### **Step 2 — Filter promotions**

Filters by:

- active
- category
- customer segment
- season
- cart value
- validity date
- location (optional)

### **Step 3 — Score promotions**

Priority:

1. seasonal
2. segment
3. cart-based
4. generic category

Tie-breakers:

- higher discount
- earlier expiry
- first in list

### **Step 4 — Select best promotion**

Returns **one** promotion only.

### **Step 5 — Format output**

Returns structured JSON.

# **6. Stage 4 — Tool → JSON Response**

### **Success Response**

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

### **No Promotion Response**

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

### **Error Response**

json

```
{
  "error": "Unable to fetch promotions"
}

```

# **7. Stage 5 — Agent → Customer-Friendly Output**

The Marketing & Promotions Agent:

- interprets the JSON
- converts it into a natural message
- applies multilingual translation (via Multilingual Agent)
- ensures safety rules
- avoids hallucination

### **Example Agent Output**

> “Yes! We have an Eid Special: 10% off on premium sofas. Valid until 15 July. Would you like to see some sofa options?”

### **If no promotion**

> “There are no active promotions for this product right now, but I can help you find similar items or upcoming offers.”

# **8. Error Handling Flow**

### **If tool fails**

Agent says:

> “I’m unable to fetch promotions right now. Let me help you browse products instead.”

### **If input is invalid**

Agent asks:

> “Can you tell me which product you’re interested in?”

### **If promotions.json is malformed**

Tool returns safe error → agent switches to Catalog Agent.

# **9. Data Flow Diagram (Text Version)**

Code

```
User Message
     ↓
Marketing & Promotions Agent
     ↓ (extracts category, segment, season, cart value)
Promotion Engine Tool (Azure Function)
     ↓ (loads promotions.json)
Filtering Logic
     ↓
Scoring Logic
     ↓
Best Promotion Selected
     ↓
JSON Response
     ↓
Agent Interpretation
     ↓
Customer-Friendly Message

```

# **10. Future Data Flow Extensions**

### **Phase 2**

- Shopify Discounts API
- Database-backed promotions
- Real-time sync
- Admin dashboard
- Multi-store support

