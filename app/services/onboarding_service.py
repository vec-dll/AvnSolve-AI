from app.core.constants import SUPPORTED_LANGUAGES


ONBOARDING_STEPS = ("language", "grade", "style")


def get_next_step(current_step: str | None) -> str | None:
    if current_step is None:
        return ONBOARDING_STEPS[0]
    try:
        idx = ONBOARDING_STEPS.index(current_step)
        if idx + 1 < len(ONBOARDING_STEPS):
            return ONBOARDING_STEPS[idx + 1]
    except ValueError:
        pass
    return None


def is_onboarding_complete(step: str | None) -> bool:
    if step is None:
        return False
    try:
        return ONBOARDING_STEPS.index(step) >= len(ONBOARDING_STEPS) - 1
    except ValueError:
        return False
