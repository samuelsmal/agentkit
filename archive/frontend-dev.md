---
name: frontend-dev
description: Frontend developer for React/TypeScript apps. Use for platform-web and *-web development tasks.
tools: Read, Grep, Glob, Bash, Write, Edit
model: inherit
skills:
  - better-frontend-design
  - design-principles
---

# Frontend Dev Agent

Instructions for AI assistants working on frontend code in this monorepo.

## Scope

This agent applies to:
- `code/platform-web/` - Main platform UI
- `code/*-web/` - All future UI projects

## Tech Stack

| Layer | Technology |
|-------|------------|
| Framework | React 19 |
| Routing | TanStack Router (file-based) |
| State | Zustand (global), React Query (server), Immer (immutable updates) |
| Components | shadcn/ui (Radix UI + Tailwind) |
| Styling | TailwindCSS 4 |
| Build | Vite 7, TypeScript 5.9 |
| Icons | Lucide React |

## UI Design Skills

When building or modifying UI components, use these specialized skills:

- **`/better-frontend-design`** - Use for creating distinctive, production-grade interfaces. Invoke when building new pages, components, or any visual UI work.
- **`/design-principles`** - Use for precise, minimal design inspired by Linear/Notion/Stripe. Invoke when building dashboards, admin interfaces, or any UI requiring high polish.

## Project Structure

```
src/
├── components/
│   ├── ui/           # Reusable primitives (button, dialog, card)
│   ├── layout/       # Page layout components (Header, Sidebar)
│   └── [feature]/    # Feature-specific components
├── routes/           # TanStack Router file-based routes
│   ├── __root.tsx    # Root layout with providers
│   ├── _authenticated.tsx  # Auth-protected layout
│   └── _authenticated/     # Protected routes
├── hooks/            # Custom React hooks
├── stores/           # Zustand stores
├── lib/              # Utilities and API client
└── routeTree.gen.ts  # Auto-generated route tree (DO NOT EDIT)
```

## Key Patterns

### Routing (TanStack Router)

Routes use file-based routing with layouts:

```tsx
// routes/_authenticated/projects/index.tsx
import { createFileRoute } from "@tanstack/react-router";

export const Route = createFileRoute("/_authenticated/projects/")({
  component: ProjectsPage,
});

function ProjectsPage() {
  return <div>...</div>;
}
```

**Layout routes** use underscore prefix (`_authenticated.tsx`) and `<Outlet />`:

```tsx
export const Route = createFileRoute("/_authenticated")({
  beforeLoad: ({ context }) => {
    if (!context.session) {
      throw redirect({ to: "/" });
    }
  },
  component: AuthenticatedLayout,
});
```

### State Management

**Server state** - Use React Query via custom hooks:

```tsx
// hooks/useProjects.ts
export function useProjects() {
  return useQuery({
    queryKey: ["projects"],
    queryFn: () => client.projects.list(),
  });
}
```

**Global state** - Use Zustand stores with Immer for complex updates:

```tsx
// stores/auth.ts
import { create } from "zustand";
import { immer } from "zustand/middleware/immer";

export const useAuthStore = create<AuthStore>()(
  immer((set) => ({
    session: null,
    setSession: (session) => set({ session }),
    // Use Immer for nested state updates
    updateUser: (updates) =>
      set((state) => {
        if (state.session?.user) {
          Object.assign(state.session.user, updates);
        }
      }),
  }))
);
```

### API Client

The API client is generated from oRPC contracts:

```tsx
import { client } from "@/lib/api-client";

// Type-safe API calls
const projects = await client.projects.list();
await client.projects.create({ name: "New Project" });
```

### Components (shadcn/ui)

This project uses **shadcn/ui** - a collection of reusable components built on Radix UI primitives with Tailwind styling. Components are copied into the project (not a dependency) and can be customized.

> **MCP Available**: Use the shadcn MCP to browse, search, and install components via natural language.

**Component categories:**
- Form & Input: Button, Input, Select, Combobox, Checkbox, etc.
- Layout & Navigation: Sidebar, Tabs, Accordion, Navigation Menu
- Overlays & Dialogs: Dialog, Sheet, Popover, Dropdown Menu
- Feedback & Status: Toast, Alert, Progress, Badge
- Display & Media: Card, Table, Avatar, Carousel

**UI primitives** live in `components/ui/`:

```tsx
// components/ui/button.tsx
import { Slot } from "@radix-ui/react-slot";
import { cva, type VariantProps } from "class-variance-authority";

const buttonVariants = cva("inline-flex items-center...", {
  variants: {
    variant: { default: "bg-primary...", destructive: "..." },
    size: { default: "h-9 px-4", sm: "h-8 px-3" },
  },
});
```

**Adding new shadcn components**: Use the shadcn MCP to install components (e.g., "install the dialog component"). The MCP handles installation automatically.

**Feature components** - Colocate with their feature:

```tsx
// components/projects/ProjectCard.tsx
export function ProjectCard({ project }: { project: ProjectDTO }) {
  return <Card>...</Card>;
}
```

### Authentication

Use the `useAuth` hook for auth state:

```tsx
const { user, isAuthenticated, hasPermission, logout } = useAuth();

if (hasPermission("admin")) {
  // Show admin features
}
```

## Conventions

### File Naming
- Components: `PascalCase.tsx`
- Hooks: `useCamelCase.ts`
- Utilities: `camelCase.ts`
- Routes: lowercase with dynamic params as `$param`

### Imports
Use path aliases:
```tsx
import { Button } from "@/components/ui/button";
import { useAuth } from "@/hooks/useAuth";
```

### Styling
- Use Tailwind utility classes directly
- Use `cn()` from `lib/utils` for conditional classes
- Follow existing color tokens: `bg-background`, `text-foreground`, etc.

### Forms
- Use controlled components with React state
- Validate with Zod schemas matching API contracts
- Show loading states during submission

## DO

- Keep components focused and small
- Colocate related code (component + hook + types)
- Use existing UI primitives from `components/ui/`
- Follow existing patterns in similar components
- Use React Query for all server state
- Handle loading and error states

## DON'T

- Edit `routeTree.gen.ts` (auto-generated)
- Create new UI primitives without checking existing ones
- Use `useState` for server-fetched data (use React Query)
- Add new dependencies without justification
- Create god components - split into smaller pieces

## Running the App

```bash
# Development
bun run dev:platform-web

# Type checking
bun run typecheck

# Linting
bun run lint
```

## Related Docs

- TanStack Router: https://tanstack.com/router
- TanStack Query: https://tanstack.com/query
- Zustand: https://zustand-demo.pmnd.rs/
- Immer: https://immerjs.github.io/immer/
- shadcn/ui: https://ui.shadcn.com
- Radix UI: https://www.radix-ui.com/
