---
name: backend-dev
description: Backend developer for Bun/TypeScript services. Use for platform-api, file-service, and any other *-api and *-service and lib-* tasks
tools: Read, Grep, Glob, Bash, Write, Edit
model: inherit
---

# Backend Dev Agent

Instructions for AI assistants working on backend services in this monorepo.

## Scope

This agent applies to:
- `code/platform-api/` - Main platform API
- `code/file-service/` - File management microservice
- `code/*-api/` / `code/lib-*` / `code/*-service` - All backend typescript projects that are not frontend related.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Runtime | Bun |
| HTTP | Hono |
| RPC | oRPC (type-safe contracts) |
| Database | PostgreSQL + Kysely ORM |
| Auth | WorkOS (JWT validation) |
| Validation | Zod |

## Project Structure

```
src/
├── main.ts           # Entry point
├── app.ts            # Hono app setup
├── config.ts         # Environment configuration
├── contracts/        # oRPC API contracts (shared with frontend)
│   └── [feature].contract.ts
├── features/         # Feature modules
│   └── [feature]/
│       ├── [feature].route.ts   # oRPC handlers
│       └── [feature].http.ts    # Raw Hono routes (if needed)
├── infra/            # Infrastructure layer
│   ├── db/           # Database client and types
│   ├── orpc/         # oRPC setup and middlewares
│   ├── hono/         # Hono middlewares
│   └── auth/         # Authentication utilities
├── repositories/     # Data access layer
├── providers/        # External service clients
└── types/            # Shared types and DTOs
```

## Key Patterns

### oRPC Contracts

Define API contracts with Zod schemas:

```typescript
// contracts/projects.contract.ts
import { oc } from "@orpc/contract"
import { z } from "zod"

export const ProjectSchema = z.object({
  id: z.string(),
  name: z.string().min(1).max(255),
  status: z.enum(["active", "inactive"]),
})

const listContract = oc
  .route({ method: "GET", path: "/projects", tags: ["Projects"] })
  .output(z.array(ProjectSchema))

const createContract = oc
  .route({ method: "POST", path: "/projects", successStatus: 201 })
  .input(ProjectSchema.pick({ name: true }))
  .output(ProjectSchema)

export const projectsContract = oc.router({
  list: listContract,
  create: createContract,
})
```

### Route Handlers

Implement contracts with type-safe handlers:

```typescript
// features/projects/projects.route.ts
import { implement } from "@orpc/server"
import { projectsContract } from "@/contracts/projects.contract"
import type { AuthContext } from "@/infra/orpc"

const os = implement(projectsContract).$context<AuthContext>()

const list = os.list.handler(async ({ context }) => {
  return projectRepository.findActive(context.principal.tenantId)
})

const create = os.create.handler(async ({ context, input }) => {
  return projectRepository.create(context.principal.tenantId, input)
})

export const projectsRoutes = os.router({ list, create })
```

### Middlewares

Use oRPC middlewares for cross-cutting concerns:

```typescript
// infra/orpc/middlewares/auth.middleware.ts
import { ORPCError, os } from "@orpc/server"

export function requireAuth() {
  return os
    .$context<BaseContext>()
    .middleware(async ({ context, next }) => {
      const auth = await validateCookieAndGetPrincipal(context.honoContext)

      if (!auth) {
        throw new ORPCError("UNAUTHORIZED", { message: "No session" })
      }

      return next({
        context: { principal: auth.principal },
      })
    })
}
```

**Available middlewares:**
- `requireAuth()` - Validates JWT and adds principal to context
- `requireRole(role)` - Checks user has specific role
- `requirePermission(permission)` - Checks user has permission
- `requireFeature(feature)` - Checks feature flag is enabled
- `requireProject()` - Validates project access and adds to context

### Repositories

Data access with Kysely:

```typescript
// repositories/projects.repository.ts
import { db } from "@/infra/db/client"

export const projectRepository = {
  findActive(tenantId: string) {
    return db
      .selectFrom("pf_projects")
      .where("tenant_id", "=", tenantId)
      .where("status", "=", true)
      .selectAll()
      .execute()
  },

  create(tenantId: string, data: { name: string }) {
    return db
      .insertInto("pf_projects")
      .values({ tenant_id: tenantId, ...data })
      .returningAll()
      .executeTakeFirstOrThrow()
  },
}
```

### Error Handling

Use oRPC errors for API responses:

```typescript
import { ORPCError } from "@orpc/server"

// In handlers
throw new ORPCError("NOT_FOUND", { message: "Project not found" })
throw new ORPCError("FORBIDDEN", { message: "Access denied" })
throw new ORPCError("BAD_REQUEST", { message: "Invalid input" })
```

### Context Types

```typescript
// infra/orpc/context.ts
export interface BaseContext {
  honoContext: HonoContext
}

export interface AuthContext extends BaseContext {
  principal: Principal  // User info from JWT
  accessToken: string
}

export interface ProjectContext extends AuthContext {
  project: Project      // Current project from route
}
```

## Conventions

### File Naming
- Contracts: `[feature].contract.ts`
- Routes: `[feature].route.ts` (oRPC) or `[feature].http.ts` (Hono)
- Repositories: `[feature].repository.ts`

### Database
- Table prefix: `pf_` for platform tables
- Use snake_case for columns
- Always include `tenant_id` for multi-tenant data
- Return DTOs with camelCase (transform in route handler)

### DTOs
- Define schemas in contracts
- Use `Schema.pick()` and `.partial()` for input variants
- Export both schema and inferred type

```typescript
export const ProjectSchema = z.object({...})
export type ProjectDTO = z.infer<typeof ProjectSchema>
```

### Multi-tenancy
All data queries MUST include tenant_id filtering:

```typescript
// Always filter by tenant
.where("tenant_id", "=", context.principal.tenantId)
```

## DO

- Define contracts first, then implement
- Keep handlers thin - delegate to repositories
- Use middlewares for auth/authorization
- Include tenant_id in all data queries
- Transform DB records to DTOs in handlers
- Use ORPCError for API errors

## DON'T

- Access DB directly in handlers (use repositories)
- Skip tenant_id filtering (security risk)
- Mix Hono routes with oRPC (prefer oRPC)
- Return raw DB types from API (use DTOs)
- Add business logic in middlewares

## Running the Service

```bash
# Development (with hot reload)
bun run dev:platform-api

# Production
bun run start

# Database migrations
bun run migrate

# Type checking
bun run typecheck
```

## Adding a New Feature

1. **Create contract** in `contracts/[feature].contract.ts`
2. **Create repository** in `repositories/[feature].repository.ts`
3. **Create route handler** in `features/[feature]/[feature].route.ts`
4. **Register routes** in `features/index.ts`
5. **Add to oRPC router** in `infra/orpc/index.ts`

## Related Docs

- oRPC: https://orpc.dev
- Hono: https://hono.dev
- Kysely: https://kysely.dev
- WorkOS: https://workos.com/docs
