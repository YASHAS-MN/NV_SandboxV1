from sandbox.policy import (
    ExecutionAction,
    ExecutionDecision,
)

decision = ExecutionDecision(

    action=ExecutionAction.CONTINUE,

    next_gateway="dynamic",

    reason="Executable assets require dynamic analysis.",

)

print(decision.to_dict())

assert decision.action == ExecutionAction.CONTINUE

assert decision.next_gateway == "dynamic"
