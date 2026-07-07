# **Design Tradeoffs for Promotion Engine Tool**

## **1. Purpose of This Document**

This document explains the **key design tradeoffs** made while building the Promotion Engine Tool. It clarifies *why* certain architectural choices were selected, *what alternatives were rejected*, and *how these decisions impact scalability, safety, and complexity*.

This helps future developers, agents, and reviewers understand the reasoning behind the system.

## **2. Tradeoff: JSON File vs Database**

### **Chosen:** JSON file (`promotions.json`)

### **Alternative:** SQL/NoSQL database

### **Why JSON?**

- Simple for Phase 1
- Easy to edit manually
- Works offline
- Perfect for demos and portfolio
- Zero infrastructure cost
- Cursor can reason over it easily

### **Tradeoff Impact**

- ❌ No dynamic updates
- ❌ No multi-user editing
- ❌ No real-time promotions
- ❌ No large-scale data support

### **Future Upgrade**

Move to:

- **PostgreSQL**
- **MongoDB**
- **Shopify Discounts API**

### Guided Link

**Database Upgrade**

## **3. Tradeoff: Azure Function vs Containerized Microservice**

### **Chosen:** Azure Function

### **Alternative:** Docker + Kubernetes microservice

### **Why Azure Function?**

- Fast to build
- No DevOps overhead
- Auto-scaling
- Perfect for beginners
- Easy Foundry integration
- Works well with Cursor

### **Tradeoff Impact**

- ❌ Limited runtime customization
- ❌ Harder to run heavy ML logic
- ❌ Not ideal for multi-tool orchestration
- ❌ Cold start delays under high load

### **Future Upgrade**

Move to:

- Dockerized microservice
- Azure Container Apps
- Kubernetes (AKS)

### Guided Link

**Containerization**

## **4. Tradeoff: Deterministic Scoring vs ML-based Personalization**

### **Chosen:** Deterministic scoring rules

### **Alternative:** Machine learning model for promotion ranking

### **Why deterministic?**

- Transparent
- Easy to test
- Easy to debug
- Predictable
- Safe for early agents
- No training data required

### **Tradeoff Impact**

- ❌ No personalization
- ❌ No learning from customer behavior
- ❌ No dynamic ranking
- ❌ No A/B testing

### **Future Upgrade**

Use:

- Customer segmentation model
- Collaborative filtering
- Real-time personalization

### Guided Link

**Personalization Upgrade**

## **5. Tradeoff: Single Promotion vs Multiple Promotions**

### **Chosen:** Return **one best promotion**

### **Alternative:** Return multiple promotions

### **Why single promotion?**

- Simple for agents
- Easy for customers
- Avoids confusion
- Matches retail expectations
- Reduces hallucination risk
- Easier to score

### **Tradeoff Impact**

- ❌ Cannot show “all available offers”
- ❌ Cannot combine promotions
- ❌ Cannot show category-wide campaigns

### **Future Upgrade**

Add:

- “Show all promotions” endpoint
- Multi-promotion ranking
- Promotion bundles

### Guided Link

**Multi-Promotion**

## **6. Tradeoff: Read-Only Promotions vs Editable Promotions**

### **Chosen:** Read-only promotions

### **Alternative:** Admin dashboard to create/edit promotions

### **Why read-only?**

- Safe
- No accidental changes
- No admin UI required
- No authentication needed
- Perfect for demos

### **Tradeoff Impact**

- ❌ Cannot update promotions dynamically
- ❌ Cannot add new campaigns without editing JSON
- ❌ No business-user interface

### **Future Upgrade**

Add:

- Admin dashboard
- Promotion management API
- Authentication + RBAC

### Guided Link

**Admin Dashboard**

## **7. Tradeoff: Local Logic vs Shopify Discounts API**

### **Chosen:** Local logic

### **Alternative:** Shopify Discounts API integration

### **Why local logic?**

- No Shopify access needed
- Works without client store
- Perfect for portfolio
- Fast to build
- Easy to test

### **Tradeoff Impact**

- ❌ Cannot sync with real store discounts
- ❌ Cannot apply discount codes automatically
- ❌ Cannot validate discount availability

### **Future Upgrade**

Integrate:

- Shopify Admin API
- Shopify Discounts API
- Draft order discount application

### Guided Link

**Shopify Integration**

## **8. Tradeoff: English Output vs Multilingual Output**

### **Chosen:** English-only output

### **Alternative:** Multi-language output inside the tool

### **Why English-only?**

- Multilingual Agent handles translation
- Keeps tool simple
- Avoids language-specific bugs
- Avoids duplicated logic

### **Tradeoff Impact**

- ❌ Tool cannot directly return Arabic/Hindi
- ❌ Requires agent collaboration

### **Future Upgrade**

Add:

- Language parameter
- Multi-language templates

### Guided Link

**Multilingual Upgrade**

## **9. Tradeoff: Static Promotions vs Real-Time Promotions**

### **Chosen:** Static promotions

### **Alternative:** Real-time promotions from APIs

### **Why static?**

- Predictable
- Easy to test
- No external dependencies
- Perfect for demos

### **Tradeoff Impact**

- ❌ Cannot reflect real-time store changes
- ❌ Cannot auto-expire promotions
- ❌ Cannot sync with inventory

### **Future Upgrade**

Add:

- Cron jobs
- Real-time API sync
- Inventory-aware promotions

