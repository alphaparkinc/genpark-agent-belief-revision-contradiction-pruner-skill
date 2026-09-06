"""
Example usage of Agent Belief Revision Contradiction Pruner Skill.
"""

from client import BeliefRevisionEngine


def main():
    print("=== Agent Belief Revision Contradiction Pruner Demonstration ===")
    engine = BeliefRevisionEngine()

    # 1. Initial observation (Expansion)
    print("\n1. Expansion: Initial observations")
    res1 = engine.assert_belief("user_language", "Python", entrenchment=2.0, source="user_profile")
    res2 = engine.assert_belief("deployment_target", "AWS", entrenchment=1.5, source="docs")
    print("  assert user_language=Python ->", res1["action"])
    print("  assert deployment_target=AWS ->", res2["action"])

    # 2. Contradictory weak rumor (Attempted revision with lower entrenchment)
    print("\n2. Attempted weak contradictory evidence")
    res3 = engine.assert_belief("user_language", "Go", entrenchment=1.0, source="unverified_comment")
    print("  assert user_language=Go (entrenchment=1.0) ->", res3["action"])

    # 3. Direct explicit user instruction (Strong revision with high entrenchment)
    print("\n3. Strong explicit contradictory evidence")
    res4 = engine.assert_belief("user_language", "Rust", entrenchment=5.0, source="explicit_user_directive")
    print("  assert user_language=Rust (entrenchment=5.0) ->", res4["action"])
    print("  Retracted:", res4["retracted_belief"]["value"], "-> Accepted:", res4["accepted_belief"]["value"])

    # Current consistent world state
    print("\nCurrent Consistent World State:")
    print(" ", engine.get_world_state())


if __name__ == "__main__":
    main()
