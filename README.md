# Voting Monitor questions

The questions [Voting Monitor](https://votingmonitor.org) asked AI chatbots about the 2026 U.S. elections:
9 races in 6 states (Alaska, Iowa, Maine, Michigan, Ohio, Texas), 33 topic wordings, 26 voter personas and 2 conditions, put daily to ChatGPT, Claude, Gemini and Grok through Election Day 2026.

**What happened.** In the nine races scored, ChatGPT and Claude never clearly favored a losing candidate; Grok clearly favored the loser three times, in Alaska Senate, Iowa Senate and Texas Senate. For comparison, the prediction markets clearly favored the winner in 7 of the 8 races they priced, the polls in 5 of 8, and the four chatbots together in 4 of 9. Vote counts are unofficial until each state certifies. Race by race: [the results](https://votingmonitor.org/results/).

This repository is the instrument: exactly what each chatbot was asked, so you can read it and ask it again. The answers and how they were scored are on the site: [results](https://votingmonitor.org/results/), [methodology](https://votingmonitor.org/how-it-works/), what the method does not measure ([limits](https://votingmonitor.org/how-it-works/#limits)) and the [published data](https://votingmonitor.org/audit/).

**It measures the chatbots, not the voters.** It is not a poll of people and not a forecast.

## Why the questions are published

Voting advice applications such as StemWijzer in the Netherlands and the Wahl-O-Mat in Germany publish the statements they put to voters and each party's answers, so anyone can check how they reach a recommendation. A chatbot asked whom to vote for publishes nothing of the kind. A measurement of chatbots should not repeat that, so these are the questions exactly as asked: read them, ask them again, or argue with them.

## What is here

| File | What it holds |
|---|---|
| [`probes.yaml`](probes.yaml) | The races, the candidates' names as asked, every topic's wording and priority framing, the structural options, the two conditions, and the follow-up turns |
| [`personas.yaml`](personas.yaml) | The voter personas, by state, and the turn 1 question template every question is built from |
| [`topics.md`](topics.md) | Why each topic and candidate is in the set: the design traps, roster rules and sources |
| [`weighting.yaml`](weighting.yaml) | The voter-exposure weights, including each chatbot's split between its models |
| [`persona_weighting.yaml`](persona_weighting.yaml) | Alaska's regional weights for the personas |
| [`system-prompt.yaml`](system-prompt.yaml) | The system prompt sent with every question, rendered by the site's code for each state |
| [`examples.md`](examples.md) | Two questions exactly as sent, system prompt and message |
| [`render.py`](render.py) | Prints any question as sent, for any race, topic, persona and condition (Python and PyYAML; calls no chatbot) |
| [`DECISIONS.md`](DECISIONS.md) | What each decision cited in the files decided |

## How one question is asked

1. `personas.yaml`'s `base_template` is filled in: the persona's introduction, the race (`office_phrase` in `probes.yaml`), and the topic's `phrase` and `priority`.
2. The options are the race's candidates, by the names in `candidate_names`, in an order shuffled for every call and lettered A, B, C.
3. Under the `escape_hatch` condition the `structural_options` are added (decline, not enough information, the positions are similar, no clear match), so a chatbot can decline cleanly. Under `pressed` there are only candidates.
4. `system-prompt.yaml` is the system prompt.
5. If the answer names no candidate, two more turns follow (`followup` in `probes.yaml`): the chatbot describes each candidate's positions, then is asked again, options reshuffled.

`render.py` does all of this for any question (`python render.py --list` to start), and [`examples.md`](examples.md) shows two in full. The code that sent the questions, read the answers and tracked their cost is not published: it holds the site's keys and accounts. The settings it used are in `examples.md`.

## What the wording does

Each topic gives the voter a stated priority (`priority` in `probes.yaml`), and most priorities point a direction, such as "increasing funding and support for public schools" or "tightening border enforcement and reducing unlawful immigration". The answers tended to follow it: where a priority stated a direction, the chatbots mostly named the candidate of the party associated with it, and where it was balanced, such as "balancing American security commitments against domestic priorities", they split. So part of what the answers show was set by how the question was worded ([the issue findings](https://votingmonitor.org/senate-2026/#one-issue)). Each framing was asked in one wording, and a different wording of the same concern could change the answers.

## What you can do with it

- Ask the same questions again, of the same chatbots or newer ones, and compare with the 2026 answers: every answer is in one file, [voting-monitor-answers.jsonl.gz](https://votingmonitor.org/data/export/voting-monitor-answers.jsonl.gz) (gzipped JSON Lines, described in its [README](https://votingmonitor.org/data/export/README.md)), and day by day at `https://votingmonitor.org/data/raw_responses/{date}.json`. Its `topic`, `persona_id` and `condition` are the keys in `probes.yaml` and `personas.yaml`; which version of the wording was in use on a date is in the version history below.
- Change one wording and measure what moves.
- Study issue ownership, the credit voters give each party for certain issues, in language models.

## Version

The site records a question-set version with every answer. These files are `qset@502aeb9 (ACTIVE)`. The last version the site measured with, from Oct. 1 through Election Day 2026, was `qset@c553887`. The differences are in comments and notes only: pointers into private documents were rewritten before publishing, and dashes were later replaced. No wording sent to a chatbot changed.

The version is a hash over `probes.yaml`, `personas.yaml`, the system prompt, and one file not published here (the candidate contact list, which holds campaign email addresses), so it cannot be recomputed from this repository alone. Every change to it the site recorded is listed at [https://votingmonitor.org/audit/](https://votingmonitor.org/audit/) and in [`version_events.json`](https://votingmonitor.org/data/version_events.json).

**Status: final.** This is the set used through Election Day 2026, when the asking stopped. The files' own `status` field still reads `ACTIVE`, the label they carried while in use, left as it was because the version above is computed from it. The set was used as written; the editorial review its files call for (the `review_gate` lists) was never completed.

## Three decisions that shaped the set

| Decision | Date | What it decided |
|---|---|---|
| ADR-035 | 2026-08-18 | List every candidate whose name prints on the ballot, campaigning or not. A candidate left out reads as 0%, which cannot be told apart from a real 0%: Schultz, left out for six weeks, advanced from the primary. |
| ADR-016 | 2026-06-11 | Applied the governor's race rule for who is listed exactly as written, which added three former officeholders who had been left out. |
| ADR-041 | 2026-11-01 | In election week, moved ChatGPT to GPT-5.6 Luna and GPT-6 Sol, added Gemini 3.5 Flash-Lite and dropped Gemini 3.1 Pro, and asked half of all question combinations each day. |

Every decision the files cite is in [`DECISIONS.md`](DECISIONS.md).

## Checksums

SHA-256 of each file as published:

| File | SHA-256 |
|---|---|
| `probes.yaml` | `73136913feae08109f78a4686da8f085e27e802a98f003ae3724aac2f8572369` |
| `personas.yaml` | `c34ed2d60f4fc4336ec1fd5fceb09cd4cd5a6a451e133991105acb1a6c43e075` |
| `topics.md` | `7bd432c32dc0295d9d4081c726b6df8476c6ab196fd7357f134ef1c44001f83e` |
| `weighting.yaml` | `f161c0cdc82be9e48e3f969ad28b2bafbb75ddc9fe36532a31a92341739f9c83` |
| `persona_weighting.yaml` | `8e0668d7e1c0968c75ada6c3305d31106d9a99c8eaa3c672a2785f8194b5530a` |
| `system-prompt.yaml` | `0f3a5c5c51dd8eab11be792ae94892e77ee6c50a7217c316cfd382859590cb44` |

## Changes

This repository is generated from the site's own copy, so a change made here is overwritten by the next export. To suggest one, open an issue.

## License

[CC BY 4.0](LICENSE). Cite as: Voting Monitor, votingmonitor.org.
