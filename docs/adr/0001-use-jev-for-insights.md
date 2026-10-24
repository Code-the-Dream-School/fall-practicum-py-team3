---
status: proposed
---

# Use Jev for Insights

Sprint 3 needs an AI stage that adds something a rule-based transform cannot. We propose that Python computes the facts for each city-month, TypeSafe's Jev model (via AI/ML API) makes typed judgments about them (choice of likely cause, score for how unusual, yes/no for "getting worse"), and fixed sentence templates turn the judgments into an Insight. Jev returns decisions, not prose, so it cannot invent claims, and it is far cheaper than a text LLM (about $0.05 per 1M input tokens, output free, as listed in October 2026).

## Considered Options

- **Text LLM writes the Insight**: most flexible wording, but higher cost and risk of made-up claims on health-related text.
- **Jev judges, a text LLM writes**: two providers, two keys, more cost.
- **Jev judges, templates write** (chosen).

## Consequences

- Jev is weak at arithmetic, counting and date comparison, so all numbers are computed in Python before asking.
- Jev launched in September 2026. Only the Jev Judge module knows the provider, so it can be swapped for a text LLM without touching other stages.
- Health Tips stay a fixed EPA-based lookup and are not part of this decision.
