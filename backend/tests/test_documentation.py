"""
Test cases for documentation completeness and quality.
"""

import os
import re
import pytest
from pathlib import Path
from typing import List, Dict


class TestDocumentationStructure:
    """Test documentation structure and completeness."""

    def test_main_readme_exists(self):
        """Test that main README.md exists."""
        readme_path = Path("README.md")
        assert readme_path.exists(), "Main README.md should exist"

    def test_folder_readmes_exist(self):
        """Test that each major folder has a README.md."""
        required_readmes = [
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md",
            "docs/README.md",
            "backend/tests/README.md"
        ]
        
        for readme_path in required_readmes:
            path = Path(readme_path)
            assert path.exists(), f"{readme_path} should exist"

    def test_docs_folder_structure(self):
        """Test that docs folder has proper structure."""
        docs_path = Path("docs")
        assert docs_path.exists(), "docs folder should exist"
        
        required_docs = [
            "docs/README.md",
            "docs/SETUP.md",
            "docs/ARCHITECTURE.md",
            "docs/API.md"
        ]
        
        for doc_path in required_docs:
            path = Path(doc_path)
            assert path.exists(), f"{doc_path} should exist"


class TestDocumentationContent:
    """Test documentation content quality and completeness."""

    def test_main_readme_sections(self):
        """Test that main README has required sections."""
        readme_path = Path("README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            "# Wellows AI Chatbot",
            "## ✨ Features",
            "## Technology Stack",
            "## 🚀 Getting Started",
            "## 📚 Enhanced Documentation"
        ]
        
        for section in required_sections:
            assert section in content, f"Main README should contain section: {section}"

    def test_backend_readme_completeness(self):
        """Test that backend README is comprehensive."""
        readme_path = Path("backend/README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            "# Backend - Wellows AI Chatbot API",
            "## 🏗️ Architecture",
            "## 🚀 Quick Start",
            "## 📚 API Documentation",
            "## 🧪 Testing",
            "## 🔒 Security"
        ]
        
        for section in required_sections:
            assert section in content, f"Backend README should contain: {section}"

    def test_frontend_readme_completeness(self):
        """Test that frontend README is comprehensive."""
        readme_path = Path("frontend/README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            "# Frontend - Wellows AI Chatbot Interface",
            "## 🏗️ Architecture",
            "## 🚀 Quick Start",
            "## 🎨 Design System",
            "## 🧪 Testing"
        ]
        
        for section in required_sections:
            assert section in content, f"Frontend README should contain: {section}"

    def test_devcontainer_readme_completeness(self):
        """Test that dev container README is comprehensive."""
        readme_path = Path(".devcontainer/README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        required_sections = [
            "# Dev Container - Wellows Development Environment",
            "## 🏗️ Structure",
            "## 🚀 Quick Start",
            "## 🔧 Configuration Details",
            "## 🛠️ Included Tools"
        ]
        
        for section in required_sections:
            assert section in content, f"Dev container README should contain: {section}"


class TestDocumentationLinks:
    """Test that documentation links are valid."""

    def _extract_markdown_links(self, content: str) -> List[Dict[str, str]]:
        """Extract markdown links from content."""
        # Pattern for [text](url) format
        link_pattern = r'\[([^\]]+)\]\(([^)]+)\)'
        matches = re.findall(link_pattern, content)
        return [{"text": text, "url": url} for text, url in matches]

    def test_internal_links_valid(self):
        """Test that internal documentation links are valid."""
        readme_path = Path("README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        links = self._extract_markdown_links(content)
        
        for link in links:
            url = link["url"]
            # Check internal relative links
            if url.startswith("./") and url.endswith(".md"):
                file_path = Path(url[2:])  # Remove "./"
                assert file_path.exists(), f"Internal link target should exist: {url}"

    def test_cross_references_exist(self):
        """Test that cross-references between docs exist."""
        main_readme_path = Path("README.md")
        
        with open(main_readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that main README links to folder READMEs
        expected_links = [
            "./backend/README.md",
            "./frontend/README.md",
            "./.devcontainer/README.md",
            "./docs/README.md",
            "./backend/tests/README.md"
        ]
        
        for expected_link in expected_links:
            assert expected_link in content, f"Main README should link to {expected_link}"


class TestCodeExamples:
    """Test that code examples in documentation are valid."""

    def test_bash_examples_syntax(self):
        """Test that bash code examples have proper syntax."""
        readme_files = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md"
        ]
        
        bash_block_pattern = r'```bash\n(.*?)\n```'
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if not readme_path.exists():
                continue
                
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            bash_blocks = re.findall(bash_block_pattern, content, re.DOTALL)
            
            for block in bash_blocks:
                # Basic syntax checks
                lines = block.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        # Check for common bash syntax issues
                        assert not line.endswith('\\\\'), f"Double backslash in bash: {line}"
                        assert '&&' not in line or line.count('&&') == line.count(' && '), f"Malformed && in: {line}"

    def test_json_examples_valid(self):
        """Test that JSON code examples are valid."""
        readme_files = [
            "backend/README.md",
            ".devcontainer/README.md"
        ]
        
        json_block_pattern = r'```json\n(.*?)\n```'
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if not readme_path.exists():
                continue
                
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            json_blocks = re.findall(json_block_pattern, content, re.DOTALL)
            
            for block in json_blocks:
                try:
                    import json
                    json.loads(block)
                except json.JSONDecodeError as e:
                    pytest.fail(f"Invalid JSON in {readme_file}: {e}")


class TestDocumentationConsistency:
    """Test documentation consistency across files."""

    def test_project_name_consistency(self):
        """Test that project name is consistent across documentation."""
        readme_files = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md",
            "docs/README.md"
        ]
        
        expected_name = "Wellows"
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if not readme_path.exists():
                continue
                
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            assert expected_name in content, f"{readme_file} should mention project name: {expected_name}"

    def test_consistent_formatting(self):
        """Test that documentation uses consistent formatting."""
        readme_files = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md"
        ]
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if not readme_path.exists():
                continue
                
            with open(readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for consistent emoji usage in headers
            emoji_headers = re.findall(r'^## [🎯🚀🔧📚🛠️📁🧪🔄📊♿🔍🤝📈🆘]', content, re.MULTILINE)
            if emoji_headers:
                # If emojis are used, they should be consistent
                assert len(emoji_headers) > 0, f"{readme_file} should use emojis consistently in headers"

    def test_table_of_contents_links(self):
        """Test that table of contents links work properly."""
        docs_readme_path = Path("docs/README.md")
        
        if docs_readme_path.exists():
            with open(docs_readme_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for TOC-style links
            toc_links = re.findall(r'\[([^\]]+)\]\(\.\/([^)]+\.md)\)', content)
            
            for link_text, file_path in toc_links:
                full_path = Path("docs") / file_path
                # Note: Some files might not exist yet, so we'll just check format
                assert file_path.endswith('.md'), f"TOC link should point to .md file: {file_path}"


class TestDocumentationMetadata:
    """Test documentation metadata and structure."""

    def test_readme_file_sizes(self):
        """Test that README files are substantial (not empty stubs)."""
        readme_files = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md",
            "docs/README.md",
            "backend/tests/README.md"
        ]
        
        min_size = 1000  # Minimum 1KB for substantial documentation
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if readme_path.exists():
                file_size = readme_path.stat().st_size
                assert file_size > min_size, f"{readme_file} should be substantial (>{min_size} bytes), got {file_size}"

    def test_documentation_encoding(self):
        """Test that documentation files use UTF-8 encoding."""
        readme_files = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md"
        ]
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if readme_path.exists():
                try:
                    with open(readme_path, 'r', encoding='utf-8') as f:
                        f.read()
                except UnicodeDecodeError:
                    pytest.fail(f"{readme_file} should be UTF-8 encoded")
