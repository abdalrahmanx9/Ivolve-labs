# build_html_guide.py
import sys
import os
import re
from html.parser import HTMLParser

# Add generator directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "generator"))

from module1_buildtools import LABS_MODULE_1
from module2_docker import LABS_MODULE_2
from module3_kubernetes import LABS_MODULE_3
from module4_jenkins import LABS_MODULE_4
from module5_gitops import LABS_MODULE_5
from module6_ansible import LABS_MODULE_6
from template import get_html_template

def sanitize_html(html_str):
    # 1. Fix bash heredocs: <<EOF -> &lt;&lt;EOF
    html_str = html_str.replace("<<EOF", "&lt;&lt;EOF")
    
    # 2. Fix arrows: <- -> &lt;-
    html_str = html_str.replace("<-", "&lt;-")
    
    # 3. Fix unescaped placeholders that look like tags
    placeholders = [
        '<node_IP>', '<CONTROL_PLANE_IP>', '<MASTER_IP>', '<TOKEN>', '<HASH>',
        '<password>', '<GIT_USER>', '<GIT_PASS>', '<YOUR_KEY>', '<YOUR_SECRET>',
        '<K8S_URL>', '<token>', '<hash>', '<control-plane-ip>', '<managed_node_ip>',
        '<your-account>', '<vault_password>', '<ansible_controller_ip>', '<subnet-id>', '<security-group-id>'
    ]
    for p in placeholders:
        esc = p.replace('<', '&lt;').replace('>', '&gt;')
        html_str = html_str.replace(p, esc)
        
    return html_str

class StrictHTMLValidator(HTMLParser):
    def __init__(self):
        super().__init__()
        self.tags = []
        self.void_tags = {'meta', 'link', 'img', 'br', 'hr', 'input', 'circle', 'line', 'polyline'}
        self.errors = []

    def handle_starttag(self, tag, attrs):
        if tag not in self.void_tags:
            self.tags.append((tag, self.getpos()))

    def handle_endtag(self, tag):
        if tag in self.void_tags:
            return
        if not self.tags:
            self.errors.append(f"Unexpected closing tag </{tag}> at {self.getpos()}")
            return
        last_tag, pos = self.tags.pop()
        if last_tag != tag:
            self.errors.append(f"Mismatched tag: opened <{last_tag}> at {pos}, closed </{tag}> at {self.getpos()}")

def main():
    print("Aggregating all labs across all 6 modules...")
    all_labs = (
        LABS_MODULE_1 +
        LABS_MODULE_2 +
        LABS_MODULE_3 +
        LABS_MODULE_4 +
        LABS_MODULE_5 +
        LABS_MODULE_6
    )

    print(f"Total labs assembled: {len(all_labs)}")
    assert len(all_labs) == 28, f"Expected 28 labs, got {len(all_labs)}"

    print("Generating comprehensive HTML document...")
    html_content = get_html_template(all_labs)
    html_content = sanitize_html(html_content)

    print("Validating HTML syntax tree...")
    validator = StrictHTMLValidator()
    validator.feed(html_content)

    if validator.errors or validator.tags:
        print(f"Validation FAILED! Found {len(validator.errors)} tag errors, {len(validator.tags)} unclosed tags:")
        for err in validator.errors:
            print("  [ERROR]", err)
        for t, p in validator.tags:
            print(f"  [UNCLOSED] <{t}> at {p}")
        sys.exit(1)
    else:
        print("HTML validation PASSED! 100% compliant, 0 tag mismatches, 0 unclosed tags.")

    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    index_path = os.path.join(repo_root, "index.html")

    with open(index_path, "w", encoding="utf-8") as f:
        f.write(html_content)
    print(f"Successfully generated: {index_path} ({os.path.getsize(index_path):,} bytes)")

if __name__ == "__main__":
    main()
