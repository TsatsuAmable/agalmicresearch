export function knowledgeObjectSchema(z) {
  return z.object({
    id: z.string(),
    title: z.string(),
    kind: z.string(),
    layer: z.string(),
    commitment: z.string(),
    meaningful: z.boolean().optional(),
    topics: z.array(z.string()),
    status: z.string(),
    summary: z.string(),
    direction: z.string(),
    href: z.string(),
    related: z.array(z.string()).default([]),
    version: z.string().optional(),
    created: z.string().optional(),
    updated: z.string().optional(),
    epistemicStatus: z.string().optional(),
    lineageStatus: z.string().optional(),
    predecessors: z.array(z.string()).default([]),
    successors: z.array(z.string()).default([]),
    supersedes: z.array(z.string()).default([]),
    supersededBy: z.array(z.string()).default([]),
    provenanceRef: z.string().optional(),
    handoffRefs: z.array(z.string()).default([]),
    aliases: z.array(z.string()).default([]),
  });
}

export function historyEventSchema(z) {
  return z.object({
    id: z.string(),
    slug: z.string(),
    date: z.string(),
    state: z.string(),
    previous_title: z.string(),
    current_title: z.string(),
    reason: z.string(),
    current_href: z.string(),
    object_ids: z.array(z.string()),
    legacy_paths: z.array(z.string()).default([]),
  });
}

export function handoffSchema(z) {
  return z.object({
    id: z.string(),
    title: z.string(),
    origin: z.string(),
    state: z.string().optional(),
    priority: z.string().optional(),
    question: z.string().optional(),
    expertise_needed: z.array(z.string()).default([]),
    what_exists: z.string().optional(),
    requested_contribution: z.string().optional(),
    completion_condition: z.string().optional(),
    links: z.array(z.string()).default([]),
  });
}
