"""
Agent Belief Revision Contradiction Pruner Skill Client
Pure Python Standard Library implementation of AGM Belief Revision (Alchourrón-Gärdenfors-Makinson).
Evaluates epistemic entrenchment, detects contradictory facts, and performs minimal contraction
to incorporate new evidence without logical contradiction.
"""

from typing import List, Dict, Any, Optional, Tuple, Set


class BeliefRevisionEngine:
    """
    Belief revision engine managing an agent's internal propositional belief base.
    Each belief has: key, value, entrenchment (importance/evidence weight), timestamp.
    """

    def __init__(self):
        self.beliefs: Dict[str, Dict[str, Any]] = {}
        self.revision_history: List[Dict[str, Any]] = []

    def assert_belief(self, key: str, value: Any, entrenchment: float = 1.0, source: str = "agent") -> Dict[str, Any]:
        """
        Incorporate a belief into the base using AGM revision.
        If a contradictory value already exists for the key, decide whether to revise or reject.
        """
        key = key.strip().lower()
        existing = self.beliefs.get(key)

        if existing is None:
            # Expansion: no contradiction
            entry = {
                "key": key,
                "value": value,
                "entrenchment": float(entrenchment),
                "source": source
            }
            self.beliefs[key] = entry
            return {"action": "EXPANSION", "belief": entry}

        if existing["value"] == value:
            # Reinforcement: increase entrenchment
            existing["entrenchment"] += entrenchment * 0.5
            return {"action": "REINFORCEMENT", "belief": existing}

        # Contradiction detected: existing["value"] != value
        if entrenchment >= existing["entrenchment"]:
            # Revision: new evidence is stronger, contract old belief and expand new
            old_belief = dict(existing)
            entry = {
                "key": key,
                "value": value,
                "entrenchment": float(entrenchment),
                "source": source
            }
            self.beliefs[key] = entry
            record = {
                "action": "REVISION",
                "key": key,
                "retracted_belief": old_belief,
                "accepted_belief": entry
            }
            self.revision_history.append(record)
            return record
        else:
            # Rejection: existing belief has higher epistemic entrenchment
            return {
                "action": "REJECTED_NEW_EVIDENCE",
                "key": key,
                "retained_belief": existing,
                "rejected_value": value,
                "reason": "Existing belief has higher epistemic entrenchment."
            }

    def retract_belief(self, key: str) -> Optional[Dict[str, Any]]:
        """Contraction: explicitly remove a belief from the base."""
        key = key.strip().lower()
        if key in self.beliefs:
            removed = self.beliefs.pop(key)
            self.revision_history.append({"action": "CONTRACTION", "key": key, "retracted_belief": removed})
            return removed
        return None

    def get_world_state(self) -> Dict[str, Any]:
        """Retrieve full consistent set of beliefs."""
        return {k: v["value"] for k, v in self.beliefs.items()}
