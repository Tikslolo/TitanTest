#!/usr/bin/env python3
"""Checkpoint game prototype inspired by Papers, Please in an apocalypse setting."""

from __future__ import annotations

import random
from dataclasses import dataclass


NAMES = [
    "Mara", "Ilya", "Noor", "Jax", "Pavel", "Sera", "Bram", "Kade", "Lina", "Oren",
]

REQUESTS = ["shelter", "supply trade", "medical aid", "family reunification"]


@dataclass
class Entrant:
    name: str
    request: str
    bitten: bool
    fake_identity: bool

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

    def generate_entrant(self) -> Entrant:
        name = self.random.choice(NAMES)
        request = self.random.choice(REQUESTS)
        bitten = self.random.random() < 0.22
        fake_identity = self.random.random() < 0.20

        # Keep some entrants clean so decisions are mixed.
        if bitten and fake_identity and self.random.random() < 0.5:
            fake_identity = False

        return Entrant(name=name, request=request, bitten=bitten, fake_identity=fake_identity)

    def get_clues(self, entrant: Entrant) -> list[str]:
        clues = [f"- Request reason: {entrant.request}"]

        if entrant.bitten:
            clues.append("- Their sleeve is torn and there is a fresh bandage with blood spots.")
        else:
            clues.append("- They keep distance from infected checkpoints and know quarantine protocol.")

        if entrant.fake_identity:
            clues.append("- Their ID photo looks new, but the card edges are heavily worn.")
        else:
            clues.append("- ID serial and ration ledger entry match correctly.")

        # Add occasional noise clue to preserve uncertainty.
        if self.random.random() < 0.4:
            clues.append("- Nervous behavior: avoids eye contact and fidgets constantly.")

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
            reason = "You let in a bitten survivor. Medical wing is now in lockdown."
        elif entrant.fake_identity and allowed:
            reason = "You let in an impostor. Supplies went missing overnight."
        elif denied:
            reason = "You denied a legitimate survivor. Morale in the base dropped."
        else:
            reason = "Bad call at the gate."
        return False, reason

    def run(self) -> None:
        print("\n=== Last Light Gatekeeper ===")
        print("Apocalypse checkpoint duty: ALLOW (a) or DENY (d) each entrant.\n")

        for day in range(1, self.days + 1):
            print(f"\n--- Day {day} ---")

            for idx in range(1, self.entrants_per_day + 1):
                entrant = self.generate_entrant()
                print(f"\nEntrant {idx}: {entrant.name}")
                for clue in self.get_clues(entrant):
                    print(clue)

                decision = input("Decision [a/d]: ")
                correct, message = self.judge(entrant, decision)
                result = "PASS" if correct else "FAIL"
                print(f"{result}: {message}")

                if self.strikes >= 5:
                    print("\nToo many mistakes. You are removed from gate duty.")
                    self.end_game(early=True)
                    return

        self.end_game(early=False)

    def end_game(self, early: bool) -> None:
        total = self.days * self.entrants_per_day
        reviewed = self.score + self.strikes
        print("\n=== Shift Report ===")
        print(f"Correct decisions: {self.score}")
        print(f"Mistakes/strikes: {self.strikes}")
        print(f"Reviewed: {reviewed}/{total}")

        if early:
            print("Outcome: Suspended. The base needs steadier hands.")
        elif self.score >= int(total * 0.8):
            print("Outcome: Promoted to Senior Gatekeeper.")
        elif self.score >= int(total * 0.6):
            print("Outcome: Adequate. You keep your post.")
        else:
            print("Outcome: Barely survived the shift. Retraining required.")


if __name__ == "__main__":
    Game().run()
