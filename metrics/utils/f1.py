from collections import Counter
from re import findall


def tp_fp_fn(reference: str, text: str) -> tuple[int, int, int]:
    ref = Counter(_extract_prices(reference))
    rec = Counter(_extract_prices(text))

    tp = sum((ref & rec).values())
    fp = sum(rec.values()) - tp
    fn = sum(ref.values()) - tp
    return tp, fp, fn


def f1(tp: int, fp: int, fn: int) -> float:
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return 2 * p * r / (p + r) if p + r else 0.0


def _extract_prices(text: str) -> list[str]:
    return [price.replace(",", ".") for price in findall(r"\d+[.,]\d+", text)]
