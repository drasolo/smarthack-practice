# Jury questions

Two-sentence answers, grounded in what we built. The `pitch-qa` skill rehearses these.

- **How do you know it works?** Answer with the eval table and the baseline row.
- **What does a false positive cost?** An inspector visit for nothing. Say how many of our top
  10 were real and how the ranking keeps visits for the strongest cases.
- **Where does customer data go?** Raw rows stay in the data folder. The LLM sees aggregates
  only, PII is masked, and every call is logged. A local model is the fallback.
- **Which AI Act category is this?** Not a safety component of supply, so not high risk under
  Annex III point 2. We keep human oversight and logs anyway.
- **What if someone hides instructions in the data?** The prompt treats input as data, and the
  output must match a fixed schema and use only evidence numbers. Show the grounded check.
- **Does it scale to 2 million meters at 96 readings a day?** The scoring is a daily batch of
  aggregates in DuckDB here, Spark on PPC's EMR in production.
- **Why an LLM at all?** Detection is plain statistics. The LLM writes the explanation an
  inspector reads, which is where time goes today.
- **What would you build with another month?**
