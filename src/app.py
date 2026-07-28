"""
🚀 CORE AGENT APP (Role 4: Core Developer / Integrator)

Trạng thái hiện tại: Mốc 2 — Chatbot Baseline.
Phần ReAct Agent Loop sẽ được tích hợp ở Mốc 3 sau khi Role 2 và Role 3
hoàn thiện tool contract, ReAct prompt và guardrails.
"""

import json
import os
import sys

from dotenv import load_dotenv


SRC_DIR = os.path.dirname(os.path.abspath(__file__))
if SRC_DIR not in sys.path:
    sys.path.append(SRC_DIR)

if sys.stdout.encoding != "utf-8":
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

from prompts import CHATBOT_BASELINE_PROMPT
from providers import get_llm_provider

load_dotenv()


def load_test_cases():
    """Đọc bộ test cases do Role 1 quản lý từ config/test_cases.json."""
    config_path = os.path.join(os.path.dirname(SRC_DIR), "config", "test_cases.json")
    with open(config_path, "r", encoding="utf-8") as file:
        return json.load(file)


def run_baseline_chatbot(user_query: str, provider):
    """Chạy đúng một LLM call, tuyệt đối không đăng ký hoặc gọi tool."""
    print(f"\n💬 [CHATBOT BASELINE] Câu hỏi: {user_query}")
    response = provider.generate(user_query, system_prompt=CHATBOT_BASELINE_PROMPT).strip()
    print(f"🤖 Chatbot trả lời:\n{response}")
    return {"answer": response, "tool_calls": 0}


def run_baseline_evaluation(test_cases, provider):
    """Chạy baseline trên toàn bộ bộ đề để Role 5 lưu và đánh giá output."""
    for test_case in test_cases:
        print("\n" + "=" * 50)
        print(f"TEST CASE #{test_case['id']}: {test_case['category']}")
        print(f"Kỳ vọng: {test_case['expected_behavior']}")
        run_baseline_chatbot(test_case["question"], provider)


if __name__ == "__main__":
    print("=" * 50)
    print("🏫 ĐẠI HỌC VINUNI - BÀI LAB 3: CHATBOT VS REACT AGENT")
    print("=" * 50)

    provider = get_llm_provider()
    model_name = getattr(provider, "model_name", "Offline Mock Mode")
    print(f"🔌 LLM Provider đang hoạt động: {provider.__class__.__name__} (Model: {model_name})")

    tests = load_test_cases()
    print(f"✅ Đã tải thành công {len(tests)} Test Cases từ config/test_cases.json")
    print("\n--- MỐC 2: CHẠY CHATBOT BASELINE TRÊN TOÀN BỘ TEST CASES ---")
    run_baseline_evaluation(tests, provider)
