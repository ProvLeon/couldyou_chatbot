# from utils import escape_markdown_v2
def escape_markdown_v2(text):
    escape_chars = r"_~`>#+-=|{}.!"
    return ''.join(['\\' + char if char in escape_chars else char for char in text])

def test_escape_markdown():
    test_cases = [
        "Hello * World",
        "Test_with_underscore",
        "Numbers: 1.23!",
        "**Bold Text**",
        "*Italic Text*",
        "- Bullet point"
    ]

    print("\nTesting Markdown escaping:")
    print("=" * 50)

    for test in test_cases:
        print(f"\nTest case: {test}")
        escaped = escape_markdown_v2(test)
        print(f"Escaped result: {escaped}")
        print("-" * 50)

if __name__ == "__main__":
    test_escape_markdown()
