# FitFindr

> ### 👋 Start here
>
> **New to this repo? Read [RUNNING.md](RUNNING.md) first** — setup, every
> command, and what to do when something breaks.
>
> Once `python test.py` passes:
>
> ```bash
> python app.py listings --full -n 6      # read the data (Milestone 1)
> python app.py fields                    # what you can filter on
> python app.py ask 'vintage graphic tee under $30'
> ```
>
> All three tools are stubs, so that last command will do nothing useful yet.
> That's the starting position.
>
> **The rest of this file is your submission.** Fill it in as you go.

---

<!-- ─────────────────────────────────────────────────────────────────────────
     HOW TO USE THIS FILE

     This is your submission. Fill each section in as you finish the milestone
     it belongs to — don't leave it all to the end.

     Unit 3 asks for the first five sections. Unit 4 adds the five below them.
     Leave the unit 4 sections alone until then; they're here so you know
     what's coming.

     Everything is pasted as TEXT. No screenshots, no images, no video links.
     A typed block of output gets full credit; a picture of the same output
     gets none.
     ───────────────────────────────────────────────────────────────────────── -->

<!-- ═══════════════════════ UNIT 3 — THE BUILD ═══════════════════════ -->

## What This Does

<!-- Three or four sentences: what a user asks for, and what they get back. -->
FitFindr helps users find clothing in the provided listings data using a clothing description, an optional size, and an optional budget. It selects the highest-ranked match and suggests outfits combining that item with the user's wardrobe. It then generates a short social media caption mentioning the item, price, platform, and outfit style. When no listings match, it stops and suggests changing the clothing keywords, size, or budget; when the wardrobe is empty, it provides general styling advice.



---

## Tool Inventory
     
<!-- Four lines per tool. This is worth 2 points and it's the single most
     common place students lose them.

     "Returns a list" earns NOTHING. The description has to say what is IN
     the list.

     The empty case isn't optional either — it's the thing your loop branches
     on, and if you don't decide it here you'll discover it as a crash in
     Milestone 5. -->

### `search_listings`

- **What it does:** This will search the provided clothing lines using clothing keywords which will also include sizes, and the maximum price. 
- **Inputs:** description(str) will contain clothing keywords. Size(str or none) will focus on the requested size the user gives. Max_price will set an inclusive price ceilinig.<!-- name and type each: `max_price` (float), not "a price" -->
- **Returns:** A list[dict] of matching listing that the user has requested. Each dictionary contains id, title, description, category, style_tags, size, condition, price, colors, brand, and platform. Listing with no keywords overlap are excluded.
- **When it has nothing:**  It will return an empty list [] , when no listings are match

### `suggest_outfit`

- **What it does:** This will suggest one or two outfits based on the users wardrobes.
- **Inputs:** new_item(dict) is the selected listing dictionary. wardrobe(dict) contains an items listing of wardrobe dicitionaries which will describe clothing the user owns. 
- **Returns:** a non-empty str describing one or two outfit suggestions which will include the selected items from the users wardrobe.
- **When it has nothing:** If it's empty it will just give advice on items that go well together to make an outfit. It will suggest any clothing item since it will not know what is in the wardrobe.

### `create_fit_card`

- **What it does:** Uses the model to turn the outfit suggestion into a short caption which can be used for social media.
- **Inputs:** outfit (str) is the outfit suggestion returned by suggest_outfit. new_item (dict) is the selected listing dictionary
- **Returns:** A str containing a two-to-four-sentence caption that mentions the selected item, its price, and its platform once each, and it will describes the outfit’s style.
- **When it has nothing:** if outfit is empty then it will return a message that will explain that an outfit suggestion is needed in order to make a fit card.

---

## Planning Loop

<!-- Your branch rule, stated as a rule — the condition AND both paths — plus
     the file and function that holds it.

     Like this:
       "If search_listings returns an empty list, put a message in the session
        and stop. Otherwise take the first result and go to suggest_outfit."
        — agent.py::run_agent

     The grader checks your code against what you claim here, so the file and
     function have to be real. -->

**Branch rule:** If search_listings returns an empty list then a message will be stored that will give suggestions on changing clothing keywords, size , or budget and stop without calling the other tools. Otherwise select the first result and then save it in the session  and then continue onto suggest_outfit and then create_fit_card. 

**Where it lives:** `agent.py::run_agent`

**How the query is parsed:** <!-- regex, string splitting, or asking the model — say which -->

**What moves through the session:** <!-- which fields, in what order -->

---

## Sample Run

<!-- Two things go here.

     1. One FULL query and its output, pasted as text.
     2. Your three per-tool terminal tests — the command and what it printed. -->

**One full query**

```
$ python app.py ask '...'

```

**The three tools, tested one at a time**

```
$ python -c "from tools import search_listings; print(search_listings('graphic tee', size='M', max_price=30))"
.

[{'id': 'lst_002', 'title': 'Y2K Baby Tee — Butterfly Print', 'description': 'Super cute early 2000s baby tee with butterfly graphic. Fitted crop length. Tag says medium but fits like a small.', 'category': 'tops', 'style_tags': ['y2k', 'vintage', 'graphic tee', 'cottagecore'], 'size': 'S/M', 'condition': 'excellent', 'price': 18.0, 'colors': ['white', 'pink', 'purple'], 'brand': None, 'platform': 'depop'}, {'id': 'lst_017', 'title': 'Mesh Long-Sleeve Top — Black', 'description': 'Sheer black mesh long-sleeve. Great for layering under a graphic tee or over a bralette. Stretchy material, fits true to size.', 'category': 'tops', 'style_tags': ['y2k', 'grunge', 'goth', 'layering'], 'size': 'S/M', 'condition': 'excellent', 'price': 15.0, 'colors': ['black'], 'brand': None, 'platform': 'depop'}]


```

```
$ python -c "from tools import suggest_outfit; from utils.data_loader import get_example_wardrobe, load_listings; print(suggest_outfit(load_listings()[0], get_example_wardrobe()))"

Here are two outfits featuring the Vintage Levi's 501 Jeans:

**Outfit 1: Casual & Clean**
*   **Selected Item:** Vintage Levi's 501 Jeans — Medium Wash
*   **Wardrobe Pieces:** White ribbed tank top, Chunky white sneakers, Black crossbody bag
*   **Why it works:** This is a timeless, effortless combination. The fitted white tank balances the straight-leg fit of the 501s, while the chunky sneakers and crossbody bag keep the look modern and streetwear-inspired.

**Outfit 2: Cozy Layered Streetwear**
*   **Selected Item:** Vintage Levi's 501 Jeans — Medium Wash
*   **Wardrobe Pieces:** Oversized grey crewneck sweatshirt, Black combat boots, Brown leather belt, Black crossbody bag
*   **Why it works:** Pairing the relaxed 501s with an oversized crewneck creates a comfortable, slouchy silhouette. The brown belt adds a nice contrast at the waist, and the combat boots give the vintage denim an edgy, grounded finish.

```

```
$ AI201_CACHE=0 python - <<'PY'
from tools import create_fit_card
from utils.data_loader import load_listings

item = load_listings()[0]
outfit = "Pair the selected jeans with a white ribbed tank top and chunky white sneakers."

for attempt in range(1, 4):
    print(f"\nRun {attempt}:")
    print(create_fit_card(outfit, item))
PY

Run 1:
Style these vintage Levi's 501 jeans with a simple white ribbed tank top and chunky white sneakers for an effortless streetwear look. Find this classic medium wash denim listed on depop for $38.00.

Run 2:
Embrace a classic streetwear look by styling these vintage Levi's 501 jeans with a simple white ribbed tank top and chunky white sneakers. You can find this medium wash denim for $38.0 on Depop.

Run 3:
Embrace effortless streetwear styling by pairing these classic blue vintage Levi's 501 Jeans with a simple white ribbed tank top and chunky sneakers. Find them on Depop for $38.00 to complete your casual denim look.
```

---

## How I Used AI
 I used AI to help implement the three tools and help connecting the tools. It provided Python implementations for keyword-ranked search, wardrobe-aware outfit suggestions, and caption generation with an empty-outfit guard. Some things that I did change was replacing the three stubs in `tools.py`, added the `re` and `json` imports, and ran the supplied terminal tests. I checked matching and empty search results, both wardrobe cases, and three uncached captions. When the caption tests initially printed blank output, I used its inspection command to check the function Python was loading, saved the updated file, and reran the tests successfully.


<!-- Two specific moments. What you asked, what came back, what you changed.

     "I used Claude to help me code" is not enough.

     "I gave Claude my search_listings spec. It returned None on no match
     instead of an empty list, so I changed it" is the level we want. -->

**Moment 1**

- *What I asked for:*
- *What came back:*
- *What I changed:*

**Moment 2**

- *What I asked for:*
- *What came back:*
- *What I changed:*

<!-- ═══════════════════════ UNIT 4 — THE TEST ═══════════════════════

     Don't fill these in during unit 3.
     ═══════════════════════════════════════════════════════════════════ -->

---

## Run Log — Before

<!-- Five criteria, five tries each, in this exact format.

     Five, because your criteria are written out of five. Mark each try PASS
     or FAIL, count the passes, and read that count against your target — a
     row targeting 4 of 5 with three PASS cells is MISSED (3/5).

     `python run_eval.py --label before` runs everything and writes the table
     into results/. Paste it here and fill in the verdicts. -->

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Real output from one try**, pasted as text, naming the file and function
that produced it:

```

```

---

## Verdicts and Diagnoses

<!-- MET or MISSED per criterion against LAST UNIT's target, plus a sentence on
     how you decided.

     Then, for every miss: which of the four places it happened — a tool, the
     loop's branch, the session, or the model's output — AND the mechanism.

     Not a diagnosis:  "The fit card was bad."
     A diagnosis:      "The fit card criterion missed on 2 of 5 items. Both had
                        an empty brand field. My prompt puts the brand in the
                        first sentence, so the card opened with a blank and read
                        like a fragment. The tool worked; the prompt assumed a
                        field that isn't always there."

     Look for a pattern. Three misses on the same tool is one problem, not
     three. -->

| # | Criterion | Target | Verdict | How I decided |
|---|---|---|---|---|
| 1 |  |  |  |  |
| 2 |  |  |  |  |
| 3 |  |  |  |  |
| 4 |  |  |  |  |
| 5 |  |  |  |  |

**Diagnoses**



---

## Loop Trace

<!-- One full run, printed step by step, with the MCP call visible in it.

     `python app.py ask '...' --trace` once you've added the trace.step()
     calls in Milestone 2.

     Worth pasting BOTH the happy path and the empty-search path. The empty
     one should be visibly shorter, because it stops. If your two traces are
     the same length, your branch isn't working — and this is the fastest way
     anyone will ever find that out. -->

**Happy path**

```

```

**Empty search**

```

```

**On the MCP move:** <!-- what changed in your code, and whether anything
behaved differently afterwards. If the rewire didn't work, say exactly where it
broke — the error text and the last thing that worked. That earns the point in
full. -->



---

## The Improvement

<!-- What you changed, why your diagnosis pointed at it, and the after-run in
     the same table format. One change, measured properly.

     `python run_eval.py --label after` -->

**What I changed:**

**Which failure it was meant to fix:**

### Run Log — After

| Criterion | Target | Try 1 | Try 2 | Try 3 | Try 4 | Try 5 | Verdict |
|---|---|---|---|---|---|---|---|
| 1.  |  |  |  |  |  |  |  |
| 2.  |  |  |  |  |  |  |  |
| 3.  |  |  |  |  |  |  |  |
| 4.  |  |  |  |  |  |  |  |
| 5.  |  |  |  |  |  |  |  |

**Did it help, and how do I know:**

<!-- If it made things worse, say that. Honestly reported, that earns full
     credit and is more interesting than one that worked. -->



---

## What's Still Broken

<!-- For each criterion still missed: what you'd do, and why you stopped where
     you did. "I ran out of time" is fine if it's true. Pretending nothing is
     left is not. -->



<!-- ═════════════════════════════════════════════════════════════════════

     SUBMISSION CHECKLIST — unit 3

       [ ] criteria.md has five numbered criteria, each with a target
       [ ] Each criterion has a reason underneath it
       [ ] All five unit 3 sections above have real content
       [ ] Tool Inventory: all three tools, inputs WITH TYPES, a specific
           return value, and the empty case
       [ ] Planning Loop names the branch rule and agent.py::run_agent
       [ ] Sample Run: one full query plus the three per-tool tests, as text
       [ ] At least four new commits
       [ ] Repository URL submitted — WRITE IT DOWN, you submit the same one
           next unit

     SUBMISSION CHECKLIST — unit 4

       [ ] mcp_server.py exists with one tool registered
           (or a written record of exactly where the rewire broke)
       [ ] Run Log — Before, five criteria, five tries each
       [ ] Real output pasted underneath, naming file and function
       [ ] A verdict on every criterion
       [ ] A diagnosis for every miss, naming a place AND a mechanism
       [ ] Loop Trace, with the MCP call visible in it
       [ ] All three failure modes triggered and handled
       [ ] One improvement, with Run Log — After in the same format
       [ ] What's Still Broken
       [ ] At least four new commits
       [ ] The SAME repository URL as last unit

     Do not delete and recreate this repository. Your commit history is what
     shows your criteria existed before your results did.
     ═════════════════════════════════════════════════════════════════════ -->

---

📖 **How to run this project: [RUNNING.md](RUNNING.md)**
