import re

css_path = r'c:\Users\VASANTHI\OneDrive\Desktop\AP Invoice\frontend\styles.css'
with open(css_path, 'r', encoding='utf-8') as f:
    css = f.read()

# Replace fonts
css = re.sub(r"@import url\('.*?'\);", r"@import url('https://fonts.googleapis.com/css2?family=Open+Sans:wght@300;400;500;600;700&family=Poppins:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');", css)

# Replace variables in :root
root_vars = """
  /* Color Palette */
  --bg-primary: #F8FAFC;
  --bg-secondary: #F1F3F5;
  --bg-tertiary: #E4E7EB;
  --bg-card: #FFFFFF;
  --bg-glass: rgba(0, 0, 0, 0.04);
  --bg-glass-hover: rgba(0, 0, 0, 0.08);
  --bg-input: #FFFFFF;

  --border-subtle: #E4E7EB;
  --border-medium: #CBD5E1;
  --border-focus: rgba(37, 99, 235, 0.5);

  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-tertiary: #64748b;
  --text-inverse: #FFFFFF;

  --accent-indigo: #1E3A5F;
  --accent-indigo-light: #2563EB;
  --accent-indigo-glow: rgba(37, 99, 235, 0.15);
  --accent-violet: #1E3A5F;
  --accent-cyan: #0284C7;
  --accent-emerald: #059669;
  --accent-amber: #D97706;
  --accent-rose: #DC2626;

  --severity-high: #DC2626;
  --severity-high-bg: rgba(220, 38, 38, 0.12);
  --severity-medium: #D97706;
  --severity-medium-bg: rgba(217, 119, 6, 0.12);
  --severity-low: #0284C7;
  --severity-low-bg: rgba(2, 132, 199, 0.12);

  --success: #059669;
  --success-bg: rgba(5, 150, 105, 0.12);

  /* Typography */
  --font-sans: 'Open Sans', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-heading: 'Poppins', -apple-system, BlinkMacSystemFont, sans-serif;
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;

  /* Spacing */
  --space-xs: 4px;
  --space-sm: 8px;
  --space-md: 16px;
  --space-lg: 24px;
  --space-xl: 32px;
  --space-2xl: 48px;

  /* Borders */
  --radius-sm: 4px;
  --radius-md: 6px;
  --radius-lg: 8px;
  --radius-xl: 12px;
  --radius-full: 9999px;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-glow: 0 0 10px rgba(37, 99, 235, 0.1);

  /* Transitions */
  --transition-fast: 150ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-base: 250ms cubic-bezier(0.4, 0, 0.2, 1);
  --transition-slow: 400ms cubic-bezier(0.4, 0, 0.2, 1);
"""

# Replace all variables in :root
css = re.sub(r":root\s*\{[^}]+\}", f":root {{{root_vars}}}", css, count=1)

# Modify h1, h2, h3, h4
css = re.sub(r"(h1,\s*h2,\s*h3,\s*h4\s*\{)([^}]+)\}", r"\1\n  font-family: var(--font-heading);\2", css)

# Remove background gradient
css = re.sub(r"body::before\s*\{[^}]+\}", "", css)

# Remove backdrop-filter
css = re.sub(r"backdrop-filter:\s*[^;]+;", "", css)
css = re.sub(r"-webkit-backdrop-filter:\s*[^;]+;", "", css)

# Fix loading overlay background
css = re.sub(r"background:\s*rgba\(10,\s*14,\s*26,\s*0\.85\);", "background: rgba(248, 250, 252, 0.85);", css)

# Fix app-header styling
css = re.sub(r"background:\s*linear-gradient\(135deg,\s*var\(--text-primary\),\s*var\(--accent-indigo-light\)\);[\s\n]*-webkit-background-clip:\s*text;[\s\n]*-webkit-text-fill-color:\s*transparent;[\s\n]*background-clip:\s*text;", "color: var(--text-primary);", css)
css = re.sub(r"background:\s*linear-gradient\(135deg,\s*var\(--accent-indigo\),\s*var\(--accent-violet\)\);", "background: var(--accent-indigo);", css)

# Fix loading overlay text
css = css.replace("color: white;", "color: var(--text-inverse);")
css = css.replace("color: #FFFFFF;", "color: var(--text-inverse);")

with open(css_path, 'w', encoding='utf-8') as f:
    f.write(css)

print("Updated styles.css successfully!")
