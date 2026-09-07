import type { AstroIntegration } from 'astro';

export interface KnowledgeObject {
  id: string;
  title: string;
  kind: string;
  layer: string;
  commitment: string;
  meaningful?: boolean;
  topics: string[];
  status: string;
  summary: string;
  direction: string;
  href: string;
  related: string[];
  version?: string;
  created?: string;
  updated?: string;
  epistemicStatus?: string;
  lineageStatus?: string;
  predecessors?: string[];
  successors?: string[];
  supersedes?: string[];
  supersededBy?: string[];
  provenanceRef?: string;
  handoffRefs?: string[];
  aliases?: string[];
}

export interface KnowledgeRegistry {
  schema_version?: string;
  updated?: string;
  purpose?: string;
  objects: KnowledgeObject[];
}

export interface Handoff {
  id: string;
  title: string;
  origin: string;
  [key: string]: unknown;
}

export interface HistoryEvent {
  id: string;
  slug: string;
  date: string;
  state: string;
  previous_title: string;
  current_title: string;
  reason: string;
  current_href: string;
  object_ids: string[];
  legacy_paths?: string[];
}

export interface SearchOptions {
  output?: string;
  titleComparison?: 'exact' | 'case-insensitive';
  maxBodyCharacters?: number;
  ignoreAttribute?: string;
}

export interface AstroAgalmicOptions {
  registry?: string;
  history?: string | null;
  handoffs?: string | null;
  researchKinds?: string[];
  requiredFields?: string[];
  knownOrigins?: string[] | null;
  validate?: boolean;
  search?: false | SearchOptions;
}

export interface ValidationResult {
  errors: string[];
  warnings: string[];
  counts: { objects: number; handoffs: number; history: number };
}

export default function astroAgalmic(options?: AstroAgalmicOptions): AstroIntegration;
export function validateKnowledge(options: {
  registry: KnowledgeRegistry | KnowledgeObject[];
  handoffs?: { handoffs: Handoff[] } | Handoff[] | null;
  history?: { events: HistoryEvent[] } | HistoryEvent[] | null;
  requiredFields?: string[];
  researchKinds?: string[];
  knownOrigins?: string[] | null;
}): ValidationResult;
export function buildSearchIndex(options: Record<string, unknown>): { schema_version: string; generated_at: string; count: number; entries: unknown[] };
export function normalizePathname(href?: string): string;
export function htmlToText(value?: string): string;
export function readJsonFile(root: URL | string, source?: string | null): unknown;
