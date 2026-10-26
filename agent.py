"""
The FitFindr planning loop.

This is the file that makes FitFindr an agent rather than a script. It decides
which tool to run next based on what the last one returned.

If your loop calls all three tools no matter what comes back, you have a list
of function calls. A loop looks at the last result before it picks the next
step. **That branch is the graded part of this unit.**

Build and test your three tools in `tools.py` first. Then come here.

    python agent.py          runs both example paths below
"""
import re
import config
import trace
from tools import search_listings, suggest_outfit, create_fit_card
from generate import ModelUnavailable


# ── session state ─────────────────────────────────────────────────────────────

def new_session(query: str, wardrobe: dict) -> dict:
    """
    A fresh session for one user interaction.

    The session is the single source of truth for a run. Every tool result goes
    in here, and the next tool reads it back out.

    You could pass values straight from one call to the next. It would work,
    and you would not be able to test it — you can't print a variable you have
    already overwritten. Going through the session is what makes the state
    visible, and unit 4 has you write a criterion about exactly that.

    Add fields if you need them.
    """
    return {
        "query": query,              # what the user typed
        "parsed": {},                # description / size / max_price you pulled out of it
        "search_results": [],        # everything search_listings returned
        "selected_item": None,       # the one you chose — goes into suggest_outfit
        "wardrobe": wardrobe,        # the user's wardrobe
        "outfit_suggestion": None,   # what suggest_outfit returned
        "fit_card": None,            # what create_fit_card returned
        "error": None,               # set when the run ended early
    }


# ── planning loop ─────────────────────────────────────────────────────────────

def run_agent(query: str, wardrobe: dict) -> dict:
    """Parse a query, run the appropriate tools, and return their session."""
    session = new_session(query, wardrobe)

    price_pattern = (
        r"\b(?:under|below|up\s+to|max(?:imum)?(?:\s+price)?)"
        r"\s*\$?\s*(\d+(?:\.\d+)?)\b"
    )
    size_pattern = (
        r"\b(?:in\s+)?size\s+"
        r"(US\s*\d+(?:\.\d+)?|W\d+(?:\s+L\d+)?|"
        r"[23]?X{0,3}[SML](?:/[23]?X{0,3}[SML])?|\d+(?:\.\d+)?)\b"
    )

    price_match = re.search(price_pattern, query, re.IGNORECASE)
    size_match = re.search(size_pattern, query, re.IGNORECASE)

    description = re.sub(
        price_pattern, " ", query, flags=re.IGNORECASE
    )
    description = re.sub(
        size_pattern, " ", description, flags=re.IGNORECASE
    )
    description = re.sub(
        r"\b(?:looking\s+for|find\s+me|please|i\s+want)\b",
        " ",
        description,
        flags=re.IGNORECASE,
    )

    session["parsed"] = {
        "description": " ".join(description.split()).strip(" ,.;:!?"),
        "size": size_match.group(1).upper() if size_match else None,
        "max_price": float(price_match.group(1)) if price_match else None,
    }

    next_step = "search"
    iterations = 0

    while True:
        iterations += 1
        trace.check_iterations(iterations)

        if next_step == "search":
            session["search_results"] = search_listings(
                **session["parsed"]
            )

            if not session["search_results"]:
                session["error"] = (
                    "No matching listings were found. Try broader clothing "
                    "keywords, a different size, or a higher budget."
                )
                return session

            session["selected_item"] = session["search_results"][0]
            next_step = "outfit"

        elif next_step == "outfit":
            session["outfit_suggestion"] = suggest_outfit(
                session["selected_item"],
                session["wardrobe"],
            )
            next_step = "caption"

        elif next_step == "caption":
            session["fit_card"] = create_fit_card(
                session["outfit_suggestion"],
                session["selected_item"],
            )
            return session


# ── running it directly ───────────────────────────────────────────────────────

def _show(session: dict) -> None:
    if session["error"]:
        print(f"  stopped: {session['error']}")
        print(f"  fit_card is {session['fit_card']!r} — it should still be None here")
        return

    item = session["selected_item"] or {}
    print(f"  found:    {item.get('title')} — ${item.get('price')} on {item.get('platform')}")
    print(f"  outfit:   {session['outfit_suggestion']}")
    print(f"  fit card: {session['fit_card']}")


if __name__ == "__main__":
    from utils.data_loader import get_example_wardrobe

    print("=== A query the data can match ===")
    _show(run_agent(
        query="looking for a vintage graphic tee under $30",
        wardrobe=get_example_wardrobe(),
    ))

    print("\n=== A query it can't ===")
    _show(run_agent(
        query="designer ballgown size XXS under $5",
        wardrobe=get_example_wardrobe(),
    ))

    print(
        "\nThe second one should stop before the fit card. If both paths look "
        "the same,\nthe branch isn't doing anything yet."
    )
