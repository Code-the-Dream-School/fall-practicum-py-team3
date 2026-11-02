---
status: proposed
---

# Use OpenAI gpt-4o-mini to write Insights

Sprint 3 needs an LLM Enrichment stage that adds something a rule-based transform cannot: a plain-language Insight for each Tracked City month. Python computes the facts, `gpt-4o-mini` writes the Insight from them through the OpenAI API directly, and a fixed template writes it if the model's text is unusable. The courses use OpenAI too ([tools and prior coverage](../tools_and_prior_coverage.md)). Details: [LLM Enrichment contract](../architecture/llm-enrichment.md).

## Considered Options

- **OpenAI `gpt-4o-mini`, called directly** (chosen): the provider the team knows from the courses, one model, one secret, structured JSON output.
- **Jev judges, `gpt-4o-mini` writes** (deferred): TypeSafe's Jev model returns typed judgments (choice, score, yes/no) that cannot invent claims. It adds a second provider and model before we know we need typed judgments, so it was dropped from this proposal. It stays reachable on branch `DREAM-34-jev-enrichment` at commit `4dbd1e9`.
- **Templates only**: safest, but the wording reads like a rule-based transform.

## Consequences

- LLMs are weak at arithmetic, counting and date comparison, so all numbers are computed in Python before asking.
- Only the enrichment module knows the provider, so the model can be swapped without touching other stages. Typed judgments (pollution profile, how unusual, getting worse) are out of scope here; scikit-learn is planned for them.
- The writer's output is checked (length, health-advice blocklist); unusable output falls back to the template. Transient API errors leave the month `failed` so the next run retries it.
- OpenAI lists `gpt-4o-mini` ([`gpt-4o-mini-2024-07-18`](https://platform.openai.com/docs/deprecations)) for removal on January 14, 2027, with `gpt-6-luna` as the recommended replacement. The model ID lives in one place and is stored per row, so moving to another model means one config change plus a `--re-enrich`.
- Health Tips stay a fixed EPA-based lookup and are not part of this decision.
