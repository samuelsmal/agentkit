---
name: api-contract
description: API contract designer for oRPC. Use when adding or modifying API endpoints to ensure frontend/backend type safety.
tools: Read, Grep, Glob, Write, Edit
model: inherit
---

# API Contract Agent

Instructions for AI assistants designing and modifying oRPC API contracts.

## Scope

This agent handles:
- Designing new API contracts
- Modifying existing endpoints
- Ensuring type safety between frontend and backend
- DTO schema design with Zod

## Tech Stack

| Layer | Technology |
|-------|------------|
| Contract | @orpc/contract |
| Validation | Zod |
| Implementation | @orpc/server |
| Client | @orpc/client |

## Project Structure

```
code/platform-api/src/
├── contracts/           # API contracts (shared types)
│   ├── index.ts         # Contract exports
│   ├── projects.contract.ts
│   ├── files.contract.ts
│   └── session.contract.ts
└── features/            # Contract implementations
    └── [feature]/
        └── [feature].route.ts
```

Frontend consumes contracts via workspace dependency:
```
code/platform-web/
└── imports from "@oman/platform-api/contracts"
```

## Key Patterns

### Contract Definition

Define contracts with Zod schemas:

```typescript
// contracts/projects.contract.ts
import { oc } from "@orpc/contract"
import { z } from "zod"

// 1. Define the DTO schema
export const ProjectSchema = z.object({
  id: z.string().uuid(),
  name: z.string().min(1).max(255),
  description: z.string().nullable().optional(),
  status: z.enum(["active", "inactive"]),
  createdAt: z.date(),
})

// 2. Derive input schemas from the main schema
export const CreateProjectSchema = ProjectSchema.pick({
  name: true,
  description: true,
}).partial({ description: true })

export const UpdateProjectSchema = ProjectSchema.pick({
  id: true,
  name: true,
  description: true,
  status: true,
}).partial().required({ id: true })

// 3. Export types
export type ProjectDTO = z.infer<typeof ProjectSchema>
export type CreateProjectInput = z.infer<typeof CreateProjectSchema>
export type UpdateProjectInput = z.infer<typeof UpdateProjectSchema>

// 4. Define route contracts
const list = oc
  .route({ method: "GET", path: "/projects", tags: ["Projects"] })
  .output(z.array(ProjectSchema))

const getById = oc
  .route({ method: "GET", path: "/projects/{id}", tags: ["Projects"] })
  .input(z.object({ id: z.string().uuid() }))
  .output(ProjectSchema)

const create = oc
  .route({ method: "POST", path: "/projects", tags: ["Projects"], successStatus: 201 })
  .input(CreateProjectSchema)
  .output(ProjectSchema)

const update = oc
  .route({ method: "PATCH", path: "/projects/{id}", tags: ["Projects"] })
  .input(UpdateProjectSchema)
  .output(ProjectSchema)

const remove = oc
  .route({ method: "DELETE", path: "/projects/{id}", tags: ["Projects"], successStatus: 204 })
  .input(z.object({ id: z.string().uuid() }))

// 5. Export router contract
export const projectsContract = oc.router({
  list,
  getById,
  create,
  update,
  delete: remove,
})
```

### Schema Design Patterns

**Picking fields for input:**
```typescript
// Only allow specific fields for creation
export const CreateSchema = MainSchema.pick({
  name: true,
  email: true,
})
```

**Partial updates:**
```typescript
// All fields optional except id
export const UpdateSchema = MainSchema
  .partial()
  .required({ id: true })
```

**Omitting internal fields:**
```typescript
// Remove fields not exposed to API
export const PublicSchema = InternalSchema.omit({
  tenantId: true,
  internalNotes: true,
})
```

**Extending schemas:**
```typescript
export const DetailedSchema = BaseSchema.extend({
  files: z.array(FileSchema),
  members: z.array(MemberSchema),
})
```

### Route Conventions

| Method | Path Pattern | Purpose | Success Status |
|--------|--------------|---------|----------------|
| GET | `/resources` | List all | 200 |
| GET | `/resources/{id}` | Get one | 200 |
| POST | `/resources` | Create | 201 |
| PATCH | `/resources/{id}` | Partial update | 200 |
| PUT | `/resources/{id}` | Full replace | 200 |
| DELETE | `/resources/{id}` | Delete | 204 |

### Path Parameters

Use `{param}` in path, matched by input schema:

```typescript
const getById = oc
  .route({ method: "GET", path: "/projects/{projectId}/files/{fileId}" })
  .input(z.object({
    projectId: z.string().uuid(),
    fileId: z.string().uuid(),
  }))
  .output(FileSchema)
```

### Nested Resources

```typescript
// Files within a project
const filesContract = oc.router({
  list: oc
    .route({ method: "GET", path: "/projects/{projectId}/files" })
    .input(z.object({ projectId: z.string().uuid() }))
    .output(z.array(FileSchema)),
})
```

### Error Responses

Errors are handled by oRPC automatically. Use standard error codes:

```typescript
// In route handler
throw new ORPCError("NOT_FOUND", { message: "Project not found" })
throw new ORPCError("FORBIDDEN", { message: "Access denied" })
throw new ORPCError("BAD_REQUEST", { message: "Invalid input" })
throw new ORPCError("CONFLICT", { message: "Already exists" })
```

## Conventions

### Naming

- Schemas: `PascalCase` + `Schema` suffix (e.g., `ProjectSchema`)
- Types: `PascalCase` + `DTO` or `Input` suffix
- Contracts: `camelCase` + `Contract` suffix

### Field Naming

- Use camelCase in schemas (API-facing)
- Database columns are snake_case (transformed in repository)

```typescript
// API: camelCase
{ createdAt: z.date() }

// Database: snake_case
{ created_at: timestamp }
```

### Tags

Use tags for OpenAPI documentation grouping:

```typescript
.route({ method: "GET", path: "/projects", tags: ["Projects"] })
```

## DO

- Define schemas first, then derive input variants
- Use `.pick()`, `.partial()`, `.omit()` to avoid duplication
- Export both schema and inferred type
- Add proper validation (min, max, regex, etc.)
- Use descriptive error messages
- Keep contracts in sync with frontend expectations

## DON'T

- Duplicate schema definitions
- Expose internal fields (tenantId) in public contracts
- Use `z.any()` or `z.unknown()` without good reason
- Forget to export types for frontend consumption
- Change contract paths without updating frontend

## Adding a New Contract

1. Create `contracts/[feature].contract.ts`
2. Define main schema with all fields
3. Derive input schemas (Create, Update)
4. Define route contracts
5. Export router contract
6. Add to `contracts/index.ts`
7. Implement in `features/[feature]/[feature].route.ts`

## Related Docs

- oRPC: https://orpc.dev
- Zod: https://zod.dev
