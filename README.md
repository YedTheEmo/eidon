# EIDON
Eidon is a command-line tool for advanced cognitive function and socionics analysis.
---

## Features

- **Analyze MBTI Types:**
Output the cognitive function stacks for Ego, Subconscious, Unconscious, and Superego for any MBTI type.
- **Socionics Integration:**
Show Socionics type mappings and compute exact Socionics intertype relations using mathematically precise variable-alteration logic.
- **Type Inference:**
Infer the closest MBTI type from any four-function cognitive stack, with confidence scoring and difference reporting.
- **Command-Line Interface:**
Easy-to-use CLI with clear subcommands and arguments for analysis and inference.

---

## Installation

Clone the repository and ensure you have Python 3.7+ installed.

```bash
git clone https://github.com/yourusername/eidon.git
cd eidon
```


---

## Usage

### Analyze an MBTI Type

```bash
python3 eidon.py analyze --type INFJ
```

Show Socionics types and compare to another MBTI type for intertype relation:

```bash
python3 eidon.py analyze --type INFJ --show-socionics --compare-to ISTJ
```

Select specific function blocks to display:

```bash
python3 eidon.py analyze --type ENTP --functions ego unconscious
```


### Infer MBTI Type from Stack

```bash
python3 eidon.py infer --stack Ni Fe Ti Se
```

This will output the closest MBTI type, confidence, and show differences if not an exact match.

---

## Example Output

```
python3 eidon.py analyze --type INFJ --compare-to ISTJ --show-socionics
Analysis for INFJ (MBTI):
Ego: Ni-Fe-Ti-Se  (MBTI: INFJ)
Subconscious: Se-Ti-Fe-Ni  (MBTI: ESTP)
Unconscious: Ne-Fi-Te-Si  (MBTI: ENFP)
Superego: Si-Te-Fi-Ne  (MBTI: ISTJ)

Socionics Relation between INFJ and ISTJ: Super-Ego
```
