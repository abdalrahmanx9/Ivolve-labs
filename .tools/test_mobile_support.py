# test_mobile_support.py
"""
Single runnable check for mobile phone support in generated DevOps Labs Guide.
Tests required responsive breakpoints, drawer elements, and mobile styles.
"""
import os

def test_mobile_support():
    repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    guide_path = os.path.join(repo_root, "index.html")
    assert os.path.exists(guide_path), f"File {guide_path} not found"
    
    with open(guide_path, "r", encoding="utf-8") as f:
        html = f.read()

    # 1. Viewport meta tag
    assert '<meta name="viewport" content="width=device-width, initial-scale=1.0">' in html, "Missing viewport meta tag"

    # 2. Mobile drawer elements
    assert 'id="drawerBackdrop"' in html, "Missing #drawerBackdrop element"
    assert 'id="mobileNavBtn"' in html, "Missing #mobileNavBtn element"
    assert 'id="closeSidebarBtn"' in html, "Missing #closeSidebarBtn element"
    assert 'class="sidebar-header-mobile"' in html, "Missing .sidebar-header-mobile element"

    # 3. Mobile CSS breakpoints & responsive styles
    assert '@media (max-width: 1024px)' in html, "Missing tablet/mobile 1024px breakpoint"
    assert '@media (max-width: 640px)' in html, "Missing smartphone 640px breakpoint"
    assert 'transform: translateX(-100%);' in html, "Missing sidebar drawer offscreen transform"
    assert 'transform: rotate(90deg);' in html, "Missing vertical flow arrow rotation for mobile"
    assert '-webkit-overflow-scrolling: touch;' in html, "Missing touch scrolling optimization"
    assert 'grid-template-columns: repeat(2, 1fr);' in html, "Missing 2-column stats grid for mobile"

    # 4. Mobile Drawer JavaScript controls
    assert 'openMobileDrawer' in html, "Missing openMobileDrawer function in script"
    assert 'closeMobileDrawer' in html, "Missing closeMobileDrawer function in script"
    assert 'no-scroll' in html, "Missing body no-scroll lock toggle"

    # 5. Symbol-only mobile button (no text span inside mobileNavBtn)
    import re
    nav_btn_match = re.search(r'<button id="mobileNavBtn"[^>]*>(.*?)</button>', html, re.DOTALL)
    assert nav_btn_match, "Cannot find mobileNavBtn"
    nav_btn_content = nav_btn_match.group(1).strip()
    assert '<span' not in nav_btn_content, "mobileNavBtn must be symbol only (found span)"
    assert '<svg' in nav_btn_content, "mobileNavBtn must contain SVG symbol"

    # 6. Stationary copy button wrapper (prevents sliding on horizontal scroll)
    assert '.code-block-wrapper' in html, "Missing .code-block-wrapper in CSS/JS"
    assert 'wrapper.appendChild(copyBtn)' in html, "Copy button must attach to non-scrolling wrapper"

    # 7. Column Synchronization & Scrollspy
    assert 'syncSidebarScroll' in html, "Missing syncSidebarScroll in JS"
    assert 'syncColumns' in html, "Missing syncColumns in JS"
    assert 'getActiveLab' in html, "Missing getActiveLab in JS"

    # 8. Reading State Persistence & Resume Toast
    assert 'devops_guide_last_lab' in html, "Missing localStorage key for reading persistence"
    assert 'restoreReadingPosition' in html, "Missing restoreReadingPosition in JS"
    assert 'id="resumeToast"' in html, "Missing #resumeToast in HTML"
    assert '.resume-toast' in html, "Missing .resume-toast in CSS"

    print("ALL MOBILE SUPPORT & SYNC TESTS PASSED! (100% verified)")

if __name__ == "__main__":
    test_mobile_support()

