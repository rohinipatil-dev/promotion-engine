# **Promotion Engine Tool Boundaries**

## **1. Purpose of This Document**

This document defines the **strict boundaries** for the Promotion Engine Tool. It prevents ambiguity, hallucination, and accidental expansion of scope by clearly stating:

- What the tool **is responsible for**
- What the tool **is not responsible for**
- What the tool **must never do**
- What other agents or systems handle

These boundaries ensure safe, predictable behavior inside Foundry.

## **2. Core Responsibilities (What the Tool *Must* Do)**

- Load promotions from `promotions.json`
- Filter promotions based on:
  - category
  - customer segment
  - season
  - cart value
  - validity date
  - active status
  - location (optional)
- Score promotions using deterministic rules
- Select **one best promotion**
- Return a structured JSON response
- Return a “no promotion” response when nothing matches
- Handle errors gracefully
- Log failures (local or Azure logs)

These are the **only** responsibilities of the Promotion Engine Tool.

## **3. Non-Responsibilities (What the Tool *Does Not* Do)**

The tool **does not**:

- Create promotions
- Update promotions
- Delete promotions
- Modify promotions
- Translate promotions
- Provide product details
- Provide product images
- Handle checkout
- Handle order creation
- Handle delivery or logistics
- Manage inventory
- Connect to Shopify
- Connect to databases
- Apply multiple promotions
- Negotiate discounts
- Apply custom discounts
- Generate dynamic promotions
- Manage customer profiles
- Manage customer segmentation
- Handle multilingual output
- Handle WhatsApp conversation flow

These responsibilities belong to other agents or backend systems.

## **4. Hard Safety Boundaries (What the Tool *Must Never* Do)**

The tool must **never**:

- Invent promotions
- Guess discount values
- Apply expired promotions
- Apply promotions not present in `promotions.json`
- Apply promotions for the wrong category
- Apply promotions for the wrong customer segment
- Apply promotions for the wrong season
- Apply promotions below cart threshold
- Apply multiple promotions at once
- Return raw internal errors
- Reveal internal logic or architecture
- Reveal file paths or server details
- Return unvalidated or malformed JSON
- Translate output (Multilingual Agent handles translation)

These are **strict prohibitions**.

## **5. Input Boundaries**

The tool only accepts the following fields:

- `category`
- `customer_segment`
- `cart_value`
- `season`
- `language`
- `location` (optional)

The tool must **reject**:

- unknown fields
- missing required fields
- invalid types
- malformed JSON

If input is invalid, return a safe error response.

## **6. Output Boundaries**

The tool must return **only**:

### ✔ A valid promotion

or

### ✔ A “no promotion” structured response

or

### ✔ A safe error response

The tool must **not**:

- return multiple promotions
- return raw JSON arrays
- return internal stack traces
- return Python objects
- return partial promotions
- return unstructured text

## **7. Data Boundaries**

The tool uses **only**:

- `src/data/promotions.json`

It must **not**:

- read external APIs
- read Shopify
- read databases
- read other JSON files
- write to any file
- modify promotions.json

Promotions.json is **read-only**.

## **8. Execution Boundaries**

The tool runs as:

- an Azure Function
- stateless
- idempotent
- deterministic

It must **not**:

- maintain session state
- store user data
- cache promotions
- perform long-running tasks
- perform background jobs

## **9. Agent Boundaries**

The Promotion Engine Tool is used **only** by:

- Marketing & Promotions Agent

It must **not** be used for:

- product search (Catalog Agent)
- order creation (Order Agent)
- delivery updates (Logistics Agent)
- translation (Multilingual Agent)
- customer segmentation (Segmentation Agent)

Each agent has its own domain.

## **10. Future Boundaries (Phase 2)**

In future versions, the tool **may** integrate with:

- Shopify Discounts API
- Database-backed promotions
- Multi-store promotions
- Personalized promotions
- Inventory-aware promotions

But these are **explicitly out of scope for Phase 1**.