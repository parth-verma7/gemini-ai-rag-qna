from guardrails.hub import ToxicLanguage, DetectPII
from guardrails import Guard

guard = Guard().use_many(
    ToxicLanguage(threshold=0.5, validation_method="sentence", on_fail="exception"),
    DetectPII(pii_entities=["EMAIL_ADDRESS", "PHONE_NUMBER"], on_fail="exception")
)

def guardrail_check(user_input) -> list:
    try:
        guard.validate(user_input)
        return ["positive"]
    except Exception as e:
        return ["negative", str(e)]

