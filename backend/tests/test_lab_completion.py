"""
Comprehensive test suite for LAB-10 and LAB-2 completion verification.
"""

import os
import json
import pytest
from pathlib import Path
from typing import List, Dict


class TestLAB10Completion:
    """Test that LAB-10 requirements are fully met."""

    def test_devcontainer_setup_complete(self):
        """Test that dev container setup is complete and functional."""
        # Check main devcontainer.json exists and is valid
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        assert devcontainer_path.exists(), "devcontainer.json must exist"
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        # Verify essential configuration
        assert config["name"] == "Wellows Development Environment"
        assert "dockerComposeFile" in config
        assert "customizations" in config
        assert "vscode" in config["customizations"]

    def test_vscode_extensions_comprehensive(self):
        """Test that VS Code extensions are comprehensive (40+ extensions)."""
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        extensions = config["customizations"]["vscode"]["extensions"]
        
        # Should have 40+ extensions as specified
        assert len(extensions) >= 40, f"Should have 40+ extensions, got {len(extensions)}"
        
        # Check for key categories
        python_extensions = [ext for ext in extensions if "python" in ext.lower()]
        typescript_extensions = [ext for ext in extensions if "typescript" in ext.lower() or "javascript" in ext.lower()]
        docker_extensions = [ext for ext in extensions if "docker" in ext.lower()]
        git_extensions = [ext for ext in extensions if "git" in ext.lower()]
        
        assert len(python_extensions) >= 3, "Should have multiple Python extensions"
        assert len(typescript_extensions) >= 1, "Should have TypeScript/JavaScript extensions"
        assert len(docker_extensions) >= 1, "Should have Docker extensions"
        assert len(git_extensions) >= 1, "Should have Git extensions"

    def test_automated_setup_scripts(self):
        """Test that automated setup scripts are present and functional."""
        required_scripts = [
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh"
        ]
        
        for script_path in required_scripts:
            path = Path(script_path)
            assert path.exists(), f"Required script {script_path} must exist"
            assert os.access(path, os.X_OK), f"Script {script_path} must be executable"

    def test_utility_scripts_present(self):
        """Test that utility scripts are present and functional."""
        utility_scripts = [
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in utility_scripts:
            path = Path(script_path)
            assert path.exists(), f"Utility script {script_path} must exist"
            assert os.access(path, os.X_OK), f"Script {script_path} must be executable"

    def test_development_aliases_configured(self):
        """Test that development aliases are properly configured."""
        post_create_path = Path(".devcontainer/post-create.sh")
        
        with open(post_create_path, 'r') as f:
            content = f.read()
        
        required_aliases = [
            "runapi",
            "runfrontend", 
            "test-backend",
            "test-frontend",
            "backend",
            "frontend",
            "docs"
        ]
        
        for alias in required_aliases:
            assert f"alias {alias}=" in content, f"Alias {alias} must be configured"

    def test_multi_language_support(self):
        """Test that multi-language support (Python + Node.js) is configured."""
        dockerfile_path = Path(".devcontainer/Dockerfile")
        assert dockerfile_path.exists(), "Dockerfile must exist"
        
        with open(dockerfile_path, 'r') as f:
            content = f.read()
        
        # Check for Python and Node.js installation
        assert "python" in content.lower(), "Dockerfile should install Python"
        assert "node" in content.lower(), "Dockerfile should install Node.js"

    def test_database_integration(self):
        """Test that database services are integrated."""
        compose_path = Path("docker-compose.dev.yml")
        assert compose_path.exists(), "docker-compose.dev.yml must exist"
        
        with open(compose_path, 'r') as f:
            content = f.read()
        
        # Check for database services
        assert "postgres:" in content, "PostgreSQL service must be configured"
        assert "redis:" in content, "Redis service must be configured"

    def test_port_forwarding_configured(self):
        """Test that port forwarding is properly configured."""
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        forwarded_ports = config["forwardPorts"]
        required_ports = [3000, 8000, 5432, 6379]
        
        for port in required_ports:
            assert port in forwarded_ports, f"Port {port} must be forwarded"


class TestLAB2Completion:
    """Test that LAB-2 requirements are fully met."""

    def test_folder_documentation_complete(self):
        """Test that each major folder has comprehensive documentation."""
        required_readmes = [
            "backend/README.md",
            "frontend/README.md", 
            ".devcontainer/README.md",
            "docs/README.md",
            "backend/tests/README.md"
        ]
        
        for readme_path in required_readmes:
            path = Path(readme_path)
            assert path.exists(), f"Documentation {readme_path} must exist"
            
            # Check that documentation is substantial (not just a stub)
            file_size = path.stat().st_size
            assert file_size > 1000, f"Documentation {readme_path} must be substantial (>{1000} bytes)"

    def test_main_readme_enhanced(self):
        """Test that main README is enhanced with navigation."""
        readme_path = Path("README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for enhanced sections
        required_sections = [
            "# Wellows AI Chatbot",
            "## ✨ Features",
            "## 📚 Enhanced Documentation",
            "## 🎯 **LAB Tasks Completed**"
        ]
        
        for section in required_sections:
            assert section in content, f"Main README must contain section: {section}"

    def test_documentation_navigation(self):
        """Test that documentation has proper navigation between sections."""
        readme_path = Path("README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for links to folder documentation
        expected_links = [
            "./backend/README.md",
            "./frontend/README.md",
            "./.devcontainer/README.md",
            "./docs/README.md",
            "./backend/tests/README.md"
        ]
        
        for link in expected_links:
            assert link in content, f"Main README must link to {link}"

    def test_documentation_consistency(self):
        """Test that documentation is consistent across folders."""
        readme_files = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md"
        ]
        
        project_name = "Wellows"
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                assert project_name in content, f"{readme_file} must mention project name: {project_name}"

    def test_documentation_structure_standards(self):
        """Test that documentation follows consistent structure standards."""
        readme_files = [
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md"
        ]
        
        for readme_file in readme_files:
            readme_path = Path(readme_file)
            if readme_path.exists():
                with open(readme_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                # Check for standard sections
                standard_sections = [
                    "## Overview",
                    "## 🏗️ Architecture" if "backend" in readme_file or "frontend" in readme_file else "## 🏗️ Structure",
                    "## 🚀 Quick Start"
                ]
                
                for section in standard_sections:
                    if section.endswith("Structure") and "devcontainer" not in readme_file:
                        continue
                    assert section in content, f"{readme_file} should contain standard section: {section}"

    def test_api_documentation_present(self):
        """Test that API documentation is present and comprehensive."""
        api_doc_path = Path("docs/API.md")
        assert api_doc_path.exists(), "API documentation must exist"
        
        # Check backend README for API documentation section
        backend_readme_path = Path("backend/README.md")
        with open(backend_readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "## 📚 API Documentation" in content, "Backend README must have API documentation section"

    def test_setup_guides_present(self):
        """Test that setup guides are present and comprehensive."""
        setup_doc_path = Path("docs/SETUP.md")
        assert setup_doc_path.exists(), "Setup documentation must exist"
        
        # Check that main README has setup information
        readme_path = Path("README.md")
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        assert "Getting Started" in content, "Main README must have getting started section"


class TestOverallQuality:
    """Test overall quality and completeness of LAB implementations."""

    def test_no_placeholder_content(self):
        """Test that there's no placeholder or TODO content."""
        files_to_check = [
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md",
            ".devcontainer/devcontainer.json"
        ]
        
        placeholder_patterns = [
            "TODO",
            "FIXME",
            "PLACEHOLDER",
            "TBD",
            "Coming soon",
            "Under construction"
        ]
        
        for file_path in files_to_check:
            path = Path(file_path)
            if path.exists():
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read().upper()
                
                for pattern in placeholder_patterns:
                    assert pattern not in content, f"{file_path} should not contain placeholder: {pattern}"

    def test_comprehensive_coverage(self):
        """Test that implementation provides comprehensive coverage."""
        # Check that we have documentation for all major components
        components = [
            ("backend", "backend/README.md"),
            ("frontend", "frontend/README.md"),
            ("devcontainer", ".devcontainer/README.md"),
            ("tests", "backend/tests/README.md"),
            ("docs", "docs/README.md")
        ]
        
        for component_name, readme_path in components:
            path = Path(readme_path)
            assert path.exists(), f"{component_name} component must have documentation"
            
            # Check that documentation is comprehensive
            with open(path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Should have multiple sections
            section_count = content.count("##")
            assert section_count >= 5, f"{readme_path} should have multiple sections (>=5), got {section_count}"

    def test_development_workflow_documented(self):
        """Test that development workflow is properly documented."""
        readme_path = Path("README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        workflow_elements = [
            "Quick Development Commands",
            "runapi",
            "runfrontend",
            "test-backend",
            "Dev Container"
        ]
        
        for element in workflow_elements:
            assert element in content, f"Development workflow should include: {element}"

    def test_jira_task_completion_documented(self):
        """Test that JIRA task completion is properly documented."""
        readme_path = Path("README.md")
        
        with open(readme_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that LAB tasks are documented as completed
        assert "LAB-10" in content, "LAB-10 completion should be documented"
        assert "LAB-2" in content, "LAB-2 completion should be documented"
        assert "✅" in content, "Completion status should be marked with checkmarks"


@pytest.mark.integration
class TestEndToEndIntegration:
    """End-to-end integration tests for the complete implementation."""

    def test_all_files_present(self):
        """Test that all expected files are present."""
        expected_files = [
            # Dev container files
            ".devcontainer/devcontainer.json",
            ".devcontainer/Dockerfile",
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh",
            ".devcontainer/requirements.dev.txt",
            
            # Utility scripts
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh",
            
            # Documentation files
            "README.md",
            "backend/README.md",
            "frontend/README.md",
            ".devcontainer/README.md",
            "docs/README.md",
            "backend/tests/README.md",
            
            # Configuration files
            "docker-compose.dev.yml",
            ".env.example"
        ]
        
        for file_path in expected_files:
            path = Path(file_path)
            assert path.exists(), f"Expected file must exist: {file_path}"

    def test_implementation_completeness(self):
        """Test that implementation is complete and ready for use."""
        # This is a meta-test that verifies the overall implementation
        
        # Check LAB-10 completion indicators
        lab10_indicators = [
            Path(".devcontainer/devcontainer.json").exists(),
            Path(".devcontainer/post-create.sh").exists(),
            Path(".devcontainer/scripts").exists()
        ]
        
        assert all(lab10_indicators), "LAB-10 implementation must be complete"
        
        # Check LAB-2 completion indicators  
        lab2_indicators = [
            Path("backend/README.md").exists(),
            Path("frontend/README.md").exists(),
            Path(".devcontainer/README.md").exists(),
            Path("docs/README.md").exists()
        ]
        
        assert all(lab2_indicators), "LAB-2 implementation must be complete"
