from typing import Tuple


class DiagnosisAgent:
    """
    Simple rule-based diagnosis agent for now (if-else).
    Later, you can plug in an API/LLM here.
    """

    def predict(
        self,
        symptoms: str,
        age: int,
        gender: str,
        height: float,
        weight: float,
    ) -> Tuple[str, str]:
        text = (symptoms or "").lower()

        # Very simple heuristics – you can extend this
        if "fever" in text and "cough" in text:
            return ("Possible viral infection (e.g., flu)", "medium")
        if "chest pain" in text or "breathless" in text:
            return ("Possible cardiac/respiratory issue – urgent check", "high")
        if "headache" in text and "stress" in text:
            return ("Possible tension headache / stress-related issue", "low")
        if "stomach" in text or "abdomen" in text:
            return ("Possible gastric/abdominal issue", "medium")

        return ("General check-up recommended, no clear pattern detected", "low")
