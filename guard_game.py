#!/usr/bin/env python3
"""Checkpoint game prototype inspired by Papers, Please in an apocalypse setting."""

from __future__ import annotations

import random
from dataclasses import dataclass

NAMES = ["Mara", "Ilya", "Noor", "Jax", "Pavel", "Sera", "Bram", "Kade", "Lina", "Oren"]
REQUESTS = ["shelter", "supply trade", "medical aid", "family reunification"]
OCCUPATIONS = ["Mechanic", "Teacher", "Medic", "Farmer", "Courier", "Engineer", "Cook"]
VISUALS = ["🧍", "🧑", "👩", "👨", "🧑‍🔧", "🧑‍🌾", "🧑‍⚕️", "🧑‍🏫"]


@dataclass
class Entrant:
    name: str
    request: str
    bitten: bool
    fake_identity: bool
    age: int
    occupation: str
    visual: str

    @property
    def should_allow(self) -> bool:
        return not self.bitten and not self.fake_identity


class Game:
    def __init__(self, days: int = 3, entrants_per_day: int = 5, seed: int | None = None) -> None:
        self.days = days
        self.entrants_per_day = entrants_per_day
        self.random = random.Random(seed)
        self.score = 0
        self.strikes = 0
        self.day = 1
        self.entrant_number = 0

    def generate_entrant(self) -> Entrant:
        bitten = self.random.random() < 0.22
        fake_identity = self.random.random() < 0.20
        if bitten and fake_identity and self.random.random() < 0.5:
            fake_identity = False

        return Entrant(
            name=self.random.choice(NAMES),
            request=self.random.choice(REQUESTS),
            bitten=bitten,
            fake_identity=fake_identity,
            age=self.random.randint(18, 68),
            occupation=self.random.choice(OCCUPATIONS),
            visual=self.random.choice(VISUALS),
        )

    def get_clues(self, entrant: Entrant) -> list[str]:
        clues = [
            f"Request reason: {entrant.request}",
            f"Claimed occupation: {entrant.occupation}",
        ]

        if entrant.bitten:
            clues.append("Sleeve torn; fresh bandage has blood spotting.")
        else:
            clues.append("Knows quarantine protocol and keeps safe distance.")

        if entrant.fake_identity:
            clues.append("ID photo print looks new but document edges are worn.")
        else:
            clues.append("ID serial and ration ledger records match.")

        if self.random.random() < 0.4:
            clues.append("Behavioral note: avoids eye contact and fidgets.")

        return clues

    def judge(self, entrant: Entrant, decision: str) -> tuple[bool, str]:
        decision = decision.strip().lower()
        allowed = decision in {"a", "allow"}
        denied = decision in {"d", "deny"}

        if not (allowed or denied):
            self.strikes += 1
            return False, "Invalid order. Hesitation at the gate costs trust."

        correct = (allowed and entrant.should_allow) or (denied and not entrant.should_allow)
        if correct:
            self.score += 1
            return True, "Correct call. The checkpoint remains secure."

        self.strikes += 1
        if entrant.bitten and allowed:
            return False, "You let in a bitten survivor. Medical wing is in lockdown."
        if entrant.fake_identity and allowed:
            return False, "You let in an impostor. Supplies went missing overnight."
        if denied:
            return False, "You denied a legitimate survivor. Morale dropped in the base."
        return False, "Bad call at the gate."

    def total_cases(self) -> int:
        return self.days * self.entrants_per_day

    def processed_cases(self) -> int:
        return self.score + self.strikes

    def has_more_cases(self) -> bool:
        return self.processed_cases() < self.total_cases() and self.strikes < 5

    def outcome_text(self) -> str:
        total = self.total_cases()
        if self.strikes >= 5:
            return "Suspended. The base needs steadier hands."
        if self.score >= int(total * 0.8):
            return "Promoted to Senior Gatekeeper."
        if self.score >= int(total * 0.6):
            return "Adequate performance. You keep your post."
        return "Barely survived the shift. Retraining required."

    def run_cli(self) -> None:
        print("\n=== Last Light Gatekeeper ===")
        print("Apocalypse checkpoint duty: ALLOW (a) or DENY (d).\n")

        while self.has_more_cases():
            if self.entrant_number == 0:
                print(f"\n--- Day {self.day} ---")

            self.entrant_number += 1
            entrant = self.generate_entrant()
            print(f"\nEntrant {self.entrant_number}: {entrant.visual} {entrant.name}, age {entrant.age}")
            for clue in self.get_clues(entrant):
                print(f"- {clue}")

            decision = input("Decision [a/d]: ")
            ok, msg = self.judge(entrant, decision)
            print(("PASS" if ok else "FAIL") + f": {msg}")

            if self.entrant_number >= self.entrants_per_day:
                self.day += 1
                self.entrant_number = 0

        print("\n=== Shift Report ===")
        print(f"Correct decisions: {self.score}")
        print(f"Mistakes/strikes: {self.strikes}")
        print(f"Reviewed: {self.processed_cases()}/{self.total_cases()}")
        print(f"Outcome: {self.outcome_text()}")


if __name__ == "__main__":
    Game().run_cli()
