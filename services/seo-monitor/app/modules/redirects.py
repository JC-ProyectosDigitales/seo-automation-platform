from typing import Any, Dict, List


def analyze_redirects(
    redirect_count: int,
    redirect_history: List[Dict[str, Any]],
    requested_url: str,
    final_url: str | None,
) -> Dict[str, Any]:
    has_redirects = redirect_count > 0

    excessive = redirect_count > 2

    return {
        "has_redirects": has_redirects,
        "count": redirect_count,
        "excessive": excessive,
        "recommended_max": 2,
        "requested_url": requested_url,
        "final_url": final_url,
        "history": redirect_history,
    }
