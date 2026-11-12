#!/usr/bin/env bash
# Verify cross-agent parity, host character limits, file references, and Antigravity bundle health.
#
#   tools/check.sh
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

FAIL=0
ok()   { printf '  ok    %s\n' "$1"; }
fail() { printf '  FAIL  %s\n' "$1"; FAIL=1; }

charcount() {
  python3 -c 'import sys; print(len(open(sys.argv[1], encoding="utf-8").read()))' "$1"
}

extract_block() {
  awk 'BEGIN{n=0} /^```/{n++; if(n==2) exit; next} n==1{print}' "$1"
}

echo "1. Universal AGENTS.md & SKILL.md metadata limits"
bytes=$(wc -c < AGENTS.md | tr -d ' ')
lines=$(wc -l < AGENTS.md | tr -d ' ')
if [ "$bytes" -lt 32768 ] && [ "$lines" -le 200 ]; then
  ok "AGENTS.md is $bytes bytes, $lines lines (limits: <32768 bytes, <=200 lines)"
else
  fail "AGENTS.md exceeds recommended size ($bytes bytes, $lines lines)"
fi

desc_info=$(python3 - <<'PY'
import re
t = open("SKILL.md", encoding="utf-8").read()
m = re.match(r"^---\n(.*?)\n---", t, re.S)
assert m, "No frontmatter"
fm = m.group(1)
name = re.search(r"^name:\s*(.+)$", fm, re.M).group(1).strip()
desc = re.search(r"^description:\s*(.+)$", fm, re.M).group(1).strip()
bad_chars = ("<" in desc) or (">" in desc)
print(f"{name}|{len(desc)}|{int(bad_chars)}")
PY
)
IFS='|' read -r sname dlen dbad <<< "$desc_info"
if [ "$sname" = "short-form-script-writer-pro" ] && [ "$dlen" -le 1024 ] && [ "$dbad" = "0" ]; then
  ok "SKILL.md frontmatter valid: name='$sname', description=$dlen/1024 chars"
else
  fail "SKILL.md frontmatter invalid ($desc_info)"
fi

echo
echo "2. Portable prompt host character budgets"
check_budget() {
  local file=$1 limit=$2 host=$3 tmp n
  if [ ! -f "$file" ]; then fail "$file missing"; return; fi
  tmp=$(mktemp)
  extract_block "$file" > "$tmp"
  n=$(charcount "$tmp")
  rm -f "$tmp"
  if [ "$n" -eq 0 ]; then fail "$file has no copyable code block"; return; fi
  if [ "$n" -le "$limit" ]; then
    ok "$(printf '%-38s %5s / %s chars  (%s)' "$file" "$n" "$limit" "$host")"
  else
    fail "$(printf '%-38s %5s / %s chars  (%s) — over by %s' "$file" "$n" "$limit" "$host" "$((n-limit))")"
  fi
}
check_budget portable/mini-prompt.md             1450 "ChatGPT Free <=1500"
check_budget portable/gemini-gem-instructions.md 3900 "Gemini Gem ~4000"
check_budget portable/kimi-instructions.md       3900 "Kimi+ Assistant ~4000"
check_budget portable/chatgpt-instructions.md    4900 "ChatGPT Paid <=5000"
check_budget portable/kickoff-prompt.md          6000 "First-message chat paste"
check_budget portable/system-prompt.md           7900 "Custom GPT / Projects <=8000"

echo
echo "3. Referenced repository paths exist"
missing=0
while IFS= read -r p; do
  [ -n "$p" ] || continue
  if [ ! -e "$p" ]; then
    fail "referenced path missing: $p"
    missing=1
  fi
done < <(
  grep -hoE '`(references|scripts|portable|tools|bundles|evals)/[A-Za-z0-9._/-]+`' \
    SKILL.md AGENTS.md README.md llms.txt 2>/dev/null \
    | sed 's/`//g' | grep -v '\*' | sort -u
)
[ "$missing" -eq 0 ] && ok "all referenced repository paths exist"

echo
echo "4. Core behavioral rules survive across SKILL.md, AGENTS.md & all 6 portable prompts"
check_surface_rules() {
  local label=$1 file=$2
  for token in "Hook" "Story" "Turn" "Takeaway" "Closer" "30s" "45s" "60s" "75s" "90s" "120s" "sharpen" "—"; do
    if ! grep -q "$token" "$file"; then
      fail "$label missing required rule/token: '$token'"
      return
    fi
  done
  ok "$label carries all 5 beats, all 6 duration tiers, research boundary & humanizer rules"
}

check_surface_rules "SKILL.md"  SKILL.md
check_surface_rules "AGENTS.md" AGENTS.md
for p in portable/system-prompt.md portable/gemini-gem-instructions.md portable/kimi-instructions.md \
         portable/chatgpt-instructions.md portable/mini-prompt.md portable/kickoff-prompt.md; do
  tmp=$(mktemp)
  extract_block "$p" > "$tmp"
  check_surface_rules "$p (block)" "$tmp"
  rm -f "$tmp"
done

echo
echo "5. Corpus freshness, Antigravity package sync, and Gemini upload legality"
ANTIGRAVITY_DIR=".agents/skills/short-form-script-writer-pro"
ANTIGRAVITY_ZIP="bundles/antigravity/short-form-script-writer-pro.zip"
if [ ! -f llms-full.txt ] || [ ! -f bundles/short-form-script-writer-pro.zip ] \
   || [ ! -f "$ANTIGRAVITY_ZIP" ] || [ ! -f "$ANTIGRAVITY_DIR/SKILL.md" ] \
   || [ ! -f "$ANTIGRAVITY_DIR/references/combined-skills-fallback.md" ] \
   || [ ! -f "$ANTIGRAVITY_DIR/scripts/validate_script.py" ] \
   || [ ! -f short-form-script-writer-pro.skill ]; then
  fail "one or more generated artifacts missing (run tools/build.sh)"
else
  snap_dir=$(mktemp -d)
  cp llms-full.txt "$snap_dir/llms-full.txt"
  cp bundles/short-form-script-writer-pro.zip "$snap_dir/gemini.zip"
  cp "$ANTIGRAVITY_ZIP" "$snap_dir/antigravity.zip"
  cp short-form-script-writer-pro.skill "$snap_dir/bundle.skill"
  cp -a "$ANTIGRAVITY_DIR" "$snap_dir/antigravity-skill"
  bash tools/build.sh >/dev/null
  if cmp -s llms-full.txt "$snap_dir/llms-full.txt" \
     && cmp -s bundles/short-form-script-writer-pro.zip "$snap_dir/gemini.zip" \
     && cmp -s "$ANTIGRAVITY_ZIP" "$snap_dir/antigravity.zip" \
     && cmp -s short-form-script-writer-pro.skill "$snap_dir/bundle.skill" \
     && diff -qr "$ANTIGRAVITY_DIR" "$snap_dir/antigravity-skill" >/dev/null; then
    ok "corpus, Antigravity workspace skill/archive, Gemini bundle, and .skill are up to date"
  else
    fail "generated artifacts were out of sync with sources (rebuilt now; commit updated files)"
  fi
  rm -rf "$snap_dir"

  bad_zip=$(python3 - <<'PY2'
import zipfile
with zipfile.ZipFile("bundles/short-form-script-writer-pro.zip") as zf:
    names = zf.namelist()
    assert "short-form-script-writer-pro/SKILL.md" in names, "Missing root SKILL.md in zip"
    bad = [n for n in names if not n.endswith((".md", ".txt"))]
    print(",".join(bad))
PY2
  )
  if [ -z "$bad_zip" ]; then
    ok "bundles/short-form-script-writer-pro.zip is Gemini-upload legal (root SKILL.md + plain text only)"
  else
    fail "bundles/short-form-script-writer-pro.zip contains non-plain-text entries: $bad_zip"
  fi

  antigravity_zip_check=$(python3 - <<'PY2'
import zipfile
expected = {
    "short-form-script-writer-pro/SKILL.md",
    "short-form-script-writer-pro/references/combined-skills-fallback.md",
    "short-form-script-writer-pro/scripts/validate_script.py",
}
with zipfile.ZipFile("bundles/antigravity/short-form-script-writer-pro.zip") as zf:
    actual = {name for name in zf.namelist() if not name.endswith("/")}
    if actual != expected:
        raise SystemExit(f"unexpected Antigravity archive entries: {sorted(actual)}")
print("ok")
PY2
  )
  if [ "$antigravity_zip_check" = "ok" ] && cmp -s SKILL.md "$ANTIGRAVITY_DIR/SKILL.md"; then
    ok "Antigravity bundle has the skill manifest, fallback reference, and validator at standard skill paths"
  else
    fail "Antigravity bundle contents or workspace SKILL.md are invalid"
  fi
fi

echo
echo "6. Deterministic script validator passes on SKILL.md sample & Iteration 3 eval suite"
python3 - <<'PY'
import re, subprocess, sys
t = open("SKILL.md", encoding="utf-8").read()
m = re.search(r"### Sample Output\n```text\n(.*?)\n```", t, re.S)
assert m, "Sample Output missing"
r = subprocess.run(["python3", "scripts/validate_script.py", "-"], input=m.group(1), text=True, capture_output=True)
if r.returncode != 0:
    print(r.stdout, r.stderr)
    sys.exit(1)
PY
if [ $? -eq 0 ]; then
  ok "SKILL.md Sample Output passes scripts/validate_script.py"
else
  fail "SKILL.md Sample Output failed scripts/validate_script.py"
fi

if python3 scripts/validate_script.py evals/iteration-3/eval-1/output.txt --duration 60 >/dev/null \
   && python3 scripts/validate_script.py evals/iteration-3/eval-2/output.txt --duration 90 >/dev/null \
   && python3 scripts/validate_script.py evals/iteration-3/eval-3/output.txt --duration 30 \
        --locked-text "Your morning coffee tastes bitter because the water is too hot, not because the beans are bad." >/dev/null \
   && python3 scripts/validate_script.py evals/iteration-3/eval-4/output.txt --duration 120 >/dev/null; then
  ok "All 4 complexity-tier scripts in evals/iteration-3/ pass scripts/validate_script.py"
else
  fail "One or more scripts in evals/iteration-3/ failed validation"
fi

rm -rf scripts/__pycache__

echo
if [ "$FAIL" -eq 0 ]; then
  echo "ALL CHECKS PASSED."
  exit 0
else
  echo "SOME CHECKS FAILED."
  exit 1
fi
