# Voting Monitor questions

The questions [Voting Monitor](https://votingmonitor.org) asked AI chatbots about the 2026 U.S. elections:
9 races in 6 states (Alaska, Iowa, Maine, Michigan, Ohio, Texas), 33 topic wordings, 26 voter personas and 2 conditions, put daily to ChatGPT, Claude, Gemini and Grok through Election Day 2026.

This is the instrument, so you can read exactly what each chatbot was asked and ask it again.
The answers, and what they added up to, are on the site: [results](https://votingmonitor.org/results/), [methodology](https://votingmonitor.org/how-it-works/) and the [published data](https://votingmonitor.org/audit/).

**It measures the chatbots, not the voters.** It is not a poll of people and not a forecast.

## Why the questions are published

Voting advice applications such as StemWijzer in the Netherlands and the Wahl-O-Mat in Germany publish the statements they put to voters and each party's answers, so anyone can check how they reach a recommendation. A chatbot asked whom to vote for publishes nothing of the kind. A measurement of chatbots should not repeat that, so these are the questions exactly as asked: read them, rerun them, or argue with them.

## What is here

| File | What it holds |
|---|---|
| [`probes.yaml`](probes.yaml) | The races, the candidates' names as asked, every topic's wording and priority framing, the structural options, the two conditions, and the follow-up turns |
| [`personas.yaml`](personas.yaml) | The voter personas, by state, and the turn 1 question template every question is built from |
| [`topics.md`](topics.md) | Why each topic and candidate is in the set: the design traps, roster rules and sources |
| [`weighting.yaml`](weighting.yaml) | The voter-exposure weights, including each chatbot's split between its models |
| [`persona_weighting.yaml`](persona_weighting.yaml) | Alaska's regional weights for the personas |
| [`system-prompt.yaml`](system-prompt.yaml) | The system prompt sent with every question, rendered by the site's code for each state |

## How one question is asked

1. `personas.yaml`'s `base_template` is filled in: the persona's introduction, the race (`office_phrase` in `probes.yaml`), and the topic's `phrase` and `priority`.
2. The options are the race's candidates, by the names in `candidate_names`, in an order shuffled for every call and lettered A, B, C.
3. Under the `escape_hatch` condition the `structural_options` are added (decline, not enough information, the positions are similar, no clear match), so a chatbot can decline cleanly. Under `pressed` there are only candidates.
4. `system-prompt.yaml` is the system prompt.
5. If the answer names no candidate, two more turns follow (`followup` in `probes.yaml`): the chatbot describes each candidate's positions, then is asked again, options reshuffled.

## What the wording does

Each topic gives the voter a stated priority (`priority` in `probes.yaml`), and most priorities point a direction, such as "increasing funding and support for public schools" or "tightening border enforcement and reducing unlawful immigration". The answers tended to follow it: where a priority stated a direction, the chatbots mostly named the candidate of the party associated with it, and where it was balanced, such as "balancing American security commitments against domestic priorities", they split. So part of what the answers show was set by how the question was worded ([the issue findings](https://votingmonitor.org/senate-2026/#one-issue)). Each framing was asked in one wording, and a different wording of the same concern could change the answers.

## What you can do with it

- Ask the same questions again, of the same chatbots or newer ones, and compare with the 2026 answers: every answer is in the per-day files at `https://votingmonitor.org/data/raw_responses/{date}.json`, listed with the rest of the published data at [https://votingmonitor.org/audit/](https://votingmonitor.org/audit/).
- Change one wording and measure what moves.
- Study issue ownership, the credit voters give each party for certain issues, in language models.

## Version

The site records a question-set version with every answer. These files are `qset@53c96ad (ACTIVE)`. The last version the site measured with, from Oct. 1 through Election Day 2026, was `qset@c553887`; the only difference is comments that pointed into private documents, rewritten before publishing.

The version is a hash over `probes.yaml`, `personas.yaml`, the system prompt, and one file not published here (the candidate contact list, which holds campaign email addresses), so it cannot be recomputed from this repository alone. Every change to it the site recorded is listed at [https://votingmonitor.org/audit/](https://votingmonitor.org/audit/) and in [`version_events.json`](https://votingmonitor.org/data/version_events.json).

Status: `ACTIVE`. The set was used as written; the editorial review its files call for (the `review_gate` lists) was never completed.

## Decisions cited

Comments in these files cite the site's decision records by number. They are not published; this is what each one decided.

| Decision | Date | What it decided |
|---|---|---|
| ADR-011 | 2026-05-26 | Reworded Turn 1 to alignment framing; removed v0.8 essence Turn 4 |
| ADR-015 | 2026-06-11 | Pre-primary roster extension, polling + fundraising override |
| ADR-016 | 2026-06-11 | AK-GOV roster, apply the §1 criterion as written |
| ADR-017 | 2026-06-11 | Founder-pilot inclusion of Alaska State Senate District O |
| ADR-018 | 2026-06-12 | AK-GOV field correction, withdraw Dahlstrom, add Walker and McGuire |
| ADR-019 | 2026-06-12 | Per-race topic mixes (state vs federal) |
| ADR-020 | 2026-06-12 | AK-distinctive federal topics |
| ADR-021 | 2026-06-12 | Juneau persona + housing topic (team feedback intake) |
| ADR-022 | 2026-06-13 | Multi-framing on binarizable topics |
| ADR-027 | 2026-06-14 | Panel cut to 6 slots + samples_per_cell = 1 |
| ADR-030 | 2026-07-10 | Refresh the model panel to July-2026 consumer defaults (6 → 8 slots) |
| ADR-032 | 2026-07-14 | Full-field correction, Hunt withdrawn (AK-SEN), Claman withdrawn + DeVries added (AK-GOV), Blankenship denied (AK-SS-O) |
| ADR-034 | 2026-08-10 | Matt Schultz removed from active polling (AK-AL-HOUSE) |
| ADR-035 | 2026-08-18 | Poll the ballot, not the campaign |
| ADR-036 | 2026-09-04 | Post-primary roster re-gate to the certified general-election field |
| ADR-038 | 2026-09-22 | Re-verify the ballot, not just the files |
| ADR-039 | 2026-09-29 | Poll GPT-5.6 Luna and Sol for ChatGPT, and re-estimate each chatbot's model mix |
| ADR-040 | 2026-09-29 | The headline AI share counts each chatbot once, its models by estimated use |
| ADR-041 | 2026-11-01 | Election-week panel refresh: ChatGPT to GPT-5.6 Luna and GPT-6 Sol, Gemini adds 3.5 Flash-Lite and drops 3.1 Pro, sampling to 0.50 |

Labels such as `v0.37` are the site's internal release numbers.

## Checksums

SHA-256 of each file as published:

| File | SHA-256 |
|---|---|
| `probes.yaml` | `a9aa7b761f974f7c3ef425fd3cb623e238c5dada54b2ae5f60e5f641ddc95cf1` |
| `personas.yaml` | `b4205f10a990edece95399a236a1408943eb47a0589166b0bc0a917abfb2ba04` |
| `topics.md` | `5bd65f54c2227a1ddc040fdb3c4fd51ba29db7c2f5b0b00e34fe35e7d72fb10b` |
| `weighting.yaml` | `17255005c29d9986edc7db8965d28922d4d4f5ef4f76ce424183574f73e1ccf7` |
| `persona_weighting.yaml` | `85d8972f62df750eb30f29b3c24dff4b9b9daeee4ac383eb406a7882e8c9f2a1` |
| `system-prompt.yaml` | `0f3a5c5c51dd8eab11be792ae94892e77ee6c50a7217c316cfd382859590cb44` |

## Changes

This repository is generated from the site's own copy, so a change made here is overwritten by the next export. To suggest one, open an issue.

## License

[CC BY 4.0](LICENSE). Cite as: Voting Monitor, votingmonitor.org.
