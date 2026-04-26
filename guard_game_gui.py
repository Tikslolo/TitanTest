#!/usr/bin/env python3
"""Tkinter interface for Last Light Gatekeeper."""

from __future__ import annotations

import tkinter as tk

from guard_game import Game


class GatekeeperUI:
    def __init__(self, root: tk.Tk) -> None:
        self.root = root
        self.root.title("Last Light Gatekeeper")
        self.root.geometry("700x520")
        self.game = Game(days=3, entrants_per_day=5)
        self.current = None

        self.title = tk.Label(root, text="Last Light Gatekeeper", font=("Helvetica", 20, "bold"))
        self.title.pack(pady=12)

        self.status = tk.Label(root, text="Inspect each person. Allow or deny access.", font=("Helvetica", 11))
        self.status.pack(pady=(0, 8))

        self.person = tk.Label(root, text="", font=("Helvetica", 34))
        self.person.pack(pady=4)

        self.identity = tk.Label(root, text="", font=("Helvetica", 13, "bold"))
        self.identity.pack(pady=4)

        self.clues = tk.Text(root, height=11, width=78, state="disabled", wrap="word")
        self.clues.pack(padx=16, pady=10)

        button_frame = tk.Frame(root)
        button_frame.pack(pady=10)

        self.allow_btn = tk.Button(button_frame, text="ALLOW", width=16, bg="#2f9e44", fg="white", command=self.allow)
        self.allow_btn.grid(row=0, column=0, padx=8)

        self.deny_btn = tk.Button(button_frame, text="DENY", width=16, bg="#c92a2a", fg="white", command=self.deny)
        self.deny_btn.grid(row=0, column=1, padx=8)

        self.report = tk.Label(root, text="", font=("Helvetica", 11))
        self.report.pack(pady=8)

        self.next_case()

    def next_case(self) -> None:
        if not self.game.has_more_cases():
            self.finish_game()
            return

        self.current = self.game.generate_entrant()
        self.person.config(text=self.current.visual)
        self.identity.config(text=f"{self.current.name}, age {self.current.age} — {self.current.occupation}")

        clue_lines = [f"• {line}" for line in self.game.get_clues(self.current)]
        self.clues.config(state="normal")
        self.clues.delete("1.0", tk.END)
        self.clues.insert(tk.END, "\n".join(clue_lines))
        self.clues.config(state="disabled")

        self.report.config(
            text=f"Score: {self.game.score} | Strikes: {self.game.strikes} | Reviewed: {self.game.processed_cases()}/{self.game.total_cases()}"
        )

    def resolve(self, decision: str) -> None:
        if self.current is None:
            return

        ok, message = self.game.judge(self.current, decision)
        prefix = "PASS" if ok else "FAIL"
        self.status.config(text=f"{prefix}: {message}")
        self.next_case()

    def allow(self) -> None:
        self.resolve("allow")

    def deny(self) -> None:
        self.resolve("deny")

    def finish_game(self) -> None:
        self.allow_btn.config(state="disabled")
        self.deny_btn.config(state="disabled")
        self.person.config(text="🛡️")
        self.identity.config(text="Shift complete")
        self.clues.config(state="normal")
        self.clues.delete("1.0", tk.END)
        self.clues.insert(
            tk.END,
            f"Final Score: {self.game.score}\n"
            f"Strikes: {self.game.strikes}\n"
            f"Reviewed: {self.game.processed_cases()}/{self.game.total_cases()}\n\n"
            f"Outcome: {self.game.outcome_text()}"
        )
        self.clues.config(state="disabled")
        self.status.config(text="Session ended.")


def main() -> None:
    root = tk.Tk()
    GatekeeperUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
