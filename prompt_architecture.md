# Build a Local Airtable-like Web App (Django + React)

## Primary Prompt

Here’s a strong, detailed prompt you can use to generate the entire Airtable-like system with any advanced AI code generator (e.g., GPT-Engineer, Cursor, Replit Agent, or v0):

---

### 🔧 Prompt Title: **Build a Local Airtable‑like Web App (Django + React)**

**Prompt:**

> I want you to generate a full‑stack web application similar to Airtable but simplified and optimized for local use. The backend must use **Python Django** with **Django Rest Framework (DRF)** and the frontend should use **React** (with Vite or Next.js). The solution must include authentication, multiple user roles, dynamic table creation, and dashboard analytics.

#### ⚙️ Functional Requirements
1. **User Authentication**
   - Email + password registration and login.
   - JWT‑based authentication (access + refresh tokens).
   - Role-based access control.

2. **User Roles**
   - **Master:** Full control (create/edit/delete any base, manage users).
   - **Master Editor:** Can edit all bases and create new ones but cannot delete bases.
   - **Master Viewer:** Can view all bases but cannot edit or create.
   - **Admin:** Can create/edit records and fields only within assigned bases.
   - **Viewer:** Can only view assigned bases.

3. **Base Management (Like Airtable Bases)**
   - Each base can have unique headers (columns) defined dynamically by an admin/master.
   - Columns (fields) can be of types: text, number, date, boolean, single_select, multi_select.
   - Each user should have access only to their assigned bases unless they are a master‑level user.

4. **Record Management**
   - CRUD operations on records with validation based on field type.
   - Store record data in JSONB format for flexibility.
   - Pagination and filtering for large datasets (~100k records per base).

5. **Permissions & Visibility Logic**
   - Enforce per‑base access using memberships.
   - Global permissions for master roles.
   - Role checks should be enforced at both API and UI level.

6. **Dashboard & Analytics**
   - Each base should have a simple dashboard showing:
     - Record count per base.
     - Aggregations and charts (bar, line, pie, etc.) per field.
   - Global dashboard combining all bases (for masters).

7. **Frontend (React)**
   - Authentication pages (login/register).
   - Dashboard and base picker.
   - Spreadsheet‑like grid for records using TanStack Table.
   - Chart components using Plotly or Recharts.
   - Responsive UI using TailwindCSS.

8. **Backend (Django + DRF)**
   - Models for `User`, `Base`, `Field`, `Record`, `RecordValue`, `BaseMembership`.
   - Role and permission logic in custom DRF permission classes.
   - Flexible schema via JSONField/JSONB.
   - Analytics endpoints returning data ready for charting.
   - PostgreSQL database.

9. **Performance Considerations**
   - Optimized queries using `select_related` and indexes on JSONB.
   - Pagination default: 200 rows per page.
   - Caching layer for aggregate data.

10. **Deployment / Setup**
   - Must run **locally without Docker**.
   - Use `.env` for DB and secret configuration.
   - Include setup guide with steps to migrate and run.

#### 📊 Non‑Functional Requirements
- Scalable code structure for future features (views, automations, CSV import/export).
- Clean architecture (separate apps/modules per concern).
- Type‑safe and PEP8‑compliant Python.
- Reusable frontend components.
- Clear folder structure and comments.

#### 🧩 Tech Stack Summary
| Layer | Technology |
|-------|-------------|
| Backend | Django 5 + DRF + SimpleJWT + psycopg3 |
| Frontend | React + Vite + TanStack Table + Plotly.js |
| Database | PostgreSQL |
| Auth | JWT (access + refresh) |
| Styling | TailwindCSS |
| API Docs | DRF Schema + Swagger/OpenAPI |

#### 📘 Expected Output
- Complete codebase with backend and frontend folders.
- API endpoints for all models and roles.
- JWT authentication working out‑of‑the‑box.
- Ready‑to‑run local setup instructions.
- Example `.env` file and sample curl commands for testing.
- Example charts for dashboard data.

---

💡 *Optional Add‑ons (if supported by the AI builder):*
- CSV import/export endpoints.
- Saved views (filters/sorts).
- Audit trail (row history).
- Webhooks for automations.

---

## 🧠 AI-Optimized Architecture Overview + Generation Steps

To improve results with multi-stage generators (e.g., GPT-Engineer, Claude Code, or Cursor), prepend the following planning and execution guidance to the main prompt:

1. **Architecture Planning**
   - Summarize the overall system architecture, highlighting how Django/DRF, PostgreSQL, and React will interact.
   - Define backend apps/modules (e.g., `accounts`, `bases`, `records`, `analytics`, `common`).
   - Outline data flow for authentication, base access, record CRUD, and analytics generation.
   - Document key models, their relationships, and indexes (especially for JSONB fields).
   - Specify API endpoints, serializers, and permission classes per module.
   - Plan caching strategy for analytics and pagination approach for large datasets.
   - Note environment variables, settings modules, and local setup steps.

2. **Backend Generation Steps**
   - Scaffold the Django project and required apps.
   - Configure PostgreSQL connection, `.env` loading, and DRF + SimpleJWT.
   - Implement models, migrations, and admin registrations.
   - Create serializers, viewsets, routers, and permission classes.
   - Add pagination, filtering, and caching utilities.
   - Build analytics services and DRF schema/Swagger integration.
   - Write unit tests or sample usage scripts for critical flows.

3. **Frontend Generation Steps**
   - Scaffold the React project with Vite, TailwindCSS, TanStack Table, and Plotly integrations.
   - Set up routing, global state (e.g., React Query + Zustand/Context), and API client with JWT handling.
   - Implement authentication pages (login/register) with form validation.
   - Create dashboard pages (global + per-base) with charts and counts.
   - Build base picker, spreadsheet-like grid, and record CRUD modals.
   - Enforce role-based UI controls and guard routes with permissions.
   - Provide reusable components (tables, forms, charts, layout) and responsive design.

4. **Testing & Polish**
   - Describe backend testing strategy (API tests, permission checks, analytics validation).
   - Outline frontend testing (component/unit tests, smoke tests) if supported.
   - Include instructions for manual verification with sample data and curl commands.
   - Generate README/setup docs, example `.env`, and usage snippets.

5. **Iteration Guidance**
   - Encourage the generator to produce code in phases (plan → scaffold → implement → refine).
   - Remind it to double-check role permissions and data validation logic before final output.
   - Request a final summary of implemented features, limitations, and next steps.

Appending this section ensures the generator first plans the architecture, then implements the solution in structured stages, leading to more reliable and coherent code generation.

---

Would you like me to add any other specialized instructions (e.g., CSV import/export focus, automation hooks) to tailor the generator’s output even further?

