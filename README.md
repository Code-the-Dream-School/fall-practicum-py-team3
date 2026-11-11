# City Air Tracker

Batch data pipeline comparing air quality across U.S. cities and Census divisions, from a laptop to AWS.

- Setup: [SETUP.md](./SETUP.md)
- Reference docs index: [docs/docs_toc.md](./docs/docs_toc.md)
- Team notes and decisions: [team-documentation/toc.md](./team-documentation/toc.md)
- Shared vocabulary: [team-documentation/CONTEXT.md](./team-documentation/CONTEXT.md)

After setup:
- Run pipeline: `cd services/pipeline && python run_pipeline.py`
- Run tests: `cd services/pipeline && pytest`