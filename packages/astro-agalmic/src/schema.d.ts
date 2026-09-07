export interface ZodLike {
  string(): any;
  boolean(): any;
  array(schema: any): any;
  object(shape: Record<string, any>): any;
}

export function knowledgeObjectSchema(z: ZodLike): any;
export function historyEventSchema(z: ZodLike): any;
export function handoffSchema(z: ZodLike): any;
