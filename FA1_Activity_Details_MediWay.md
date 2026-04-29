# FA-1 Activity Details (FYMCA Sem-II)
## Subject: Software Project Management
## Project: MediWay (Django-Based Online Pharmacy Management System)

Student Name: ____________________  
PRN/Roll No.: ____________________  
Division: ____________________  
Date: ____________________

---

## 1) Life Cycle Model Selection and Justification (4 Marks)

### Selected Model: **Hybrid (Agile + Waterfall)**

For the MediWay project, we followed a **Hybrid model** because different modules had different development needs:

1. **Waterfall-like flow** was used in initial stages:
- Requirement understanding (medicine catalog, cart, order, billing, admin panel).
- Database schema design (`Medicine`, `Cart`, `Order`, `Bill`, `BillItem`).
- Basic project setup and URL structure.

2. **Agile iteration** was used for feature enhancement:
- Prescription upload added after cart and order flow.
- Razorpay payment integration added after basic order flow.
- Search enhancement (fuzzy matching), pagination, and profile updates were added incrementally.
- Admin order tracking and status updates improved across iterations.

### Why Hybrid is logically suitable for this project
- The project needed a **stable base architecture** first (models, authentication, routing).
- After base setup, many features were improved through **short iterations and feedback**.
- Frequent changes (e.g., payment and prescription workflow) are better handled by Agile.
- Regulatory and domain-specific parts (medical order flow) require planned structure like Waterfall.

Hence, Hybrid gave both **predictability** and **flexibility**, which matches MediWay’s actual development pattern.

---

## 2) Team Structure and Sudden Member Exit Scenario (4 Marks)

### Team Roles (Example for MediWay)
1. **Project Lead / Full-Stack Integrator**
- Module integration, sprint planning, deployment checks.

2. **Backend Developer (Django)**
- Models, business logic, order workflow, payment APIs.

3. **Frontend Developer**
- Templates, user navigation flow, cart/order UI, responsive layout.

4. **QA & Documentation Member**
- Test scenarios, defect logging, submission artifacts, demo preparation.

### Sudden Exit Scenario
Assume the **Backend Developer** leaves 2 weeks before submission.

### Impact
- Payment and order-status features may remain unstable.
- Bug fixing speed decreases.
- Integration bottleneck appears for frontend and testing.

### Risk Level
- **High**, because backend controls core transactions and data flow.

### Contingency/Backup Plan
1. Keep all code in shared repository with clear commit messages.
2. Maintain module-wise documentation (API flow, models, critical logic notes).
3. Cross-train at least one teammate on backend basics.
4. Freeze new features and prioritize critical bug fixes.
5. Reassign work:
- Lead handles payment/order logic stabilization.
- Frontend dev supports minor backend fixes.
- QA focuses on regression testing of checkout/order flow.

This reduces dependency on a single person and improves team resilience.

---

## 3) Risk Management: Top 3 Risks with Prioritization (4 Marks)

### Risk Register (MediWay)

| Risk Type | Risk Description | Probability | Impact | Priority |
|---|---|---|---|---|
| Technical | Payment verification mismatch/failure (Razorpay callback or status sync issues) | High | High | **1 (Highest)** |
| Schedule | Delay in integrating dependent modules (prescription upload + checkout + order status) | Medium | High | **2** |
| Resource | Team member unavailability during final integration/testing phase | Medium | Medium-High | **3** |

### Justification of Prioritization
1. **Payment flow risk** is highest because it directly affects order completion and user trust.
2. **Schedule integration delay** is second because module dependencies can block end-to-end testing.
3. **Resource risk** is third; impact is serious but can be reduced by documentation and role backup.

### Mitigation Summary
- Payment risk: sandbox testing, exception handling, transaction logging, fallback order status checks.
- Schedule risk: milestone-based planning, weekly review, early integration testing.
- Resource risk: cross-skilling, backup ownership, and documented handover notes.

---

## 4) Leadership Style Application (Directive + Collaborative) (4 Marks)

### A) Directive Leadership Situation (Realistic)
**Situation:** One day before internal demo, checkout fails for prescription-required medicines due to flow mismatch.

**Directive Actions by Project Lead:**
1. Immediately freeze non-critical UI changes.
2. Assign backend member to fix checkout condition logic.
3. Assign frontend member to verify upload form validation.
4. Assign QA to test only critical user journey (cart → prescription upload → payment → order).
5. Set strict 2-hour checkpoints.

**Reason:** Time-critical defect needs clear command, quick decisions, and zero ambiguity.

### B) Collaborative Leadership Situation (Realistic)
**Situation:** Planning a feature improvement for search relevance and admin order dashboard usability.

**Collaborative Actions by Project Lead:**
1. Conduct short brainstorming with all teammates.
2. Gather suggestions from frontend, backend, and QA perspectives.
3. Prioritize ideas by effort vs impact.
4. Agree sprint tasks jointly.
5. Review outcomes in team meeting and adjust.

**Reason:** When there is no immediate crisis, collaboration improves innovation, ownership, and quality.

---

## 5) Gantt Chart / Project Schedule (4 Marks)

### Major Activities and Timeline (8 Weeks)

| Activity | W1 | W2 | W3 | W4 | W5 | W6 | W7 | W8 |
|---|---|---|---|---|---|---|---|---|
| Requirement Analysis & Scope Finalization | ███ | ███ |  |  |  |  |  |  |
| DB Design & Django Project Setup |  | ███ | ███ |  |  |  |  |  |
| Core Modules (Auth, Medicine, Cart) |  |  | ███ | ███ |  |  |  |  |
| Prescription + Checkout + Payment Integration |  |  |  | ███ | ███ |  |  |  |
| Admin Panel + Order Management + Billing |  |  |  |  | ███ | ███ |  |  |
| Testing, Bug Fixing, Documentation |  |  |  |  |  | ███ | ███ |  |
| Final Demo Preparation & Submission |  |  |  |  |  |  | ███ | ███ |

You can reproduce this as a hand-drawn Gantt chart in your notebook/file if required by faculty.

---

## Conclusion

MediWay’s project execution best matches a **Hybrid life cycle** with planned foundation and iterative improvements.  
The team structure, prioritized risks, and leadership-style application show practical software project management decisions for a real Django implementation.  
The schedule and contingency planning improved delivery confidence and reduced last-phase project uncertainty.

