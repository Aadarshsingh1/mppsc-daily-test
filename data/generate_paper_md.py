# -*- coding: utf-8 -*-
import json

json_path = r"c:\Users\hp\Documents\antigravity\wonderful-noether\data\mppsc_mock_01.json"
with open(json_path, "r", encoding="utf-8") as f:
    questions = json.load(f)

md_lines = [
    "# MPPSC Prelims Mock Test 01 (General Studies Paper-I)",
    "**Total Questions:** 100 | **Time Allowed:** 120 Minutes | **Maximum Marks:** 100",
    "**Marking Scheme:** Correct: +1.00 | Incorrect: -0.25 | Unattempted: 0.00",
    "*(Note: Official MPPSC Prelims allocates 2 marks per question without negative marking. This test uses the requested practice marking scheme.)*",
    "\n---\n"
]

current_unit = ""
for q in questions:
    if q["unit"] != current_unit:
        current_unit = q["unit"]
        md_lines.append(f"\n## {current_unit}\n")
    
    md_lines.append(f"### Q{q['id']}. {q['question_en']}")
    md_lines.append(f"**प्र. {q['id']}. {q['question_hi']}**\n")
    
    letters = ["A", "B", "C", "D"]
    for i, l in enumerate(letters):
        md_lines.append(f"- **({l})** {q['options_en'][i]} / {q['options_hi'][i]}")
    md_lines.append("")

output_md = r"c:\Users\hp\Documents\antigravity\wonderful-noether\mppsc_mock_test_01_paper.md"
with open(output_md, "w", encoding="utf-8") as f:
    f.write("\n".join(md_lines))

print("Markdown question paper written successfully!")
