#!/usr/bin/env python3
"""Grade all eval runs for script-writer skill."""
import json
import re
import os

BASE = os.path.dirname(os.path.abspath(__file__))


def count_pattern(text, pattern):
    return len(re.findall(pattern, text))


def split_slides(text):
    """Split markdown into individual slides by --- separator."""
    # Split by --- that appears at the start of a line (slide separator)
    parts = re.split(r'\n---\n', text)
    # First part includes frontmatter, rest are slides
    return parts


def extract_scripts(text):
    """Extract all [스크립트] blocks from text."""
    return re.findall(r'<!--\s*\n?\[스크립트\].*?-->', text, re.DOTALL)


def grade_eval1(path, config_name):
    """Grade eval-1: mini-fixture-scripts."""
    filepath = os.path.join(path, "outputs", "slides.md")
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}

    with open(filepath, "r") as f:
        content = f.read()

    slides = split_slides(content)
    scripts = extract_scripts(content)
    num_slides = len(slides)

    results = {"config": config_name, "expectations": []}

    # 1. Completeness: all slides have [스크립트]
    has_script_count = sum(1 for s in slides if '[스크립트]' in s)
    results["expectations"].append({
        "text": f"완전성: {num_slides}개 슬라이드 중 {has_script_count}개에 [스크립트] 블록 존재",
        "passed": has_script_count >= 6,
        "evidence": f"{has_script_count}/{num_slides} slides have [스크립트]"
    })

    # 2. [click] sync: check v-click slides
    click_count = count_pattern(content, r'\[click\]')
    vclick_elements = count_pattern(content, r'<v-click|v-clicks>')
    results["expectations"].append({
        "text": f"[click] 싱크: [click] 마커 {click_count}개 존재",
        "passed": click_count >= 10,  # 4 + 6 + some from other slides
        "evidence": f"[click]: {click_count}, v-click elements: {vclick_elements}"
    })

    # 3. Conversational tone
    formal_patterns = re.findall(r'(?:^|\s)([\w]+이다[.\s]|[\w]+한다[.\s])', content)
    # Filter out patterns inside guide quotes or code blocks
    script_blocks = '\n'.join(scripts)
    formal_in_scripts = re.findall(r'(?<![가-힣])(이다[.\s,]|한다[.\s,])', script_blocks)
    polite_count = count_pattern(script_blocks, r'입니다|합니다|됩니다|겠습니다|보십시오|보시면|하시면')
    results["expectations"].append({
        "text": f"구어체: 존댓말 패턴 {polite_count}개, 문어체 패턴 {len(formal_in_scripts)}개",
        "passed": polite_count > 20 and len(formal_in_scripts) < 5,
        "evidence": f"Polite: {polite_count}, Formal: {len(formal_in_scripts)}"
    })

    # 4. Q&A sections
    qa_count = count_pattern(content, r'\[Q&A 대비\]')
    q_count = len(re.findall(r'^Q:', content, re.MULTILINE))
    results["expectations"].append({
        "text": f"Q&A 대비: [Q&A 대비] 섹션 {qa_count}개, 질문 {q_count}개",
        "passed": qa_count >= 3 and q_count >= 6,
        "evidence": f"Q&A sections: {qa_count}, Questions: {q_count}"
    })

    # 5. Time markers
    time_count = count_pattern(content, r'시간:\s*[\d.]+분')
    results["expectations"].append({
        "text": f"시간 산정: '시간:' 마커 {time_count}개",
        "passed": time_count >= 5,
        "evidence": f"Time markers: {time_count}"
    })

    # 6. Transition markers
    transition_count = count_pattern(content, r'전환:')
    results["expectations"].append({
        "text": f"전환 멘트: '전환:' 마커 {transition_count}개",
        "passed": transition_count >= 4,
        "evidence": f"Transition markers: {transition_count}"
    })

    return results


def grade_eval2(path, config_name):
    """Grade eval-2: code-slide-depth."""
    filepath = os.path.join(path, "outputs", "slide.md")
    if not os.path.exists(filepath):
        return {"error": f"File not found: {filepath}"}

    with open(filepath, "r") as f:
        content = f.read()

    scripts = extract_scripts(content)
    script_text = '\n'.join(scripts) if scripts else content

    results = {"config": config_name, "expectations": []}

    # 1. Line-by-line code explanation
    commands = ['mkdir', 'git init', 'git add', 'git status', 'git commit', 'git log']
    found_commands = [cmd for cmd in commands if cmd in script_text]
    results["expectations"].append({
        "text": f"줄 단위 해설: {len(found_commands)}/{len(commands)} 명령어 설명",
        "passed": len(found_commands) >= 5,
        "evidence": f"Found: {found_commands}, Missing: {[c for c in commands if c not in found_commands]}"
    })

    # 2. [click] count = 6
    click_count = count_pattern(content, r'\[click\]')
    results["expectations"].append({
        "text": f"[click] 정확도: {click_count}개 (목표: 6개)",
        "passed": click_count >= 5,  # allow slight variance
        "evidence": f"[click] count: {click_count}"
    })

    # 3. Confusion point marker
    confusion_count = count_pattern(content, r'💡')
    results["expectations"].append({
        "text": f"헷갈림 포인트: 💡 마커 {confusion_count}개",
        "passed": confusion_count >= 1,
        "evidence": f"💡 markers: {confusion_count}"
    })

    # 4. Q&A prep section
    qa_exists = '[Q&A 대비]' in content or 'Q&A' in content
    q_count = count_pattern(content, r'Q:')
    results["expectations"].append({
        "text": f"Q&A 대비: 존재={'예' if qa_exists else '아니오'}, 질문 {q_count}개",
        "passed": qa_exists and q_count >= 2,
        "evidence": f"Q&A section: {qa_exists}, Questions: {q_count}"
    })

    return results


def main():
    eval_dirs = [
        ("eval-1-mini-fixture", grade_eval1),
        ("eval-2-code-slide", grade_eval2),
    ]

    all_results = {}
    for eval_name, grade_fn in eval_dirs:
        for config in ["with_skill", "without_skill"]:
            path = os.path.join(BASE, eval_name, config)
            if os.path.exists(path):
                result = grade_fn(path, config)
                key = f"{eval_name}/{config}"
                all_results[key] = result

                # Save individual grading.json
                grading_path = os.path.join(path, "grading.json")
                with open(grading_path, "w") as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                print(f"✅ {key}: {sum(1 for e in result.get('expectations', []) if e.get('passed'))}/{len(result.get('expectations', []))} passed")

    # Summary
    print("\n=== SUMMARY ===")
    for key, result in all_results.items():
        if "expectations" in result:
            passed = sum(1 for e in result["expectations"] if e.get("passed"))
            total = len(result["expectations"])
            print(f"{key}: {passed}/{total} ({passed/total*100:.0f}%)")
        else:
            print(f"{key}: ERROR - {result.get('error', 'unknown')}")


if __name__ == "__main__":
    main()
