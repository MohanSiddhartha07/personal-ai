from pathlib import Path


DATA_DIR = Path("data")


def load_personal_context():
    files = [
        "profile.md",
        "resume.md",
        "projects.md",
        "interviews.md",
        "learning.md",
    ]

    context_parts = []

    for filename in files:
        file_path = DATA_DIR / filename

        if file_path.exists():
            content = file_path.read_text(encoding="utf-8")

            context_parts.append(
                f"""
===== {filename} =====

{content}
"""
            )

    return "\n".join(context_parts)