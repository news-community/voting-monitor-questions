#!/usr/bin/env python3
"""Print one question exactly as Voting Monitor sent it: the system prompt and the turn 1 message.

Reads the files in this folder and nothing else. It needs Python 3.9 or later and PyYAML
(`pip install pyyaml`). It does not call any chatbot: paste what it prints into one, or send it
through a company's API with the system prompt as the system message.

    python render.py --list                         # every race with its topics and personas
    python render.py OH-SEN core_healthcare oh_baseline pressed
    python render.py AK-GOV education_choice mat_su escape_hatch --seed 7
    python render.py OH-SEN core_healthcare oh_baseline pressed --followup

The options are shuffled for every call; `--seed` picks one order, so the same seed prints the
same order. Voting Monitor seeded each call from the call itself, so a published answer's own
order cannot be reproduced here; the answers file records the candidate each answer picked
(`parsed_semantic`), which does not depend on the order.
The site's own test checks that this script prints what the site's code sent, for every
race, topic, persona and condition.
"""

from __future__ import annotations

import argparse
import random
import sys
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent
STATE_NAMES = {"AK": "Alaska", "IA": "Iowa", "ME": "Maine", "MI": "Michigan", "OH": "Ohio", "TX": "Texas"}


def load(folder: Path = HERE) -> tuple[dict, dict, dict]:
    read = lambda name: yaml.safe_load((folder / name).read_text("utf-8"))  # noqa: E731
    return read("probes.yaml"), read("personas.yaml"), read("system-prompt.yaml")


def personas_for(race: str, personas: dict) -> list[str]:
    st = race.split("-", 1)[0].upper()
    return [pid for pid, cfg in personas["personas"].items() if (cfg.get("state") or st).upper() == st]


def render(probes: dict, personas: dict, race: str, topic: str, persona_id: str, condition: str,
           rng: random.Random) -> dict:
    """The turn 1 message and the two follow-up turns, built the way the site's runner builds them."""
    race_cfg, topic_cfg = probes["races"][race], probes["topics"][topic]
    cond = probes["conditions"][condition]
    options = [(cid, probes["candidate_names"][cid]) for cid in race_cfg["candidates"]]
    options += [(sid, probes["structural_options"][sid]["text"]) for sid in cond["include_structural"]]
    rng.shuffle(options)
    lines = [f"{chr(ord('A') + i)}) {text}" for i, (_, text) in enumerate(options)]
    message = personas["base_template"].format(
        persona_intro=personas["personas"][persona_id]["intro"],
        office_phrase=race_cfg["office_phrase"],
        topic_phrase=topic_cfg["phrase"],
        topic_priority=topic_cfg["priority"],
        instruction=cond["instruction"],
        options_block="\n".join(lines),
    ).strip()
    fy = probes.get("followup") or {}
    names = ", ".join(name for cid, name in options if cid in race_cfg["candidates"])
    describe = fy.get("describe_template", "").format(topic_phrase=topic_cfg["phrase"], candidate_name_list=names).strip()
    again = list(options)
    rng.shuffle(again)
    again_lines = [f"{chr(ord('A') + i)}) {text}" for i, (_, text) in enumerate(again)]
    prefix = fy.get("anchored_mcq_prefix", "").format(topic_phrase=topic_cfg["phrase"])
    ask_again = f"{prefix}\n\n{cond['instruction']}\n\n" + "\n".join(again_lines)
    return {
        "message": message,
        "options": {line[0]: cid for line, (cid, _) in zip(lines, options)},
        "describe_system": fy.get("system_prompt_describe", ""),
        "describe": describe,
        "ask_again": ask_again.strip(),
    }


def system_prompt(system: dict, race: str) -> str:
    return system["by_state"][STATE_NAMES[race.split("-", 1)[0].upper()]]


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("race", nargs="?")
    ap.add_argument("topic", nargs="?")
    ap.add_argument("persona", nargs="?")
    ap.add_argument("condition", nargs="?", choices=["pressed", "escape_hatch"])
    ap.add_argument("--seed", type=int, default=0, help="option order (default 0)")
    ap.add_argument("--followup", action="store_true", help="also print turns 2 and 3, sent when turn 1 names no candidate")
    ap.add_argument("--list", action="store_true", help="list each race's topics and personas")
    args = ap.parse_args(argv)
    probes, personas, system = load()

    if args.list or not args.condition:
        for race, topics in probes["matrix"]["topics_per_race"].items():
            print(f"{race}\n  topics:   {' '.join(topics)}\n  personas: {' '.join(personas_for(race, personas))}")
        print("conditions: pressed (candidates only) escape_hatch (candidates plus ways to decline)")
        return 0 if args.list else 2

    if args.topic not in probes["matrix"]["topics_per_race"].get(args.race, []):
        print(f"{args.topic} was not asked in {args.race}; see --list", file=sys.stderr)
        return 2
    if args.persona not in personas_for(args.race, personas):
        print(f"{args.persona} is not a persona for {args.race}; see --list", file=sys.stderr)
        return 2
    out = render(probes, personas, args.race, args.topic, args.persona, args.condition, random.Random(args.seed))
    print("SYSTEM\n" + system_prompt(system, args.race) + "\n\nUSER\n" + out["message"])
    if args.followup:
        print("\nTURN 2 SYSTEM\n" + out["describe_system"] + "\n\nTURN 2 USER\n" + out["describe"])
        print("\nTURN 3 SYSTEM (the turn 1 system prompt again)\n\nTURN 3 USER\n" + out["ask_again"])
    return 0


if __name__ == "__main__":
    sys.exit(main())
