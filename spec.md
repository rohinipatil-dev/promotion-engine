# **Promotion Engine Tool Specification**

## **1. Purpose**

The Promotion Engine Tool selects the **single best promotion** for a customer based on product category, customer segment, season, cart value, and business rules. It ensures **accuracy**, **safety**, and **non‑hallucination** by relying only on the promotions dataset.

## **2. High-Level Behavior**

The tool:

- Loads promotions from `src/data/promotions.json`
- Filters promotions based on input criteria
- Applies scoring rules to choose the best promotion
- Returns a structured JSON response
- Returns a “no promotion” response when nothing matches
- Never invents or modifies promotions



## **3. Inputs (Required Contract)**

The tool accepts a JSON payload:

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



### **Input Fields**

- **category** *(string, required)*   Product category (e.g., sofa, dining_table, bed).
- **customer_segment** *(string, required)*   Values: `new_customer`, `returning`, `high_value`.
- **cart_value** *(number, required)*   Total cart value before discount.
- **season** *(string, required)*   Values: `eid`, `diwali`, `christmas`, `none`.
- **language** *(string, required)*   Always `"en"` — translation handled by the Multilingual Agent.
- **location** *(string, optional)*   Used for region-specific promotions.



## **4. Promotions Data Structure**

Each promotion in `promotions.json` must follow:

json

```
{
  "promotion_id": "eid_sofa_10",
  "category": "sofa",
  "customer_segment": "high_value",
  "min_cart_value": 500,
  "season": "eid",
  "discount_type": "percentage",
  "discount_value": 10,
  "valid_until": "2026-07-15",
  "title": "Eid Special: 10% Off on Sofas",
  "description": "Celebrate Eid with a special discount on premium sofas.",
  "terms": "Valid on selected models only.",
  "active": true
}

```



### **Required Fields**

- promotion_id
- category
- customer_segment
- discount_type
- discount_value
- valid_until
- active



### **Optional Fields**

- min_cart_value
- season
- terms
- description
- location



## **5. Filtering Rules**

The tool must filter promotions using the following rules:

### **Rule 1 — Active Only**

Only promotions where `active == true`.

### **Rule 2 — Category Match**

Promotion category must match input category.

### **Rule 3 — Customer Segment Match**

Promotion segment must match input segment.

### **Rule 4 — Seasonal Match**

If promotion has a season:

- Must match input season If promotion has no season:
- It is considered “generic” and allowed.



### **Rule 5 — Cart Value Threshold**

If promotion has `min_cart_value`, input cart_value must be ≥ threshold.

### **Rule 6 — Validity Date**

Promotion must not be expired.

### **Rule 7 — Location Match (optional)**

If promotion has a location, it must match input location.

## **6. Scoring Logic**

After filtering, the tool must score promotions:

### **Priority Order**

1. Seasonal promotions (highest priority)
2. Customer segment promotions
3. Cart-based promotions
4. Generic category promotions



### **Tie-breaker**

If multiple promotions have equal priority:

- Higher discount_value wins
- If still tied → earliest valid_until wins
- If still tied → first in list wins



## **7. Output Contract**



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



## **8. Error Handling**



### **Invalid Input**

If required fields are missing:

- Return a structured error message
- Do not crash the function



### **Malformed promotions.json**

Return:

> “Promotion data unavailable.”



### **Unexpected Exceptions**

Return:

> “Unable to fetch promotions at the moment.”



## **9. Safety Requirements**

The tool must **never**:

- Invent promotions
- Modify promotions
- Apply expired promotions
- Apply promotions not present in promotions.json
- Translate output (Multilingual Agent handles translation)
- Negotiate discounts
- Apply multiple promotions at once



## **10. Non-Goals**

The tool does **not**:

- Create promotions
- Update promotions
- Delete promotions
- Manage inventory
- Manage orders
- Translate messages
- Handle product details
- Handle checkout

These belong to other agents.

## **11. Test Cases**



### **Test 1 — Seasonal Promotion**

Input: sofa + high_value + eid Expected: Eid promotion returned.

### **Test 2 — Cart Threshold**

Input: cart_value < min_cart_value Expected: Promotion excluded.

### **Test 3 — Expired Promotion**

Input: expired promotion Expected: Excluded.

### **Test 4 — No Promotion**

Input: category with no promotions Expected: “No active promotions”.

### **Test 5 — Multiple Promotions**

Input: multiple matches Expected: Highest priority + highest discount.

## **12. Future Extensions**

- Shopify Discounts API integration
- Personalized promotions
- Inventory-aware promotions
- Multi-store support
- Dynamic seasonal campaigns

