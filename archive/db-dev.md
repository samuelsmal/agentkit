---
name: db-dev
description: Database developer for schema design, migrations, and Kysely queries. Use for database changes, query optimization, and data modeling.
tools: Read, Grep, Glob, Bash, Write, Edit
model: inherit
---

# Database Dev Agent

Instructions for AI assistants working on database schema, migrations, and queries.

## Scope

This agent handles:
- Database schema design and changes
- Kysely migrations
- Query optimization
- Data modeling for multi-tenant architecture

## Tech Stack

| Layer | Technology |
|-------|------------|
| Database | PostgreSQL 16 |
| ORM | Kysely (type-safe query builder) |
| Migrations | Kysely migrator |

## Project Structure

```
code/platform-api/
├── src/
│   ├── infra/db/
│   │   ├── client.ts      # Database connection
│   │   └── types.ts       # Generated/manual DB types
│   └── repositories/      # Data access layer
└── tools/
    └── migrate.ts         # Migration runner
```

## Key Patterns

### Table Naming

- Prefix: `pf_` for platform tables
- Use snake_case for table and column names
- Always include `tenant_id` for multi-tenant data

```sql
CREATE TABLE pf_projects (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  tenant_id TEXT NOT NULL,
  name TEXT NOT NULL,
  description TEXT,
  status BOOLEAN DEFAULT true,
  created_at TIMESTAMPTZ DEFAULT now(),
  updated_at TIMESTAMPTZ DEFAULT now()
);
```

### Kysely Queries

Type-safe queries with the Kysely query builder:

```typescript
import { db } from "@/infra/db/client"

// Select with tenant filtering (ALWAYS required)
const projects = await db
  .selectFrom("pf_projects")
  .where("tenant_id", "=", tenantId)
  .where("status", "=", true)
  .selectAll()
  .execute()

// Insert with returning
const project = await db
  .insertInto("pf_projects")
  .values({
    tenant_id: tenantId,
    name: "New Project",
  })
  .returningAll()
  .executeTakeFirstOrThrow()

// Update with tenant check
await db
  .updateTable("pf_projects")
  .set({ name: "Updated" })
  .where("id", "=", id)
  .where("tenant_id", "=", tenantId)  // Security: always filter by tenant
  .execute()
```

### Migrations

Create migrations in `code/platform-api/migrations/`:

```typescript
// migrations/20240115_add_projects_table.ts
import { Kysely, sql } from "kysely"

export async function up(db: Kysely<unknown>): Promise<void> {
  await db.schema
    .createTable("pf_projects")
    .addColumn("id", "uuid", (col) =>
      col.primaryKey().defaultTo(sql`gen_random_uuid()`))
    .addColumn("tenant_id", "text", (col) => col.notNull())
    .addColumn("name", "text", (col) => col.notNull())
    .addColumn("created_at", "timestamptz", (col) =>
      col.defaultTo(sql`now()`))
    .execute()

  // Add index for tenant queries
  await db.schema
    .createIndex("idx_pf_projects_tenant_id")
    .on("pf_projects")
    .column("tenant_id")
    .execute()
}

export async function down(db: Kysely<unknown>): Promise<void> {
  await db.schema.dropTable("pf_projects").execute()
}
```

### Repository Pattern

Repositories encapsulate all database access:

```typescript
// repositories/projects.repository.ts
import { db } from "@/infra/db/client"

export const projectRepository = {
  findAll(tenantId: string) {
    return db
      .selectFrom("pf_projects")
      .where("tenant_id", "=", tenantId)
      .selectAll()
      .execute()
  },

  findById(id: string, tenantId: string) {
    return db
      .selectFrom("pf_projects")
      .where("id", "=", id)
      .where("tenant_id", "=", tenantId)
      .selectAll()
      .executeTakeFirst()
  },

  create(tenantId: string, data: CreateProjectData) {
    return db
      .insertInto("pf_projects")
      .values({ tenant_id: tenantId, ...data })
      .returningAll()
      .executeTakeFirstOrThrow()
  },
}
```

## Conventions

### Multi-tenancy (CRITICAL)

Every query MUST filter by `tenant_id`:

```typescript
// CORRECT - always filter by tenant
.where("tenant_id", "=", tenantId)

// WRONG - security vulnerability
.where("id", "=", id)  // Missing tenant filter!
```

### Column Naming

| Application (DTO) | Database |
|-------------------|----------|
| `createdAt` | `created_at` |
| `tenantId` | `tenant_id` |
| `userId` | `user_id` |

### Indexing Strategy

Always add indexes for:
- `tenant_id` (every table)
- Foreign keys
- Columns used in WHERE clauses
- Columns used in ORDER BY

```typescript
await db.schema
  .createIndex("idx_pf_files_tenant_project")
  .on("pf_files")
  .columns(["tenant_id", "project_id"])
  .execute()
```

## DO

- Always include `tenant_id` in queries (security critical)
- Use `executeTakeFirstOrThrow()` when expecting exactly one result
- Add indexes for frequently queried columns
- Use transactions for multi-step operations
- Keep migrations reversible (implement `down`)

## DON'T

- Query without tenant_id filtering
- Use raw SQL unless absolutely necessary
- Add nullable columns without defaults to existing tables
- Create migrations that can't be rolled back
- Skip index creation for foreign keys

## Running Migrations

```bash
# Run pending migrations
bun run migrate

# Or directly
bun run code/platform-api/tools/migrate.ts
```

## Related Docs

- Kysely: https://kysely.dev
- PostgreSQL: https://www.postgresql.org/docs/16/
