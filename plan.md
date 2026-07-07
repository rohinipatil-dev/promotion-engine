# **Implementation Plan for Promotion Engine Tool**

## **1. Objective**

Build a fully functional Promotion Engine Tool that selects the best promotion for a customer based on category, segment, season, cart value, and business rules. The tool will run as an Azure Function and integrate with a Foundry Marketing Agent.

## **2. Scope**

This plan covers:

- Tool logic
- Data structure
- Azure Function implementation
- Testing
- Documentation
- Foundry integration
- Demo preparation

It does **not** cover Shopify integration (Phase 2).

## **3. Milestones & Timeline**

### **Milestone 1 — Project Setup (Day 1)** 

- Create folder structure
- Add README.md
- Add AGENTS.md
- Add spec.md
- Add plan.md
- Add architecture docs
- Scaffold Azure Function
- Add promotions.json
- Add basic tests

**Status:** Completed ✔

### **Milestone 2 — Implement Core Logic (Day 2–3)**

Implement full promotion selection logic inside `index.py`:

1. Load promotions.json
2. Validate input payload
3. Filter promotions
  - active
  - category
  - segment
  - season
  - cart value
  - validity date
  - location (optional)
4. Score promotions
  - seasonal priority
  - segment priority
  - cart priority
  - discount value
5. Select best promotion
6. Return structured JSON response
7. Handle “no promotion” case
8. Add error handling

Cursor will generate most of this using spec.md.

### **Milestone 3 — Expand promotions.json (Day 3)**

Add realistic sample promotions:

- Eid
- Diwali
- Christmas
- Clearance
- Category-specific
- High-value customer
- Cart-based

This improves demo quality.

### **Milestone 4 — Testing (Day 3–4)**

Add unit tests in `tests/test_promotions.py`:

- seasonal promotion
- cart threshold
- expired promotion
- no promotion
- multiple promotions
- invalid input
- malformed JSON

Run:

Code

```
pytest tests/
```

### **Milestone 5 — Local Function Testing (Day 4)**

Run Azure Function locally:

Code

```
cd src/azure-functions/get_promotions
func start
```

Test with:

- curl
- Postman
- browser

Verify correct JSON output.

### **Milestone 6 — Deployment (Day 4–5)**

Deploy Azure Function:

- Create Function App
- Deploy via VS Code or Azure CLI
- Get public endpoint
- Test endpoint manually

### **Milestone 7 — Foundry Integration (Day 5)**

Create Foundry tool:

- Name: `get_promotions`
- Type: HTTP tool
- Add endpoint
- Add input schema
- Add output schema
- Add safety rules
- Add description

Test tool calls inside Foundry.

### **Milestone 8 — Agent Integration (Day 5–6)**

Connect tool to Marketing & Promotions Agent:

- Add tool call rules
- Add safety rules
- Add fallback behavior
- Add multilingual support (via Multilingual Agent)

Test with sample conversations.

### **Milestone 9 — Demo Preparation (Day 6–7)**

Prepare demo:

- Add realistic promotions
- Create sample inputs
- Record tool responses
- Prepare WhatsApp demo script
- Add screenshots to README
- Add architecture diagrams
- Add portfolio notes

## **4. Technical Tasks (Detailed)**

### **Task A — Implement filtering logic**

- active filter
- category filter
- segment filter
- season filter
- cart threshold
- validity date
- location filter

### **Task B — Implement scoring logic**

- seasonal > segment > cart > generic
- discount value tie-breaker
- validity date tie-breaker

### **Task C — Implement output formatting**

- success response
- no promotion response
- error response

### **Task D — Add safety**

- no hallucinations
- no invented promotions
- no expired promotions
- no multiple promotions

### **Task E — Add tests**

- unit tests
- edge cases
- malformed JSON
- invalid input

## **5. Dependencies**

- Python 3.11+
- Azure Functions Core Tools
- pytest
- promotions.json
- Foundry workspace
- Cursor IDE

## **6. Risks & Mitigations**

### **Risk 1 — Incorrect filtering**

Mitigation: strict rules in spec.md + unit tests.

### **Risk 2 — Incorrect scoring**

Mitigation: deterministic scoring logic + tie-breakers.

### **Risk 3 — Expired promotions**

Mitigation: date validation + tests.

### **Risk 4 — Agent hallucination**

Mitigation: strict AGENTS.md rules + safety constraints.

## **7. Future Enhancements**

- Shopify Discounts API integration
- Personalized promotions
- Inventory-aware promotions
- Multi-store support
- Dynamic seasonal campaigns
- Real-time promotion updates
- Database-backed promotions

## **8. Completion Criteria**

The Promotion Engine Tool is considered complete when:

- All filtering + scoring logic works
- All tests pass
- Azure Function runs locally
- Azure Function is deployed
- Foundry tool is connected
- Agent can call tool successfully
- Demo conversation works end-to-end

