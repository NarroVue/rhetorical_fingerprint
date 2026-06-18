# 📝 Rhetorical Fingerprint Analyzer

A Streamlit app that decodes the rhetorical DNA of any applicable text — scoring it across six dimensions of persuasive language and visualizing how two passages compare.

## What It Does

Paste any political speech, news headline, marketing copy, or policy document and the app scores it across six rhetorical categories, highlights every contributing word, and surfaces insights about the language being used.

### Six Rhetorical Categories

| Category | What It Captures |
|---|---|
| **Power** | Control, authority, dominance, victory |
| **Threat** | Danger, crisis, risk, enemies |
| **Moral** | Ethics, values, heritage, right vs. wrong |
| **Urgency** | Time pressure, necessity, immediacy |
| **Us vs. Them** | In-group identity, out-group othering |
| **Legitimacy** | Legal, democratic, and institutional authority |

Scores are normalized to **occurrences per 1,000 words** so texts of different lengths compare fairly.

## Features

- **Side-by-side comparison** of two texts
- **Color-coded highlighting** of rhetorical words in context
- **Bar charts** for each text's fingerprint
- **Line chart** overlaying both fingerprints for direct comparison
- **Word-level breakdown** by category via expandable panel
- **Auto-generated insights** — dominant category, biggest divergence

## Live Demo

[🔗 Try it on Streamlit Community Cloud](https://your-app-url.streamlit.app) 

## Run Locally

```bash
git clone https://github.com/yourname/rhetorical-fingerprint
cd rhetorical-fingerprint
pip install -r requirements.txt
streamlit run rhetorical_fingerprint.py
```

## Deploy Your Own

1. Fork this repo
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repo and deploy
4. Embed anywhere with:

```html
<iframe
  src="https://your-app-url.streamlit.app/?embed=true"
  width="100%"
  height="900"
  style="border:none; border-radius:8px;"
></iframe>
```

## Tech Requirements Stack

- [Streamlit](https://streamlit.io) — app framework
- [Pandas](https://pandas.pydata.org) — data handling
- [Altair](https://altair-viz.github.io) — visualizations

## Use Cases

- Compare political speeches across candidates or eras
- Audit marketing copy for emotional register
- Analyze how news outlets frame the same story
- Study rhetorical shifts in policy documents over time
- Media literacy education

## License

MIT
