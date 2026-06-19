# 📝 Rhetorical Fingerprint Analyzer

A Gradio app that decodes the rhetorical DNA of any text — scoring it across six dimensions of persuasive language and visualizing how two passages compare.

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
- **Scores table** with difference column for direct comparison
- **Word-level breakdown** by category
- **Auto-generated insights** — dominant category, biggest divergence

## Live Demo

[🔗 Try it on Hugging Face Spaces](https://narrovue-rhetorical-fingerprint.hf.space)

Also embedded at [narrovue.com](https://narrovue.com)

## Run Locally

```bash
git clone https://github.com/narrovue/rhetorical_fingerprint
cd rhetorical_fingerprint
pip install -r requirements.txt
python app.py
```

## Deploy Your Own

1. Fork this repo
2. Go to [huggingface.co/new-space](https://huggingface.co/new-space)
3. Select **Gradio** as the SDK and set visibility to **Public**
4. Upload `app.py` and `requirements.txt`
5. Embed anywhere with:

```html
<iframe
  src="https://your-username-rhetorical-fingerprint.hf.space"
  width="100%"
  height="900"
  style="border:none; border-radius:8px;"
></iframe>
```

## Tech Stack

- [Gradio](https://gradio.app) — app framework
- [Pandas](https://pandas.pydata.org) — data handling

## Use Cases

- Compare political speeches across candidates or eras
- Audit marketing copy for emotional register
- Analyze how news outlets frame the same story
- Study rhetorical shifts in policy documents over time
- Media literacy education

## License

MIT
