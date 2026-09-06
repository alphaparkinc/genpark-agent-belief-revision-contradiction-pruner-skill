"""
MCP Server for Agent Belief Revision Contradiction Pruner Skill.
"""

import json
import sys
from client import BeliefRevisionEngine

ENGINE = BeliefRevisionEngine()


def handle_request(req: dict) -> dict:
    method = req.get("method")
    params = req.get("params", {})

    if method == "tools/list":
        return {
            "tools": [
                {
                    "name": "assert_belief",
                    "description": "Incorporate a propositional belief with epistemic entrenchment",
                    "inputSchema": {
                        "type": "object",
                        "properties": {
                            "key": {"type": "string"},
                            "value": {},
                            "entrenchment": {"type": "number", "default": 1.0},
                            "source": {"type": "string", "default": "agent"}
                        },
                        "required": ["key", "value"]
                    }
                },
                {
                    "name": "get_world_state",
                    "description": "Retrieve currently held consistent world beliefs",
                    "inputSchema": {
                        "type": "object"
                    }
                }
            ]
        }
    elif method == "tools/call":
        tool_name = params.get("name")
        args = params.get("arguments", {})

        if tool_name == "assert_belief":
            res = ENGINE.assert_belief(
                args["key"],
                args["value"],
                args.get("entrenchment", 1.0),
                args.get("source", "agent")
            )
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        elif tool_name == "get_world_state":
            res = ENGINE.get_world_state()
            return {"content": [{"type": "text", "text": json.dumps(res)}]}

        return {"error": f"Unknown tool: {tool_name}"}

    return {"error": f"Unknown method: {method}"}


def main():
    for line in sys.stdin:
        if not line.strip():
            continue
        try:
            req = json.loads(line)
            resp = handle_request(req)
            resp["id"] = req.get("id")
            sys.stdout.write(json.dumps(resp) + "\n")
            sys.stdout.flush()
        except Exception as e:
            sys.stdout.write(json.dumps({"error": str(e)}) + "\n")
            sys.stdout.flush()


if __name__ == "__main__":
    main()
