import gradio as gr
import pandas as pd
import re
from typing import Dict, List, Tuple

# ============================================
# RHETORICAL DICTIONARIES
# ============================================

POWER_WORDS = {
    "accountability","administer","administration","appoint","authority",
    "centralize","centralise","command","commissioner","consolidate",
    "control","coordinate","delegate","department","designate","direct",
    "director","dismiss","enforce","executive","fire","govern","governance",
    "head","hierarchy","implement","jurisdiction","manage","mandate",
    "oversight","power","presidential","principal","remove","reorganize",
    "reorganise","require","restructure","secretariat","secretary",
    "subordinate","supervise","terminate","ban","compliance","compel",
    "constrain","constraint","enforcement","forbid","impose","prohibit",
    "prohibition","regulate","regulation","restriction","rule","sanction",
    "allocate","appropriate","budget","defund","funding","grant",
    "privatize","privatise","resource","transfer","dominate","force","strong",
    "lead","influence","master","victory","win","conquer","decide","determine",
    "execute","sovereign","overcome","triumph","crush","defeat","superior","might",
}

THREAT_WORDS = {
    "attack","catastrophe","chaos","collapse","crisis","danger",
    "destabilize","destabilise","devastate","disaster","emergency",
    "existential","exploit","hazard","jeopardize","jeopardise","peril",
    "risk","threat","vulnerability","abuse","corruption","corrupt",
    "illegitimate","infiltrate","manipulation","misconduct","subvert",
    "subversion","undermine","weaponize","weaponise","adversary",
    "authoritarian","communist","enemy","extremist","ideologue",
    "indoctrinate","marxist","radical","socialist","woke","bloated",
    "broken","bureaucratic","dysfunction","dysfunctional","entrenched",
    "failure","incompetent","inefficient","neglect","obstruction",
    "overreach","unaccountable","wasteful","erode","erosion","decline",
    "degradation","deterioration","disintegration","destroy","damage",
    "harm","fear","warning","vulnerable","weak","hostile","invade","loss",
    "break","fail","prevent","block","stop","hazard",
}

MORAL_WORDS = {
    "character","conscience","conviction","dignity","duty","ethic",
    "excellence","faith","honor","honour","integrity","moral","principle",
    "responsibility","righteousness","virtue","worth","worthiness",
    "child","children","community","family","father","household","marriage",
    "mother","parent","parenthood","biblical","blessing","church","creator",
    "divine","doctrine","god","gospel","grace","holy","prayer","providence",
    "religion","religious","sacred","sanctity","spiritual","american",
    "ancestry","citizen","civilization","civilisation","constitutional",
    "culture","founding","freedom","heritage","history","identity","legacy",
    "liberty","nation","national","patriot","patriotism","republic",
    "sovereign","sovereignty","tradition","traditional","value","decay",
    "decency","depravity","degenerate","immoral","indecent","pornography",
    "promiscuity","restore","revival","wholesome","justice","fair","right",
    "wrong","ethical","honest","good","evil","compassion","compassionate",
    "care","kind","selfish","greedy","corrupt","innocent","guilty","sacred",
}

URGENCY_WORDS = {
    "asap","demand","expedite","forthwith","immediate","immediately",
    "imminent","imperative","instantaneous","now","presently","prompt",
    "promptly","quick","rapid","rapidly","soon","swift","swiftly","urgent",
    "urgently","cannot","compel","compulsory","critical","crucial",
    "essential","indispensable","mandatory","must","necessary","necessity",
    "need","nonnegotiable","obligate","obligation","require","requirement",
    "shall","vital","before","deadline","delay","expire","first","initial",
    "moment","opportunity","priority","transition","window","catastrophic",
    "decisive","historic","landmark","once","unprecedented","hurry","after",
    "finally","emergency","pressing","time","sudden","accelerate","decelerate",
}

US_VS_THEM_WORDS = {
    "ally","american","coalition","colleague","compatriot","conservative",
    "constitutional","fellow","friend","loyal","movement","our","partner",
    "patriot","people","supporter","team","together","unified","unity",
    "us","we","adversary","alien","anarchist","antiamerican","bureaucrat",
    "deep","elite","enemy","establishment","extremist","faction","foreign",
    "globalist","hostile","ideologue","infiltrator","liberal","leftist",
    "marxist","opponent","opposition","outsider","radical","regime",
    "socialist","subversive","swamp","them","they","unelected","woke",
    "battle","combat","confrontation","contest","defeat","defend","fight",
    "resist","resistance","struggle","war","warfare",
}

LEGITIMACY_WORDS = {
    "amendment","article","charter","clause","codify","congress",
    "constitution","constitutional","court","enact","enumerate","founding",
    "frame","framers","judicial","jurisdiction","law","lawful","legal",
    "legislation","legitimate","precedent","provision","ratify","statute",
    "statutory","accountability","ballot","bipartisan","check","citizen",
    "civic","civil","consent","democratic","election","elect","mandate",
    "public","referendum","represent","representation","transparent",
    "transparency","vote","voter","agency","bureau","commission",
    "committee","department","expert","federal","institutional","office",
    "official","policy","process","professional","protocol","standard",
    "illegitimate","unconstitutional","unlawful","unelected","unaccountable","extralegal",
}

ALL_CATEGORIES = {
    "Power":      POWER_WORDS,
    "Threat":     THREAT_WORDS,
    "Moral":      MORAL_WORDS,
    "Urgency":    URGENCY_WORDS,
    "Us vs Them": US_VS_THEM_WORDS,
    "Legitimacy": LEGITIMACY_WORDS,
}

COLOR_MAP = {
    "Power":      "#FF6B6B",
    "Threat":     "#4ECDC4",
    "Moral":      "#45B7D1",
    "Urgency":    "#96CEB4",
    "Us vs Them": "#F7DC6F",
    "Legitimacy": "#C39BD3",
}

# ============================================
# ANALYSIS FUNCTIONS
# ============================================

def tokenize(text: str) -> List[str]:
    return re.sub(r'[^\w\s]', '', text.lower()).split()

def calculate_scores(text: str) -> Dict[str, float]:
    words = tokenize(text)
    total = len(words)
    if total == 0:
        return {cat: 0.0 for cat in ALL_CATEGORIES}
    return {cat: round(sum(1 for w in words if w in ws) / total * 1000, 2)
            for cat, ws in ALL_CATEGORIES.items()}

def get_contributions(text: str) -> Dict[str, List[str]]:
    words = tokenize(text)
    result = {cat: [] for cat in ALL_CATEGORIES}
    for word in words:
        for cat, ws in ALL_CATEGORIES.items():
            if word in ws:
                result[cat].append(word)
    return result

def highlight_text(text: str) -> str:
    word_cat = {}
    words = tokenize(text)
    for word in words:
        for cat, ws in ALL_CATEGORIES.items():
            if word in ws:
                word_cat[word] = cat

    tokens = re.findall(r'(\w+|\W+)', text)
    out = []
    for token in tokens:
        lower = token.lower()
        if lower in word_cat:
            cat = word_cat[lower]
            color = COLOR_MAP[cat]
            out.append(
                f'<span style="background:{color};padding:1px 4px;'
                f'border-radius:3px;font-weight:600;" title="{cat}">{token}</span>'
            )
        else:
            out.append(token)
    return ''.join(out)

def build_scores_table(scores_a, scores_b, label_a, label_b):
    rows = []
    for cat in ALL_CATEGORIES:
        a = scores_a[cat]
        b = scores_b[cat]
        diff = round(b - a, 2)
        arrow = "▲" if diff > 0 else ("▼" if diff < 0 else "—")
        rows.append([cat, a, b, f"{arrow} {abs(diff)}"])
    df = pd.DataFrame(rows, columns=["Category", label_a or "Text A", label_b or "Text B", "Difference"])
    return df

def build_word_breakdown(contrib, label):
    lines = []
    for cat, words in contrib.items():
        unique = sorted(set(words))
        if unique:
            color = COLOR_MAP[cat]
            lines.append(
                f'<span style="background:{color};padding:1px 6px;border-radius:3px;'
                f'font-weight:700;font-size:0.85em;">{cat}</span> '
                f'({len(unique)}): {", ".join(unique)}'
            )
    return "<br><br>".join(lines) if lines else "<em>No rhetorical words detected.</em>"

def build_insights(scores_a, scores_b, label_a, label_b):
    label_a = label_a or "Text A"
    label_b = label_b or "Text B"
    dom_a = max(scores_a, key=scores_a.get)
    dom_b = max(scores_b, key=scores_b.get)
    diffs = {cat: scores_b[cat] - scores_a[cat] for cat in ALL_CATEGORIES}
    big = max(diffs, key=lambda x: abs(diffs[x]))
    direction = "higher" if diffs[big] > 0 else "lower"

    return (
        f"**{label_a}** is most dominant in **{dom_a}** rhetoric "
        f"({scores_a[dom_a]:.1f} per 1,000 words)\n\n"
        f"**{label_b}** is most dominant in **{dom_b}** rhetoric "
        f"({scores_b[dom_b]:.1f} per 1,000 words)\n\n"
        f"Biggest divergence: **{big}** — {label_b} scores "
        f"{abs(diffs[big]):.2f} points {direction} than {label_a}"
    )

# ============================================
# MAIN ANALYZE FUNCTION
# ============================================

def analyze(text_a, label_a, text_b, label_b):
    if not text_a and not text_b:
        empty = "<em>Please enter at least one text.</em>"
        return empty, empty, None, empty, empty, empty

    label_a = label_a.strip() or "Text A"
    label_b = label_b.strip() or "Text B"

    scores_a = calculate_scores(text_a) if text_a else {c: 0.0 for c in ALL_CATEGORIES}
    scores_b = calculate_scores(text_b) if text_b else {c: 0.0 for c in ALL_CATEGORIES}

    contrib_a = get_contributions(text_a) if text_a else {c: [] for c in ALL_CATEGORIES}
    contrib_b = get_contributions(text_b) if text_b else {c: [] for c in ALL_CATEGORIES}

    # Highlighted text
    hl_a = highlight_text(text_a) if text_a else "<em>No text entered.</em>"
    hl_b = highlight_text(text_b) if text_b else "<em>No text entered.</em>"

    # Scores table
    df = build_scores_table(scores_a, scores_b, label_a, label_b)

    # Word breakdowns
    words_a = build_word_breakdown(contrib_a, label_a)
    words_b = build_word_breakdown(contrib_b, label_b)

    # Insights
    insights = build_insights(scores_a, scores_b, label_a, label_b)

    return hl_a, hl_b, df, words_a, words_b, insights

# ============================================
# GRADIO UI
# ============================================

legend_html = """
<div style="display:flex;flex-wrap:wrap;gap:8px;margin-bottom:8px;">
  <span style="background:#FF6B6B;padding:2px 10px;border-radius:4px;font-weight:600;">Power</span>
  <span style="background:#4ECDC4;padding:2px 10px;border-radius:4px;font-weight:600;">Threat</span>
  <span style="background:#45B7D1;padding:2px 10px;border-radius:4px;font-weight:600;">Moral</span>
  <span style="background:#96CEB4;padding:2px 10px;border-radius:4px;font-weight:600;">Urgency</span>
  <span style="background:#F7DC6F;padding:2px 10px;border-radius:4px;font-weight:600;">Us vs Them</span>
  <span style="background:#C39BD3;padding:2px 10px;border-radius:4px;font-weight:600;">Legitimacy</span>
</div>
"""

with gr.Blocks(title="Rhetorical Fingerprint Analyzer", theme=gr.themes.Soft()) as demo:

    gr.Markdown("# 📝 Rhetorical Fingerprint Analyzer")
    gr.Markdown(
        "Decode the rhetorical DNA of any text. Paste two passages and compare their "
        "**power**, **threat**, **moral**, **urgency**, **us vs them**, and **legitimacy** signals."
    )

    with gr.Row():
        with gr.Column():
            label_a = gr.Textbox(label="Label for Text A", value="Text A", max_lines=1)
            text_a  = gr.Textbox(label="Text A", placeholder="Paste your first paragraph here...", lines=8)
        with gr.Column():
            label_b = gr.Textbox(label="Label for Text B", value="Text B", max_lines=1)
            text_b  = gr.Textbox(label="Text B", placeholder="Paste your second paragraph here...", lines=8)

    analyze_btn = gr.Button("🔍 Analyze Rhetorical Fingerprint", variant="primary", size="lg")

    gr.Markdown("---")
    gr.Markdown("## 📊 Scores (per 1,000 words)")
    scores_table = gr.Dataframe(interactive=False)

    gr.Markdown("## 💡 Insights")
    insights_out = gr.Markdown()

    gr.Markdown("## 🎨 Highlighted Text")
    gr.HTML(legend_html)

    with gr.Row():
        with gr.Column():
            gr.Markdown("### Text A")
            highlight_a = gr.HTML()
        with gr.Column():
            gr.Markdown("### Text B")
            highlight_b = gr.HTML()

    gr.Markdown("## 📋 Contributing Words by Category")
    with gr.Row():
        with gr.Column():
            gr.Markdown("### Text A")
            words_a_out = gr.HTML()
        with gr.Column():
            gr.Markdown("### Text B")
            words_b_out = gr.HTML()

    analyze_btn.click(
        fn=analyze,
        inputs=[text_a, label_a, text_b, label_b],
        outputs=[highlight_a, highlight_b, scores_table, words_a_out, words_b_out, insights_out]
    )

    gr.Markdown("---")
    gr.Markdown("*Try pasting political speeches, marketing copy, or news headlines to see how rhetoric differs.*")

demo.launch()
