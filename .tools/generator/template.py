# generator/template.py
import html

def get_html_template(labs_data):
    total_labs = len(labs_data)
    
    # Generate TOC items
    toc_html = ""
    for lab in labs_data:
        toc_html += f"""
        <a href="#{lab['id']}" class="toc-link" data-module="{lab['module']}" data-lab-id="{lab['id']}">
            <span class="toc-num">{lab['number']}</span>
            <span class="toc-title">{lab['title']}</span>
        </a>
        """

    # Generate Lab Cards
    labs_html = ""
    for lab in labs_data:
        tags_badges = "".join([f'<span class="tag-badge">{t}</span>' for t in lab["tags"]])
        
        # Build question list with proper HTML escaping
        questions_html = ""
        for q in lab.get("question", []):
            questions_html += f"<li>{html.escape(q)}</li>"

        labs_html += f"""
        <section id="{lab['id']}" class="lab-card" data-module="{lab['module']}">
            <div class="lab-card-header">
                <div class="header-left">
                    <span class="lab-badge">{lab['number']}</span>
                    <span class="module-badge module-{lab['module'].lower().replace(' ', '-').replace('/', '-')}">{lab['module']}</span>
                    <h2 class="lab-title">{lab['icon']} {lab['title']}</h2>
                </div>
                <div class="header-actions">
                    <button class="toggle-card-btn" aria-label="Toggle section">
                        <svg class="chevron-icon" viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none">
                            <polyline points="6 9 12 15 18 9"></polyline>
                        </svg>
                    </button>
                </div>
            </div>

            <div class="lab-card-summary">
                <p class="summary-text"><strong>Objective:</strong> {lab['summary']}</p>
                <div class="tags-container">{tags_badges}</div>
            </div>

            <div class="lab-card-body">
                <!-- Lab Prompt / Questions -->
                <div class="lab-question-box">
                    <div class="question-header">
                        <span class="q-icon">📋</span>
                        <strong>Lab Prompt & Requirements (Slide Task)</strong>
                    </div>
                    <ul class="question-list">
                        {questions_html}
                    </ul>
                </div>

                <!-- Core Concepts -->
                <div class="section-block concept-block">
                    {lab['concept']}
                </div>

                <!-- Visual Workflow Diagram -->
                <div class="section-block diagram-block">
                    <h4>Architecture & Workflow Flowchart</h4>
                    {lab.get('diagram_html', '')}
                </div>

                <!-- Solving & Manifests -->
                <div class="section-block solving-block">
                    {lab['solving']}
                </div>

                <!-- Tips -->
                <div class="section-block tips-block">
                    {lab['tips']}
                </div>
            </div>
        </section>
        """

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>DevOps Labs Guide — Complete Solutions (Labs 1-28) | NTI & iVolve</title>
    <meta name="description" content="Complete practical guide for all 28 NTI & iVolve DevOps Accelerator Labs: Maven, Gradle, Docker, Kubernetes (Kubeadm, Calico), Jenkins CI/CD, GitOps (Argo CD), and Ansible Automation.">
    <meta name="keywords" content="DevOps, NTI, iVolve, Kubernetes, Kubeadm, Calico CNI, Docker, Docker Compose, Jenkins CI CD, Argo CD, GitOps, Ansible, Maven, Gradle, Trivy, Linux">
    <meta name="author" content="Abdalrahman">
    <meta name="robots" content="index, follow">
    <link rel="canonical" href="https://abdalrahmanx9.github.io/Ivolve-labs/">

    <!-- Open Graph / Social Media -->
    <meta property="og:type" content="website">
    <meta property="og:url" content="https://abdalrahmanx9.github.io/Ivolve-labs/">
    <meta property="og:title" content="NTI & iVolve DevOps Accelerator Labs — Complete 1 to 28 Solutions">
    <meta property="og:description" content="Step-by-step hands-on solutions, commands, and architecture diagrams for Maven, Gradle, Docker, Kubernetes, Jenkins CI/CD, Argo CD GitOps, and Ansible Automation.">
    <meta property="og:site_name" content="iVolve DevOps Accelerator">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary">
    <meta name="twitter:title" content="NTI & iVolve DevOps Accelerator Labs — Complete Guide">
    <meta name="twitter:description" content="Complete solutions for all 28 DevOps labs: Docker, Kubernetes, Jenkins, GitOps (Argo CD), Ansible, Maven, and Gradle.">

    <!-- Schema.org JSON-LD Structured Data for Search Engines -->
    <script type="application/ld+json">
    {{
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": "DevOps Accelerator Labs - Complete Solutions (Labs 1-28)",
        "description": "Comprehensive practical solutions, architecture diagrams, and commands for NTI and iVolve Cloud DevOps Accelerator training.",
        "url": "https://abdalrahmanx9.github.io/Ivolve-labs/",
        "author": {{
            "@type": "Person",
            "name": "Abdalrahman"
        }},
        "about": [
            "DevOps", "Docker", "Kubernetes", "Jenkins", "GitOps", "Argo CD", "Ansible", "Maven", "Gradle"
        ]
    }}
    </script>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Fira+Code:wght@400;500;600&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet">
    
    <!-- Prism.js Syntax Highlighting for Colorful Command Lines & Manifests -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/themes/prism-tomorrow.min.css">

    <style>
        :root {{
            --bg-body: #090d16;
            --bg-surface: #0f172a;
            --bg-card: #131d31;
            --bg-card-hover: #17233c;
            --bg-code: #0b1120;
            --border-color: #1e293b;
            --border-accent: #334155;
            --text-main: #f1f5f9;
            --text-muted: #94a3b8;
            --text-dim: #64748b;
            --accent-primary: #38bdf8;
            --accent-secondary: #818cf8;
            --accent-success: #34d399;
            --accent-warning: #fbbf24;
            --accent-danger: #f43f5e;
            --radius-sm: 6px;
            --radius-md: 10px;
            --radius-lg: 16px;
            --shadow-sm: 0 2px 4px rgba(0, 0, 0, 0.4);
            --shadow-md: 0 4px 12px rgba(0, 0, 0, 0.5);
            --shadow-lg: 0 10px 25px rgba(0, 0, 0, 0.6);
            --transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1);
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
            background-color: var(--bg-body);
            color: var(--text-main);
            line-height: 1.6;
            font-size: 15px;
            overflow-x: hidden;
        }}

        /* Centered Header / Hero */
        .hero-banner {{
            background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #090d16 100%);
            border-bottom: 1px solid var(--border-color);
            padding: 36px 20px;
            position: relative;
            overflow: hidden;
        }}
        .hero-banner::before {{
            content: "";
            position: absolute;
            top: -50%;
            left: -20%;
            width: 140%;
            height: 200%;
            background: radial-gradient(circle, rgba(56, 189, 248, 0.08) 0%, transparent 60%);
            pointer-events: none;
        }}
        .hero-container {{
            max-width: 1300px;
            margin: 0 auto;
            position: relative;
            z-index: 1;
        }}
        .badge-row {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
            margin-bottom: 14px;
        }}
        .program-badge {{
            background: rgba(56, 189, 248, 0.15);
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: var(--accent-primary);
            font-size: 12px;
            font-weight: 700;
            letter-spacing: 0.04em;
            padding: 4px 12px;
            border-radius: 9999px;
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .status-badge {{
            background: rgba(52, 211, 153, 0.15);
            border: 1px solid rgba(52, 211, 153, 0.4);
            color: var(--accent-success);
            font-size: 12px;
            font-weight: 700;
            padding: 4px 12px;
            border-radius: 9999px;
        }}
        .hero-title {{
            font-size: 30px;
            font-weight: 800;
            color: #ffffff;
            margin-bottom: 8px;
            line-height: 1.3;
        }}
        .hero-subtitle {{
            font-size: 15px;
            color: var(--text-muted);
            max-width: 960px;
            line-height: 1.6;
            margin-bottom: 20px;
        }}
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
        }}
        .stat-card {{
            background: rgba(15, 23, 42, 0.7);
            border: 1px solid var(--border-color);
            padding: 14px 18px;
            border-radius: var(--radius-md);
            backdrop-filter: blur(8px);
        }}
        .stat-val {{
            font-size: 24px;
            font-weight: 800;
            color: var(--accent-primary);
            display: block;
        }}
        .stat-label {{
            font-size: 12px;
            color: var(--text-muted);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            font-weight: 600;
        }}

        /* Centered App Layout */
        .app-layout {{
            display: flex;
            justify-content: center;
            max-width: 1300px;
            margin: 0 auto;
            padding: 24px 20px 80px;
            gap: 32px;
            position: relative;
        }}

        /* Sticky Sidebar TOC */
        .sidebar {{
            width: 300px;
            min-width: 300px;
            position: sticky;
            top: 24px;
            height: calc(100vh - 48px);
            overflow: hidden;
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            padding: 20px 16px 14px;
            display: flex;
            flex-direction: column;
            gap: 14px;
            box-shadow: var(--shadow-sm);
        }}
        .sidebar::-webkit-scrollbar {{
            width: 5px;
        }}
        .sidebar::-webkit-scrollbar-thumb {{
            background: var(--border-accent);
            border-radius: 3px;
        }}
        .search-box {{
            position: relative;
        }}
        .search-input {{
            width: 100%;
            background: var(--bg-code);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-sm);
            color: var(--text-main);
            padding: 9px 12px 9px 34px;
            font-size: 13px;
            outline: none;
            transition: var(--transition);
        }}
        .search-input:focus {{
            border-color: var(--accent-primary);
            box-shadow: 0 0 0 2px rgba(56, 189, 248, 0.2);
        }}
        .search-icon {{
            position: absolute;
            left: 10px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-dim);
            pointer-events: none;
        }}
        .module-filters {{
            display: flex;
            flex-wrap: wrap;
            gap: 5px;
        }}
        .filter-btn {{
            background: var(--bg-code);
            border: 1px solid var(--border-color);
            color: var(--text-muted);
            padding: 4px 9px;
            border-radius: 9999px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
        }}
        .filter-btn:hover, .filter-btn.active {{
            background: var(--accent-primary);
            color: #090d16;
            border-color: var(--accent-primary);
        }}
        .toc-list {{
            display: flex;
            flex-direction: column;
            gap: 2px;
            flex: 1;
            overflow-y: auto;
            padding-right: 4px;
            scroll-behavior: smooth;
        }}
        .toc-list::-webkit-scrollbar {{
            width: 4px;
        }}
        .toc-list::-webkit-scrollbar-thumb {{
            background: var(--border-accent);
            border-radius: 2px;
        }}
        .toc-link {{
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 7px 10px;
            border-radius: var(--radius-sm);
            color: var(--text-muted);
            text-decoration: none;
            font-size: 12.5px;
            transition: var(--transition);
            line-height: 1.3;
        }}
        .toc-link:hover {{
            background: rgba(255, 255, 255, 0.05);
            color: var(--text-main);
        }}
        .toc-link.active {{
            background: rgba(56, 189, 248, 0.12);
            color: var(--accent-primary);
            font-weight: 600;
            border-left: 3px solid var(--accent-primary);
        }}
        .toc-num {{
            font-family: 'Fira Code', monospace;
            font-size: 11px;
            font-weight: 700;
            color: var(--text-dim);
            min-width: 44px;
        }}

        /* Centered Main Content Area */
        .content-area {{
            flex: 1;
            max-width: 960px;
            width: 100%;
        }}
        .controls-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 20px;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }}
        .controls-info {{
            font-size: 14px;
            color: var(--text-muted);
        }}
        .global-toggle-btn {{
            background: var(--bg-surface);
            border: 1px solid var(--border-color);
            color: var(--text-main);
            padding: 7px 14px;
            border-radius: var(--radius-sm);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            display: inline-flex;
            align-items: center;
            gap: 6px;
        }}
        .global-toggle-btn:hover {{
            background: var(--border-color);
            border-color: var(--accent-primary);
        }}

        /* Lab Card */
        .lab-card {{
            background: var(--bg-card);
            border: 1px solid var(--border-color);
            border-radius: var(--radius-lg);
            margin-bottom: 28px;
            overflow: hidden;
            box-shadow: var(--shadow-md);
            transition: var(--transition);
        }}
        .lab-card:hover {{
            border-color: var(--border-accent);
        }}
        .lab-card-header {{
            background: var(--bg-surface);
            padding: 18px 24px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            cursor: pointer;
            user-select: none;
            transition: var(--transition);
        }}
        .lab-card-header:hover {{
            background: #152238;
        }}
        .lab-card.open .lab-card-header {{
            border-bottom: 1px solid var(--border-color);
        }}
        .header-left {{
            display: flex;
            align-items: center;
            gap: 12px;
            flex-wrap: wrap;
        }}
        .lab-badge {{
            background: #1e293b;
            color: #ffffff;
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            font-weight: 700;
            padding: 3px 8px;
            border-radius: 4px;
            border: 1px solid #334155;
        }}
        .module-badge {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            padding: 3px 8px;
            border-radius: 4px;
            letter-spacing: 0.05em;
        }}
        .module-build-tools {{ background: rgba(245, 158, 11, 0.15); color: #f59e0b; border: 1px solid rgba(245, 158, 11, 0.4); }}
        .module-docker {{ background: rgba(14, 165, 233, 0.15); color: #0ea5e9; border: 1px solid rgba(14, 165, 233, 0.4); }}
        .module-kubernetes {{ background: rgba(99, 102, 241, 0.15); color: #818cf8; border: 1px solid rgba(99, 102, 241, 0.4); }}
        .module-jenkins-ci-cd {{ background: rgba(244, 63, 94, 0.15); color: #f43f5e; border: 1px solid rgba(244, 63, 94, 0.4); }}
        .module-gitops {{ background: rgba(16, 185, 129, 0.15); color: #34d399; border: 1px solid rgba(16, 185, 129, 0.4); }}
        .module-ansible {{ background: rgba(217, 70, 239, 0.15); color: #d946ef; border: 1px solid rgba(217, 70, 239, 0.4); }}

        .lab-title {{
            font-size: 17px;
            font-weight: 700;
            color: #ffffff;
            margin: 0;
        }}
        .chevron-icon {{
            color: var(--text-dim);
            transition: transform 0.25s ease;
        }}
        .lab-card.open .chevron-icon {{
            transform: rotate(180deg);
            color: var(--accent-primary);
        }}
        .toggle-card-btn {{
            background: transparent;
            border: none;
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
        }}

        .lab-card-summary {{
            padding: 14px 24px;
            background: rgba(15, 23, 42, 0.35);
            border-bottom: 1px solid var(--border-color);
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .summary-text {{
            font-size: 14px;
            color: var(--text-muted);
        }}
        .tags-container {{
            display: flex;
            flex-wrap: wrap;
            gap: 6px;
        }}
        .tag-badge {{
            background: var(--bg-code);
            border: 1px solid var(--border-accent);
            color: var(--text-muted);
            font-size: 11px;
            padding: 2px 7px;
            border-radius: 4px;
            font-family: 'Fira Code', monospace;
        }}

        /* Lab Card Body */
        .lab-card-body {{
            display: none;
            padding: 24px 24px 32px;
        }}
        .lab-card.open .lab-card-body {{
            display: block;
        }}

        /* Lab Question Box */
        .lab-question-box {{
            background: rgba(30, 41, 59, 0.4);
            border: 1px solid #334155;
            border-left: 4px solid var(--accent-primary);
            border-radius: var(--radius-sm);
            padding: 16px 20px;
            margin-bottom: 24px;
        }}
        .question-header {{
            display: flex;
            align-items: center;
            gap: 8px;
            font-size: 14px;
            color: #ffffff;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        .question-list {{
            margin-left: 20px;
            color: #cbd5e1;
            font-size: 13.5px;
            line-height: 1.6;
        }}
        .question-list li {{
            margin-bottom: 4px;
        }}

        /* Section Blocks */
        .section-block {{
            margin-bottom: 26px;
        }}
        .section-block:last-child {{
            margin-bottom: 0;
        }}
        .section-block h4 {{
            font-size: 15px;
            font-weight: 700;
            color: var(--accent-primary);
            margin-bottom: 12px;
            display: flex;
            align-items: center;
            gap: 8px;
            border-bottom: 1px solid rgba(56, 189, 248, 0.2);
            padding-bottom: 5px;
        }}
        .section-block h5 {{
            font-size: 14px;
            font-weight: 600;
            color: #ffffff;
            margin: 18px 0 8px;
        }}
        .section-block p {{
            margin-bottom: 12px;
            color: #cbd5e1;
            font-size: 14px;
        }}
        .section-block ul, .section-block ol {{
            margin-left: 20px;
            margin-bottom: 14px;
            color: #cbd5e1;
            font-size: 14px;
        }}
        .section-block li {{
            margin-bottom: 5px;
        }}

        /* Visual Flow Diagram Nodes */
        .visual-flow {{
            display: flex;
            align-items: center;
            flex-wrap: wrap;
            gap: 12px;
            background: #0b1120;
            border: 1px solid #1e293b;
            padding: 18px 20px;
            border-radius: var(--radius-md);
            margin: 12px 0 16px;
        }}
        .flow-node {{
            background: #17233c;
            border: 1px solid #334155;
            border-radius: 8px;
            padding: 10px 14px;
            display: flex;
            flex-direction: column;
            gap: 2px;
            min-width: 140px;
            text-align: center;
            box-shadow: 0 2px 5px rgba(0,0,0,0.3);
        }}
        .flow-node.highlight {{
            border-color: var(--accent-primary);
            background: rgba(56, 189, 248, 0.1);
        }}
        .flow-node.success {{
            border-color: var(--accent-success);
            background: rgba(52, 211, 153, 0.1);
        }}
        .flow-node.danger {{
            border-color: var(--accent-danger);
            background: rgba(244, 63, 94, 0.1);
        }}
        .node-step {{
            font-size: 10px;
            font-weight: 700;
            text-transform: uppercase;
            color: var(--accent-primary);
            letter-spacing: 0.05em;
        }}
        .node-title {{
            font-size: 13px;
            font-weight: 700;
            color: #ffffff;
        }}
        .node-sub {{
            font-size: 11px;
            color: var(--text-muted);
        }}
        .flow-arrow {{
            color: var(--accent-primary);
            font-size: 14px;
            font-weight: 700;
        }}

        /* Comparison Cards */
        .visual-comparison {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
            gap: 16px;
            margin: 12px 0 16px;
        }}
        .comparison-card {{
            background: #0b1120;
            border: 1px solid #1e293b;
            border-radius: var(--radius-md);
            padding: 16px;
            display: flex;
            flex-direction: column;
            gap: 8px;
        }}
        .comp-badge {{
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            background: rgba(56, 189, 248, 0.15);
            color: var(--accent-primary);
            padding: 3px 8px;
            border-radius: 4px;
            align-self: flex-start;
        }}
        .comp-badge.success {{
            background: rgba(52, 211, 153, 0.15);
            color: var(--accent-success);
        }}
        .comp-badge.danger {{
            background: rgba(244, 63, 94, 0.15);
            color: var(--accent-danger);
        }}
        .comp-flow {{
            font-size: 13px;
            font-weight: 600;
            color: #ffffff;
        }}
        .comp-metric {{
            font-size: 13px;
            font-weight: 700;
        }}
        .comp-metric.danger {{ color: var(--accent-danger); }}
        .comp-metric.success {{ color: var(--accent-success); }}
        .comp-note {{
            font-size: 12px;
            color: var(--text-muted);
            line-height: 1.4;
        }}

        /* Clickable File Link Pills */
        .file-links-bar {{
            display: flex;
            flex-wrap: wrap;
            gap: 10px;
            margin: 12px 0 16px;
        }}
        .file-pill {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: #17233c;
            border: 1px solid rgba(56, 189, 248, 0.4);
            color: var(--accent-primary);
            padding: 7px 14px;
            border-radius: var(--radius-sm);
            text-decoration: none;
            font-size: 13px;
            font-weight: 600;
            transition: var(--transition);
        }}
        .file-pill:hover {{
            background: var(--accent-primary);
            color: #090d16;
            box-shadow: 0 0 10px rgba(56, 189, 248, 0.4);
        }}
        .pill-icon {{
            font-size: 14px;
        }}
        .pill-open {{
            font-size: 11px;
            opacity: 0.8;
            margin-left: 4px;
        }}

        /* Code Blocks & Terminal */
        .code-block-wrapper {{
            position: relative;
            margin: 10px 0 16px;
            width: 100%;
        }}
        .code-block-wrapper pre {{
            margin: 0 !important;
        }}
        pre {{
            position: relative;
            background: var(--bg-code) !important;
            border: 1px solid var(--border-accent) !important;
            border-radius: var(--radius-sm);
            padding: 28px 16px 16px;
            overflow-x: auto;
            font-family: 'Fira Code', Consolas, Monaco, monospace;
            font-size: 13px;
            line-height: 1.5;
            margin: 10px 0 16px;
            -webkit-overflow-scrolling: touch;
        }}
        code {{
            font-family: 'Fira Code', Consolas, Monaco, monospace;
            font-size: 13px;
        }}
        p code, li code {{
            background: rgba(30, 41, 59, 0.8);
            color: #38bdf8;
            padding: 2px 6px;
            border-radius: 4px;
            border: 1px solid #334155;
            font-size: 12px;
        }}
        .terminal-output {{
            background: #050811;
            border: 1px solid #1e293b;
            border-left: 3px solid #34d399;
            padding: 12px 16px;
            border-radius: var(--radius-sm);
            font-family: 'Fira Code', monospace;
            font-size: 12px;
            color: #a7f3d0;
            margin: 8px 0 16px;
            white-space: pre-wrap;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
        }}
        .copy-btn {{
            position: absolute;
            top: 6px;
            right: 8px;
            background: rgba(30, 41, 59, 0.9);
            border: 1px solid var(--border-accent);
            color: var(--text-muted);
            padding: 3px 8px;
            border-radius: 4px;
            font-size: 11px;
            font-weight: 600;
            cursor: pointer;
            transition: var(--transition);
            z-index: 10;
            backdrop-filter: blur(4px);
        }}
        .copy-btn:hover {{
            background: var(--accent-primary);
            color: #090d16;
            border-color: var(--accent-primary);
        }}
        .copy-btn.copied {{
            background: var(--accent-success);
            color: #090d16;
        }}

        /* Tips Block */
        .tips-block {{
            background: rgba(245, 158, 11, 0.05);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-left: 4px solid var(--accent-warning);
            padding: 16px 20px;
            border-radius: var(--radius-sm);
            margin-top: 24px;
        }}
        .tips-block h4 {{
            color: var(--accent-warning);
            border-bottom: none;
            padding-bottom: 0;
            margin-bottom: 8px;
        }}
        .tips-block ul {{
            margin-bottom: 0;
        }}

        /* Table */
        .table-container {{
            overflow-x: auto;
            margin: 14px 0 18px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            font-size: 13px;
            text-align: left;
        }}
        th, td {{
            padding: 10px 14px;
            border: 1px solid var(--border-color);
        }}
        th {{
            background: var(--bg-surface);
            color: #ffffff;
            font-weight: 700;
        }}
        tr:nth-child(even) {{
            background: rgba(15, 23, 42, 0.5);
        }}

        /* Back to top */
        .back-to-top {{
            position: fixed;
            bottom: 24px;
            right: 24px;
            background: var(--accent-primary);
            color: #090d16;
            width: 44px;
            height: 44px;
            border-radius: 50%;
            display: flex;
            align-items: center;
            justify-content: center;
            cursor: pointer;
            box-shadow: var(--shadow-lg);
            border: none;
            opacity: 0;
            visibility: hidden;
            transition: var(--transition);
            z-index: 100;
        }}
        .back-to-top.visible {{
            opacity: 1;
            visibility: visible;
        }}

        /* Mobile Drawer Backdrop Overlay */
        .drawer-backdrop {{
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: rgba(0, 0, 0, 0.7);
            backdrop-filter: blur(4px);
            z-index: 998;
            opacity: 0;
            visibility: hidden;
            transition: opacity 0.3s ease, visibility 0.3s ease;
        }}
        .drawer-backdrop.active {{
            opacity: 1;
            visibility: visible;
        }}

        /* Mobile Drawer Header */
        .sidebar-header-mobile {{
            display: none;
            align-items: center;
            justify-content: space-between;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--border-color);
        }}
        .sidebar-title {{
            font-size: 15px;
            font-weight: 700;
            color: #ffffff;
            display: flex;
            align-items: center;
            gap: 6px;
        }}
        .close-sidebar-btn {{
            background: #1e293b;
            border: 1px solid var(--border-accent);
            color: var(--text-muted);
            cursor: pointer;
            display: flex;
            align-items: center;
            justify-content: center;
            width: 32px;
            height: 32px;
            border-radius: var(--radius-sm);
            transition: var(--transition);
        }}
        .close-sidebar-btn:hover {{
            color: #ffffff;
            background: var(--accent-danger);
            border-color: var(--accent-danger);
        }}

        /* Mobile Floating Navigation Button (Symbol Only) */
        .mobile-nav-btn {{
            display: none;
            position: fixed;
            bottom: 24px;
            left: 20px;
            background: linear-gradient(135deg, #0284c7 0%, #38bdf8 100%);
            color: #090d16;
            border: 1px solid rgba(255, 255, 255, 0.2);
            width: 44px;
            height: 44px;
            border-radius: 50%;
            cursor: pointer;
            box-shadow: 0 4px 20px rgba(56, 189, 248, 0.45);
            z-index: 995;
            align-items: center;
            justify-content: center;
            padding: 0;
            transition: var(--transition);
        }}
        .mobile-nav-btn:hover {{
            transform: translateY(-2px);
            box-shadow: 0 6px 24px rgba(56, 189, 248, 0.6);
        }}
        .mobile-nav-btn:active {{
            transform: translateY(1px);
        }}

        body.no-scroll {{
            overflow: hidden;
        }}

        /* Resume Reading Toast Notification */
        .resume-toast {{
            position: fixed;
            bottom: 28px;
            right: 28px;
            background: #0f172a;
            border: 1px solid var(--accent-primary);
            border-radius: var(--radius-md);
            padding: 10px 16px;
            color: var(--text-main);
            font-size: 13px;
            display: flex;
            align-items: center;
            gap: 10px;
            box-shadow: 0 10px 25px -5px rgba(0, 0, 0, 0.6), 0 0 12px rgba(56, 189, 248, 0.2);
            z-index: 1000;
            opacity: 0;
            transform: translateY(20px);
            transition: transform 0.3s cubic-bezier(0.16, 1, 0.3, 1), opacity 0.3s ease;
            pointer-events: none;
        }}
        .resume-toast.show {{
            opacity: 1;
            transform: translateY(0);
            pointer-events: auto;
        }}
        .toast-icon {{
            color: var(--accent-primary);
            flex-shrink: 0;
        }}
        .toast-close {{
            background: transparent;
            border: none;
            color: var(--text-muted);
            cursor: pointer;
            padding: 2px;
            display: flex;
            align-items: center;
            border-radius: 4px;
            transition: var(--transition);
        }}
        .toast-close:hover {{
            color: #ffffff;
            background: rgba(255, 255, 255, 0.1);
        }}

        /* Responsive Layout for Tablets & Mobile Screens */
        @media (max-width: 1024px) {{
            .app-layout {{
                flex-direction: column;
                align-items: center;
                padding: 18px 16px 100px;
                gap: 16px;
            }}
            .content-area {{
                max-width: 100%;
                padding: 0;
            }}
            /* Turn sidebar into a slide-out drawer on tablets & mobile */
            .sidebar {{
                position: fixed;
                top: 0;
                left: 0;
                bottom: 0;
                width: 320px;
                max-width: 86vw;
                height: 100vh;
                z-index: 1000;
                transform: translateX(-100%);
                transition: transform 0.3s cubic-bezier(0.4, 0, 0.2, 1);
                border-radius: 0;
                border-top: none;
                border-bottom: none;
                border-left: none;
                box-shadow: 8px 0 30px rgba(0, 0, 0, 0.7);
                background: #0f172a;
                padding: 18px 14px;
            }}
            .sidebar.open {{
                transform: translateX(0);
            }}
            .mobile-nav-btn {{
                display: flex;
            }}
            .sidebar-header-mobile {{
                display: flex;
            }}
        }}

        /* Responsive Phone Optimization (iPhone, Android) */
        @media (max-width: 640px) {{
            .hero-banner {{
                padding: 22px 14px;
            }}
            .badge-row {{
                gap: 6px;
                margin-bottom: 10px;
            }}
            .program-badge, .status-badge {{
                font-size: 11px;
                padding: 3px 8px;
            }}
            .hero-title {{
                font-size: 21px;
                line-height: 1.3;
            }}
            .hero-subtitle {{
                font-size: 13.5px;
                line-height: 1.5;
                margin-bottom: 16px;
            }}
            .stats-grid {{
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
            }}
            .stat-card {{
                padding: 10px 12px;
            }}
            .stat-val {{
                font-size: 20px;
            }}
            .stat-label {{
                font-size: 10.5px;
            }}
            .controls-bar {{
                flex-direction: column;
                align-items: stretch;
                gap: 10px;
                margin-bottom: 16px;
            }}
            .global-toggle-btn {{
                justify-content: center;
                width: 100%;
                padding: 9px 12px;
            }}
            .lab-card {{
                border-radius: var(--radius-md);
                margin-bottom: 18px;
            }}
            .lab-card-header {{
                padding: 12px 14px;
            }}
            .header-left {{
                gap: 8px;
            }}
            .lab-badge {{
                font-size: 11px;
                padding: 2px 6px;
            }}
            .module-badge {{
                font-size: 10px;
                padding: 2px 6px;
            }}
            .lab-title {{
                font-size: 15px;
                line-height: 1.35;
                width: 100%;
                margin-top: 2px;
            }}
            .lab-card-summary {{
                padding: 10px 14px;
            }}
            .summary-text {{
                font-size: 13px;
                line-height: 1.45;
                word-break: break-word;
            }}
            .tag-badge {{
                font-size: 10px;
                padding: 2px 5px;
            }}
            .lab-card-body {{
                padding: 16px 12px 22px;
            }}
            .lab-question-box {{
                padding: 12px 12px;
                margin-bottom: 18px;
            }}
            .question-header {{
                font-size: 13px;
            }}
            .question-list {{
                margin-left: 14px;
                font-size: 12.5px;
            }}
            .section-block {{
                margin-bottom: 20px;
            }}
            .section-block h4 {{
                font-size: 14px;
            }}
            .section-block h5 {{
                font-size: 13px;
            }}
            .section-block p, .section-block ul, .section-block ol {{
                font-size: 13.5px;
                word-break: break-word;
            }}
            .section-block ul, .section-block ol {{
                margin-left: 16px;
            }}
            /* Flow diagrams responsive layout */
            .visual-flow {{
                flex-direction: column;
                align-items: stretch;
                padding: 14px 12px;
                gap: 6px;
            }}
            .flow-node {{
                width: 100%;
                min-width: unset;
                padding: 8px 12px;
            }}
            .flow-arrow {{
                transform: rotate(90deg);
                align-self: center;
                margin: 2px 0;
                font-size: 16px;
            }}
            .visual-comparison {{
                grid-template-columns: 1fr;
                gap: 10px;
            }}
            /* Code blocks and pre touch optimization */
            pre {{
                padding: 28px 12px 12px !important;
                font-size: 12px;
                border-radius: 4px;
                -webkit-overflow-scrolling: touch;
            }}
            code {{
                font-size: 12px;
            }}
            .copy-btn {{
                padding: 3px 7px;
                font-size: 10px;
                top: 6px;
                right: 6px;
            }}
            .terminal-output {{
                font-size: 11px;
                padding: 8px 10px;
                -webkit-overflow-scrolling: touch;
            }}
            .file-links-bar {{
                gap: 6px;
            }}
            .file-pill {{
                font-size: 12px;
                padding: 6px 10px;
                width: 100%;
                justify-content: space-between;
                word-break: break-all;
                white-space: normal;
            }}
            .tips-block {{
                padding: 12px 12px;
            }}
            .table-container {{
                -webkit-overflow-scrolling: touch;
            }}
            table {{
                font-size: 12px;
            }}
            th, td {{
                padding: 8px 10px;
            }}
            .back-to-top {{
                bottom: 20px;
                right: 14px;
                width: 40px;
                height: 40px;
            }}
            .mobile-nav-btn {{
                bottom: 20px;
                left: 14px;
                width: 40px;
                height: 40px;
                padding: 0;
            }}
            .resume-toast {{
                bottom: 74px;
                left: 14px;
                right: 14px;
                font-size: 12px;
                padding: 8px 12px;
            }}
        }}
    </style>
</head>
<body>

    <!-- Centered Header Banner -->
    <header class="hero-banner">
        <div class="hero-container">
            <div class="badge-row">
                <span class="program-badge">
                    <svg viewBox="0 0 24 24" width="14" height="14" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg>
                    NTI & iVolve Accelerator
                </span>
                <span class="status-badge">Complete 28 Labs</span>
                <span class="program-badge">Clean Code & Solved Prompts</span>
            </div>
            <h1 class="hero-title">DevOps Accelerator — Complete Labs & Solutions Guide</h1>
            <p class="hero-subtitle">
                Clear, practical explanations written for developers and interns. Covers the real problem, visual workflow diagrams, exact slide questions, working configuration files, and colorful terminal commands for all 28 labs.
            </p>

            <div class="stats-grid">
                <div class="stat-card">
                    <span class="stat-val">{total_labs}</span>
                    <span class="stat-label">Hands-On Labs</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">6</span>
                    <span class="stat-label">Core Modules</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">100%</span>
                    <span class="stat-label">Solved & Verified</span>
                </div>
                <div class="stat-card">
                    <span class="stat-val">Clickable</span>
                    <span class="stat-label">Direct File Links</span>
                </div>
            </div>
        </div>
    </header>

    <!-- Mobile Drawer Backdrop Overlay -->
    <div id="drawerBackdrop" class="drawer-backdrop"></div>

    <!-- Centered Application Workspace -->
    <div class="app-layout">
        <!-- Sidebar Navigation (Desktop sidebar & Mobile slide-out drawer) -->
        <aside class="sidebar">
            <div class="sidebar-header-mobile">
                <span class="sidebar-title">
                    <svg viewBox="0 0 24 24" width="16" height="16" fill="currentColor"><circle cx="12" cy="12" r="10"/></svg>
                    DevOps Labs
                </span>
                <button id="closeSidebarBtn" class="close-sidebar-btn" aria-label="Close navigation">
                    <svg viewBox="0 0 24 24" width="18" height="18" stroke="currentColor" stroke-width="2.5" fill="none">
                        <line x1="18" y1="6" x2="6" y2="18"></line>
                        <line x1="6" y1="6" x2="18" y2="18"></line>
                    </svg>
                </button>
            </div>

            <div class="search-box">
                <svg class="search-icon" viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
                    <circle cx="11" cy="11" r="8"></circle>
                    <line x1="21" y1="21" x2="16.65" y2="16.65"></line>
                </svg>
                <input type="text" id="searchInput" class="search-input" placeholder="Search labs, tools, YAMLs...">
            </div>

            <div class="module-filters">
                <button class="filter-btn active" data-filter="all">All</button>
                <button class="filter-btn" data-filter="Build Tools">Build Tools</button>
                <button class="filter-btn" data-filter="Docker">Docker</button>
                <button class="filter-btn" data-filter="Kubernetes">Kubernetes</button>
                <button class="filter-btn" data-filter="Jenkins CI/CD">Jenkins</button>
                <button class="filter-btn" data-filter="GitOps">GitOps</button>
                <button class="filter-btn" data-filter="Ansible">Ansible</button>
            </div>

            <nav class="toc-list" id="tocList">
                {toc_html}
            </nav>
        </aside>

        <!-- Main Centered Content -->
        <main class="content-area">
            <div class="controls-bar">
                <div class="controls-info">
                    Showing <strong id="visibleCount">{total_labs}</strong> of {total_labs} Labs
                </div>
                <div>
                    <button id="toggleAllBtn" class="global-toggle-btn">
                        <svg viewBox="0 0 24 24" width="16" height="16" stroke="currentColor" stroke-width="2" fill="none">
                            <polyline points="7 13 12 18 17 13"></polyline>
                            <polyline points="7 6 12 11 17 6"></polyline>
                        </svg>
                        <span>Expand All Labs</span>
                    </button>
                </div>
            </div>

            <!-- Lab Cards -->
            <div id="labsContainer">
                {labs_html}
            </div>
        </main>
    </div>

    <!-- Resume Reading Toast -->
    <div id="resumeToast" class="resume-toast" role="status" aria-live="polite">
        <svg class="toast-icon" viewBox="0 0 24 24" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"></path>
            <path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"></path>
        </svg>
        <span id="resumeToastText">Resumed reading</span>
        <button id="resumeToastClose" class="toast-close" type="button" aria-label="Dismiss notification">
            <svg viewBox="0 0 24 24" width="14" height="14" stroke="currentColor" stroke-width="2.5" fill="none">
                <line x1="18" y1="6" x2="6" y2="18"></line>
                <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
        </button>
    </div>

    <!-- Mobile Floating Navigation Button (Symbol only) -->
    <button id="mobileNavBtn" class="mobile-nav-btn" aria-label="Labs &amp; Search" title="Labs &amp; Search">
        <svg viewBox="0 0 24 24" width="22" height="22" stroke="currentColor" stroke-width="2.2" fill="none">
            <line x1="4" y1="7" x2="20" y2="7"></line>
            <line x1="4" y1="12" x2="20" y2="12"></line>
            <line x1="4" y1="17" x2="20" y2="17"></line>
        </svg>
    </button>

    <!-- Back to Top Button -->
    <button id="backToTop" class="back-to-top" title="Back to top">
        <svg viewBox="0 0 24 24" width="20" height="20" stroke="currentColor" stroke-width="2.5" fill="none">
            <polyline points="18 15 12 9 6 15"></polyline>
        </svg>
    </button>

    <!-- Prism.js Scripts for Code Highlighting -->
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/prism.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-bash.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-yaml.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-docker.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-groovy.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-ini.min.js"></script>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/prism/1.29.0/components/prism-json.min.js"></script>

    <script>
        document.addEventListener('DOMContentLoaded', () => {{
            const searchInput = document.getElementById('searchInput');
            const filterButtons = document.querySelectorAll('.filter-btn');
            const labCards = document.querySelectorAll('.lab-card');
            const tocLinks = document.querySelectorAll('.toc-link');
            const toggleAllBtn = document.getElementById('toggleAllBtn');
            const visibleCount = document.getElementById('visibleCount');
            const backToTop = document.getElementById('backToTop');
            const mobileNavBtn = document.getElementById('mobileNavBtn');
            const closeSidebarBtn = document.getElementById('closeSidebarBtn');
            const drawerBackdrop = document.getElementById('drawerBackdrop');
            const sidebar = document.querySelector('.sidebar');
            const tocList = document.getElementById('tocList');
            const resumeToast = document.getElementById('resumeToast');
            const resumeToastText = document.getElementById('resumeToastText');
            const resumeToastClose = document.getElementById('resumeToastClose');

            let allExpanded = false;
            let currentActiveLabId = null;
            let isProgrammaticScroll = false;
            let programmaticTimer = null;

            // Mobile Drawer Controls
            function openMobileDrawer() {{
                if (sidebar) sidebar.classList.add('open');
                if (drawerBackdrop) drawerBackdrop.classList.add('active');
                document.body.classList.add('no-scroll');
            }}

            function closeMobileDrawer() {{
                if (sidebar) sidebar.classList.remove('open');
                if (drawerBackdrop) drawerBackdrop.classList.remove('active');
                document.body.classList.remove('no-scroll');
            }}

            if (mobileNavBtn) {{
                mobileNavBtn.addEventListener('click', openMobileDrawer);
            }}
            if (closeSidebarBtn) {{
                closeSidebarBtn.addEventListener('click', closeMobileDrawer);
            }}
            if (drawerBackdrop) {{
                drawerBackdrop.addEventListener('click', closeMobileDrawer);
            }}
            document.addEventListener('keydown', (e) => {{
                if (e.key === 'Escape') closeMobileDrawer();
            }});
            window.addEventListener('resize', () => {{
                if (window.innerWidth > 1024) {{
                    closeMobileDrawer();
                }}
            }});

            // Card Toggle accordion
            labCards.forEach(card => {{
                const header = card.querySelector('.lab-card-header');
                header.addEventListener('click', () => {{
                    card.classList.toggle('open');
                    if (card.classList.contains('open')) {{
                        currentActiveLabId = card.id;
                        saveReadingPosition(card.id);
                        updateTOCActive(card.id);
                    }}
                }});
            }});

            // Expand/Collapse All
            toggleAllBtn.addEventListener('click', () => {{
                allExpanded = !allExpanded;
                labCards.forEach(card => {{
                    if (allExpanded) {{
                        card.classList.add('open');
                    }} else {{
                        card.classList.remove('open');
                    }}
                }});
                toggleAllBtn.querySelector('span').textContent = allExpanded ? 'Collapse All Labs' : 'Expand All Labs';
            }});

            // Auto-scroll TOC list so active item stays comfortably visible
            function syncSidebarScroll(activeLink) {{
                if (!tocList || !activeLink) return;
                const listRect = tocList.getBoundingClientRect();
                const linkRect = activeLink.getBoundingClientRect();

                if (linkRect.top < listRect.top) {{
                    tocList.scrollTop += (linkRect.top - listRect.top - 10);
                }} else if (linkRect.bottom > listRect.bottom) {{
                    tocList.scrollTop += (linkRect.bottom - listRect.bottom + 10);
                }}
            }}

            // Highlight TOC item
            function updateTOCActive(labId) {{
                let activeLink = null;
                tocLinks.forEach(link => {{
                    const targetId = link.getAttribute('data-lab-id') || link.getAttribute('href').replace('#', '');
                    if (targetId === labId) {{
                        link.classList.add('active');
                        activeLink = link;
                    }} else {{
                        link.classList.remove('active');
                    }}
                }});
                if (activeLink) {{
                    syncSidebarScroll(activeLink);
                }}
                return activeLink;
            }}

            // Find which lab is currently at reading line
            function getActiveLab() {{
                const cards = Array.from(document.querySelectorAll('.lab-card')).filter(c => c.style.display !== 'none');
                if (!cards.length) return null;

                if ((window.innerHeight + window.scrollY) >= document.documentElement.scrollHeight - 60) {{
                    return cards[cards.length - 1];
                }}

                const scrollPoint = 160;
                for (let i = 0; i < cards.length; i++) {{
                    const card = cards[i];
                    const rect = card.getBoundingClientRect();
                    if (rect.top <= scrollPoint && rect.bottom > scrollPoint) {{
                        return card;
                    }}
                    if (i === 0 && rect.top > scrollPoint) {{
                        return card;
                    }}
                }}
                return cards[0];
            }}

            // Save reading state to localStorage
            function saveReadingPosition(labId) {{
                if (!labId) return;
                try {{
                    localStorage.setItem('devops_guide_last_lab', labId);
                }} catch (e) {{}}
            }}

            // Sync Right Column (Content) -> Left Column (TOC)
            function syncColumns() {{
                if (isProgrammaticScroll) return;
                const activeCard = getActiveLab();
                if (!activeCard) return;

                const activeId = activeCard.id;
                if (activeId === currentActiveLabId) return;

                currentActiveLabId = activeId;
                updateTOCActive(activeId);
                saveReadingPosition(activeId);
            }}

            // Throttled scroll listener
            let ticking = false;
            window.addEventListener('scroll', () => {{
                if (!ticking) {{
                    window.requestAnimationFrame(() => {{
                        syncColumns();
                        if (window.scrollY > 400) {{
                            backToTop.classList.add('visible');
                        }} else {{
                            backToTop.classList.remove('visible');
                        }}
                        ticking = false;
                    }});
                    ticking = true;
                }}
            }}, {{ passive: true }});

            // Filtering & Search
            let activeFilter = 'all';
            let searchQuery = '';

            function updateFilter() {{
                let count = 0;
                labCards.forEach(card => {{
                    const moduleName = card.getAttribute('data-module');
                    const textContent = card.innerText.toLowerCase();
                    const matchesFilter = (activeFilter === 'all' || moduleName.toLowerCase() === activeFilter.toLowerCase());
                    const matchesSearch = (!searchQuery || textContent.includes(searchQuery));

                    const tocLink = document.querySelector(`.toc-link[data-lab-id="${{card.id}}"]`) || 
                                     document.querySelector(`.toc-link[href="#${{card.id}}"]`);

                    if (matchesFilter && matchesSearch) {{
                        card.style.display = 'block';
                        if (tocLink) tocLink.style.display = 'flex';
                        count++;
                    }} else {{
                        card.style.display = 'none';
                        if (tocLink) tocLink.style.display = 'none';
                    }}
                }});
                visibleCount.textContent = count;
                syncColumns();
            }}

            filterButtons.forEach(btn => {{
                btn.addEventListener('click', () => {{
                    filterButtons.forEach(b => b.classList.remove('active'));
                    btn.classList.add('active');
                    activeFilter = btn.getAttribute('data-filter');
                    updateFilter();
                }});
            }});

            searchInput.addEventListener('input', (e) => {{
                searchQuery = e.target.value.toLowerCase().trim();
                updateFilter();
            }});

            // Left Column (TOC) -> Right Column (Content) Sync
            tocLinks.forEach(link => {{
                link.addEventListener('click', (e) => {{
                    e.preventDefault();
                    const targetId = link.getAttribute('href').substring(1);
                    const targetCard = document.getElementById(targetId);
                    if (!targetCard) return;

                    targetCard.classList.add('open');
                    currentActiveLabId = targetId;
                    updateTOCActive(targetId);
                    saveReadingPosition(targetId);

                    isProgrammaticScroll = true;
                    const targetY = targetCard.getBoundingClientRect().top + window.scrollY - 80;
                    window.scrollTo({{
                        top: targetY,
                        behavior: 'smooth'
                    }});

                    if (history.pushState) {{
                        history.pushState(null, null, '#' + targetId);
                    }}

                    clearTimeout(programmaticTimer);
                    programmaticTimer = setTimeout(() => {{
                        isProgrammaticScroll = false;
                    }}, 800);

                    closeMobileDrawer();
                }});
            }});

            // Toast feedback when reading position is restored
            function showResumeToast(message) {{
                if (!resumeToast || !resumeToastText) return;
                resumeToastText.textContent = message;
                resumeToast.classList.add('show');

                const hide = () => resumeToast.classList.remove('show');
                if (resumeToastClose) resumeToastClose.onclick = hide;
                setTimeout(hide, 4500);
            }}

            // Restore where user left reading on load
            function restoreReadingPosition() {{
                let targetLabId = null;

                if (window.location.hash && window.location.hash.startsWith('#lab-')) {{
                    targetLabId = window.location.hash.substring(1);
                }} else {{
                    try {{
                        targetLabId = localStorage.getItem('devops_guide_last_lab');
                    }} catch (e) {{}}
                }}

                if (!targetLabId) {{
                    syncColumns();
                    return;
                }}

                const targetCard = document.getElementById(targetLabId);
                if (!targetCard) {{
                    syncColumns();
                    return;
                }}

                targetCard.classList.add('open');
                currentActiveLabId = targetLabId;
                updateTOCActive(targetLabId);

                setTimeout(() => {{
                    const targetY = targetCard.getBoundingClientRect().top + window.scrollY - 80;
                    window.scrollTo({{
                        top: targetY,
                        behavior: 'smooth'
                    }});

                    const labNum = targetLabId.replace('lab-', '');
                    showResumeToast('Resumed where you left off: Lab ' + labNum);
                }}, 350);
            }}

            restoreReadingPosition();

            // Copy to Clipboard buttons — anchored to wrapper to prevent sliding on horizontal scroll
            document.querySelectorAll('pre').forEach(pre => {{
                let wrapper = pre.parentElement;
                if (!wrapper || !wrapper.classList.contains('code-block-wrapper')) {{
                    wrapper = document.createElement('div');
                    wrapper.className = 'code-block-wrapper';
                    pre.parentNode.insertBefore(wrapper, pre);
                    wrapper.appendChild(pre);
                }}

                // Clean up any button that might be inside pre
                const existingBtn = pre.querySelector('.copy-btn');
                if (existingBtn) existingBtn.remove();

                let copyBtn = wrapper.querySelector('.copy-btn');
                if (!copyBtn) {{
                    copyBtn = document.createElement('button');
                    copyBtn.className = 'copy-btn';
                    copyBtn.type = 'button';
                    copyBtn.setAttribute('aria-label', 'Copy code to clipboard');
                    copyBtn.textContent = 'Copy';
                    wrapper.appendChild(copyBtn);
                }}

                copyBtn.addEventListener('click', async (e) => {{
                    e.stopPropagation();
                    const code = pre.querySelector('code') ? pre.querySelector('code').innerText : pre.innerText;
                    try {{
                        await navigator.clipboard.writeText(code);
                        copyBtn.textContent = 'Copied!';
                        copyBtn.classList.add('copied');
                        setTimeout(() => {{
                            copyBtn.textContent = 'Copy';
                            copyBtn.classList.remove('copied');
                        }}, 2000);
                    }} catch (err) {{
                        console.error('Failed to copy', err);
                    }}
                }});
            }});

            // Back to Top button
            backToTop.addEventListener('click', () => {{
                window.scrollTo({{ top: 0, behavior: 'smooth' }});
                if (history.pushState) {{
                    history.pushState(null, null, ' ');
                }}
            }});

            // Re-run Prism highlighting if loaded asynchronously
            if (window.Prism) {{
                Prism.highlightAll();
            }}
        }});
    </script>
</body>
</html>"""
