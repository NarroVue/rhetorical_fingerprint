import streamlit as st
import pandas as pd
import re
from collections import Counter
from typing import Dict, List, Tuple
import altair as alt

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
    "privatize","privatise","resource","transfer", "dominate", "force","strong",
    "lead","influence","master","victory","win","conquer","decide","determine",
    "execute","rule","sovereign","overcome","triumph","crush","defeat",
    "superior","might",
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
    "degradation","deterioration","disintegration","risk","destroy","damage",
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
    "wrong","ethical","honest","good","evil","compassion","Compassionate",
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

US VS THEM_WORDS = {
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
        "illegitimate","unconstitutional","unlawful","unelected",
        "unaccountable","extralegal",
    },

ALL_CATEGORIES = {
    "Power": POWER_WORDS,
    "Threat": THREAT_WORDS,
    "Moral": MORAL_WORDS,
    "Urgency": URGENCY_WORDS,
    "Us vs Them": US VS THEM_WORDS,
    "Legitimacy": LEGITIMACY_WORDS,
}

# ============================================
# TEXT ANALYSIS FUNCTIONS
# ============================================

def tokenize_words(text: str) -> List[str]:
    """Convert text to lowercase words (simple tokenization)."""
    text = re.sub(r'[^\w\s]', '', text.lower())
    return text.split()

def calculate_scores(text: str) -> Dict[str, float]:
    """Calculate raw and normalized scores for each rhetorical category."""
    words = tokenize_words(text)
    total_words = len(words)
    
    if total_words == 0:
        return {cat: 0.0 for cat in ALL_CATEGORIES.keys()}
    
    scores = {}
    for category, word_set in ALL_CATEGORIES.items():
        count = sum(1 for w in words if w in word_set)
        # Normalize to per-1000 words for consistent comparison
        scores[category] = (count / total_words) * 1000
    
    return scores

def get_word_contributions(text: str) -> Dict[str, List[Tuple[str, str]]]:
    """Return list of (word, category) for each word that contributes to scores."""
    words = tokenize_words(text)
    contributions = {cat: [] for cat in ALL_CATEGORIES.keys()}
    
    for word in words:
        for category, word_set in ALL_CATEGORIES.items():
            if word in word_set:
                contributions[category].append((word, category))
                
    return contributions

def highlight_text(text: str, contributions: Dict[str, List[Tuple[str, str]]]) -> str:
    """Add HTML spans to highlight words by their rhetorical category."""
    words = re.findall(r'(\w+|\W+)', text)  # Split keeping punctuation
    highlighted_words = []
    
    color_map = {
        "Power": "#FF6B6B",    # red
        "Threat": "#4ECDC4",   # teal
        "Moral": "#45B7D1",    # blue
        "Urgency": "#96CEB4"   # green
    }
    
    # Create a lookup for word contributions
    word_cats = {}
    for cat, word_list in contributions.items():
        for w, c in word_list:
            word_cats[w.lower()] = c
    
    for word in words:
        word_lower = word.lower()
        if word_lower in word_cats:
            category = word_cats[word_lower]
            color = color_map.get(category, "#FFFFFF")
            highlighted_words.append(f'<span style="background-color: {color}; padding: 2px 2px; border-radius: 3px;" title="{category}">{word}</span>')
        else:
            highlighted_words.append(word)
    
    return ''.join(highlighted_words)

# ============================================
# VISUALIZATION FUNCTIONS
# ============================================

def create_radar_chart(scores1: Dict[str, float], scores2: Dict[str, float], label1: str, label2: str):
    """Create a radar chart comparing two rhetorical fingerprints."""
    categories = list(ALL_CATEGORIES.keys())
    
    # Prepare data for Altair (using polar coordinates via line chart)
    df1 = pd.DataFrame({
        "Category": categories,
        "Score": [scores1[cat] for cat in categories],
        "Text": label1
    })
    df2 = pd.DataFrame({
        "Category": categories,
        "Score": [scores2[cat] for cat in categories],
        "Text": label2
    })
    df = pd.concat([df1, df2])
    
    chart = alt.Chart(df).mark_line(point=True).encode(
        x=alt.X("Category", sort=None),
        y=alt.Y("Score", scale=alt.Scale(domain=[0, max(df["Score"]) * 1.2])),
        color="Text",
        strokeDash="Text"
    ).properties(
        width=400,
        height=400,
        title="Rhetorical Fingerprint Comparison"
    )
    
    return chart

def create_bar_chart(scores: Dict[str, float], title: str):
    """Create a bar chart for a single text."""
    df = pd.DataFrame({
        "Category": list(scores.keys()),
        "Score": list(scores.values())
    })
    
    chart = alt.Chart(df).mark_bar().encode(
        x=alt.X("Category", sort=None),
        y="Score",
        color="Category"
    ).properties(
        width=400,
        height=300,
        title=title
    )
    
    return chart

# ============================================
# MAIN STREAMLIT APP
# ============================================

st.set_page_config(page_title="Rhetorical Fingerprint Analyzer", layout="wide")

st.title("📝 Rhetorical Fingerprint Analyzer")
st.markdown("""
Analyze the **power**, **threat**, **moral**, and **urgency** fingerprint of any text. 
Compare two paragraphs and see which words drive each score.
""")

# Sidebar for explanations
with st.sidebar:
    st.header("🎯 About Rhetorical Categories")
    st.markdown("""
    - **Power**: Words about control, authority, strength, victory  
      *(e.g., dominate, lead, conquer)*
    
    - **Threat**: Words about danger, risk, crisis, warning  
      *(e.g., danger, attack, collapse)*
    
    - **Moral**: Words about ethics, justice, right/wrong  
      *(e.g., justice, honest, corrupt)*
    
    - **Urgency**: Words about time, speed, necessity  
      *(e.g., now, immediate, critical)*
    
    *Scores are normalized to occurrences per 1000 words.*
    """)

# Main input area
col1, col2 = st.columns(2)

with col1:
    st.subheader("📄 Text A")
    text_a = st.text_area("Paste first paragraph:", height=200, 
                          placeholder="Enter your first text here...")
    label_a = st.text_input("Label for Text A:", value="Text A")

with col2:
    st.subheader("📄 Text B")
    text_b = st.text_area("Paste second paragraph:", height=200,
                          placeholder="Enter your second text here...")
    label_b = st.text_input("Label for Text B:", value="Text B")

# Analysis button
analyze = st.button("🔍 Analyze Rhetorical Fingerprint", type="primary")

if analyze:
    if not text_a and not text_b:
        st.warning("Please paste at least one paragraph to analyze.")
    else:
        # Calculate scores
        scores_a = calculate_scores(text_a) if text_a else {cat: 0 for cat in ALL_CATEGORIES}
        scores_b = calculate_scores(text_b) if text_b else {cat: 0 for cat in ALL_CATEGORIES}
        
        # Get word contributions
        contrib_a = get_word_contributions(text_a) if text_a else {}
        contrib_b = get_word_contributions(text_b) if text_b else {}
        
        # Display scores in metrics
        st.header("📊 Rhetorical Scores (per 1000 words)")
        
        # Create comparison DataFrame
        comparison_data = []
        for category in ALL_CATEGORIES.keys():
            comparison_data.append({
                "Category": category,
                label_a: round(scores_a[category], 2),
                label_b: round(scores_b[category], 2),
                "Difference": round(scores_b[category] - scores_a[category], 2)
            })
        
        df_comparison = pd.DataFrame(comparison_data)
        st.dataframe(df_comparison, use_container_width=True)
        
        # Visualizations
        col_viz1, col_viz2 = st.columns(2)
        
        with col_viz1:
            if text_a:
                chart_a = create_bar_chart(scores_a, f"Rhetorical Fingerprint: {label_a}")
                st.altair_chart(chart_a, use_container_width=True)
        
        with col_viz2:
            if text_b:
                chart_b = create_bar_chart(scores_b, f"Rhetorical Fingerprint: {label_b}")
                st.altair_chart(chart_b, use_container_width=True)
        
        # Radar chart comparison if both texts exist
        if text_a and text_b:
            st.subheader("🔄 Direct Comparison")
            radar_chart = create_radar_chart(scores_a, scores_b, label_a, label_b)
            st.altair_chart(radar_chart, use_container_width=True)
        
        # Highlighted text sections
        st.header("🎨 Highlighted Text Analysis")
        st.markdown("""
        *Words are color-coded by rhetorical category. Hover over highlighted words to see the category.*
        **Legend:** 🔴 Power | 🔵 Threat | 🔷 Moral | 🟢 Urgency
        """)
        
        col_highlight1, col_highlight2 = st.columns(2)
        
        with col_highlight1:
            if text_a:
                st.subheader(f"{label_a} - Highlighted")
                highlighted_a = highlight_text(text_a, contrib_a)
                st.markdown(highlighted_a, unsafe_allow_html=True)
                
                # Show word lists per category
                with st.expander("📋 View contributing words by category"):
                    for category, words in contrib_a.items():
                        if words:
                            unique_words = sorted(set([w for w, _ in words]))
                            st.write(f"**{category}** ({len(unique_words)} unique): {', '.join(unique_words)}")
        
        with col_highlight2:
            if text_b:
                st.subheader(f"{label_b} - Highlighted")
                highlighted_b = highlight_text(text_b, contrib_b)
                st.markdown(highlighted_b, unsafe_allow_html=True)
                
                with st.expander("📋 View contributing words by category"):
                    for category, words in contrib_b.items():
                        if words:
                            unique_words = sorted(set([w for w, _ in words]))
                            st.write(f"**{category}** ({len(unique_words)} unique): {', '.join(unique_words)}")
        
        # Insights
        if text_a and text_b:
            st.header("💡 Key Insights")
            dominant_a = max(scores_a, key=scores_a.get)
            dominant_b = max(scores_b, key=scores_b.get)
            
            st.write(f"- **{label_a}** is most dominant in **{dominant_a}** rhetoric")
            st.write(f"- **{label_b}** is most dominant in **{dominant_b}** rhetoric")
            
            # Find biggest difference
            differences = {cat: scores_b[cat] - scores_a[cat] for cat in ALL_CATEGORIES}
            biggest_diff_cat = max(differences, key=lambda x: abs(differences[x]))
            direction = "higher" if differences[biggest_diff_cat] > 0 else "lower"
            st.write(f"- Biggest difference is in **{biggest_diff_cat}**: {label_b} is {abs(differences[biggest_diff_cat]):.2f} points {direction} per 1000 words")

else:
    st.info("👆 Paste your paragraphs above and click 'Analyze Rhetorical Fingerprint' to get started!")

# Footer
st.markdown("---")
st.markdown("💡 **Tip:** Try pasting political speeches, marketing copy, or news headlines to see how rhetoric differs!")
