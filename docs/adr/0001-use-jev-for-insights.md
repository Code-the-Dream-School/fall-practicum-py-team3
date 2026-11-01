---
status: proposed
---

# Use Jev for judgments and gpt-4o-mini for Insight text

Sprint 3 needs an LLM Enrichment stage that adds something a rule-based transform cannot. Python computes the facts for each Tracked City month, TypeSafe's Jev model (via AI/ML API) makes typed judgments about them (pollution profile, how unusual, probability that it is "getting worse"), and `gpt-4o-mini` writes a short Insight from those facts and judgments. If the written text is unusable, a fixed template writes the Insight from the judgments instead. Jev returns decisions, not prose, so the judgments cannot invent claims; it is also cheap (input listed at $0.042–0.058 per 1M tokens in November 2026, output free; [API reference](https://docs.aimlapi.com/api-references/decision-models/typesafe/jev), [model page](https://aimlapi.com/models/typesafe-jev)). Details: [LLM Enrichment contract](../architecture/llm-enrichment.md).

## Considered Options

- **Text LLM does everything**: one call, but labels and wording both come from a model that can invent claims on health-related text.
- **Jev judges, templates write**: safest, but stiff wording that reads like a rule-based transform.
- **Jev judges, a text LLM writes, template fallback** (chosen): typed judgments where we need reliability, natural wording where we want it, and every month still gets an Insight. Both models run through AI/ML API.

## Consequences

- LLMs are weak at arithmetic, counting and date comparison, so all numbers are computed in Python before asking.
- Jev launched in September 2026. Only the enrichment module knows the providers, so either model can be swapped without touching other stages.
- The writer's output is checked (length, health-advice blocklist); failures fall back to the template.
- Health Tips stay a fixed EPA-based lookup and are not part of this decision.
