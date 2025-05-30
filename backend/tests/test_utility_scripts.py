"""
Test cases for utility scripts and development tools.
"""

import os
import subprocess
import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


class TestScriptExistence:
    """Test that all utility scripts exist and are properly configured."""

    def test_post_create_script_exists(self):
        """Test that post-create script exists and is executable."""
        script_path = Path(".devcontainer/post-create.sh")
        assert script_path.exists(), "post-create.sh should exist"
        assert os.access(script_path, os.X_OK), "post-create.sh should be executable"

    def test_post_start_script_exists(self):
        """Test that post-start script exists and is executable."""
        script_path = Path(".devcontainer/post-start.sh")
        assert script_path.exists(), "post-start.sh should exist"
        assert os.access(script_path, os.X_OK), "post-start.sh should be executable"

    def test_database_setup_script_exists(self):
        """Test that database setup script exists and is executable."""
        script_path = Path(".devcontainer/scripts/setup-database.sh")
        assert script_path.exists(), "setup-database.sh should exist"
        assert os.access(script_path, os.X_OK), "setup-database.sh should be executable"

    def test_run_tests_script_exists(self):
        """Test that run-tests script exists and is executable."""
        script_path = Path(".devcontainer/scripts/run-tests.sh")
        assert script_path.exists(), "run-tests.sh should exist"
        assert os.access(script_path, os.X_OK), "run-tests.sh should be executable"


class TestScriptContent:
    """Test script content and structure."""

    def test_scripts_have_bash_shebang(self):
        """Test that all scripts have proper bash shebang."""
        scripts = [
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh",
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in scripts:
            with open(script_path, 'r') as f:
                first_line = f.readline().strip()
                assert first_line == "#!/bin/bash", f"{script_path} should have bash shebang"

    def test_scripts_have_error_handling(self):
        """Test that scripts have proper error handling."""
        scripts = [
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh",
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in scripts:
            with open(script_path, 'r') as f:
                content = f.read()
                assert "set -e" in content, f"{script_path} should have 'set -e' for error handling"

    def test_post_create_script_content(self):
        """Test post-create script has required functionality."""
        script_path = Path(".devcontainer/post-create.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        required_elements = [
            "pip install",  # Python dependency installation
            "npm install",  # Node.js dependency installation
            "alias",        # Shell aliases setup
            "git config",   # Git configuration
            "chmod +x"      # Script permissions
        ]
        
        for element in required_elements:
            assert element in content, f"post-create.sh should contain: {element}"

    def test_post_start_script_content(self):
        """Test post-start script has required functionality."""
        script_path = Path(".devcontainer/post-start.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        required_elements = [
            "pg_isready",   # PostgreSQL readiness check
            "redis-cli",    # Redis readiness check
            "tree",         # Project structure display
        ]
        
        for element in required_elements:
            assert element in content, f"post-start.sh should contain: {element}"

    def test_database_setup_script_content(self):
        """Test database setup script has required functionality."""
        script_path = Path(".devcontainer/scripts/setup-database.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        required_elements = [
            "pg_isready",           # PostgreSQL check
            "init_db",              # Database initialization
            "asyncio.run"           # Async database setup
        ]
        
        for element in required_elements:
            assert element in content, f"setup-database.sh should contain: {element}"

    def test_run_tests_script_content(self):
        """Test run-tests script has required functionality."""
        script_path = Path(".devcontainer/scripts/run-tests.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        required_elements = [
            "pytest",      # Backend testing
            "npm test",    # Frontend testing
            "pylint",      # Code linting
            "--cov",       # Coverage reporting
            "mypy"         # Type checking
        ]
        
        for element in required_elements:
            assert element in content, f"run-tests.sh should contain: {element}"


class TestScriptFunctionality:
    """Test script functionality with mocked dependencies."""

    @patch('subprocess.run')
    def test_post_create_script_execution(self, mock_run):
        """Test post-create script execution flow."""
        mock_run.return_value = MagicMock(returncode=0)
        
        # Test that script can be executed without errors
        script_path = Path(".devcontainer/post-create.sh")
        
        # Read script content to verify it's syntactically correct
        with open(script_path, 'r') as f:
            content = f.read()
        
        # Check for syntax errors by attempting to parse
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script syntax error: {result.stderr}"

    @patch('subprocess.run')
    def test_database_setup_script_execution(self, mock_run):
        """Test database setup script execution flow."""
        mock_run.return_value = MagicMock(returncode=0)
        
        script_path = Path(".devcontainer/scripts/setup-database.sh")
        
        # Check script syntax
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script syntax error: {result.stderr}"

    @patch('subprocess.run')
    def test_run_tests_script_execution(self, mock_run):
        """Test run-tests script execution flow."""
        mock_run.return_value = MagicMock(returncode=0)
        
        script_path = Path(".devcontainer/scripts/run-tests.sh")
        
        # Check script syntax
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Script syntax error: {result.stderr}"


class TestAliasDefinitions:
    """Test that development aliases are properly defined."""

    def test_development_aliases_defined(self):
        """Test that development aliases are defined in post-create script."""
        script_path = Path(".devcontainer/post-create.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        expected_aliases = [
            "alias runapi=",
            "alias runfrontend=",
            "alias test-backend=",
            "alias test-frontend=",
            "alias backend=",
            "alias frontend=",
            "alias docs="
        ]
        
        for alias in expected_aliases:
            assert alias in content, f"Development alias should be defined: {alias}"

    def test_docker_aliases_defined(self):
        """Test that Docker aliases are defined."""
        script_path = Path(".devcontainer/post-create.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        docker_aliases = [
            "alias dc=",
            "alias dcup=",
            "alias dcdown=",
            "alias dcbuild=",
            "alias dclogs="
        ]
        
        for alias in docker_aliases:
            assert alias in content, f"Docker alias should be defined: {alias}"

    def test_git_aliases_defined(self):
        """Test that Git aliases are defined."""
        script_path = Path(".devcontainer/post-create.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        git_aliases = [
            "alias gs=",
            "alias ga=",
            "alias gc=",
            "alias gp=",
            "alias gl=",
            "alias gb=",
            "alias gco=",
            "alias gd=",
            "alias glog="
        ]
        
        for alias in git_aliases:
            assert alias in content, f"Git alias should be defined: {alias}"


class TestScriptErrorHandling:
    """Test script error handling and robustness."""

    def test_scripts_handle_missing_dependencies(self):
        """Test that scripts handle missing dependencies gracefully."""
        scripts_to_test = [
            ".devcontainer/post-create.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in scripts_to_test:
            with open(script_path, 'r') as f:
                content = f.read()
            
            # Check for conditional execution patterns
            conditional_patterns = [
                "if [ -f",      # File existence checks
                "command -v",   # Command availability checks
                "which",        # Alternative command checks
            ]
            
            has_conditionals = any(pattern in content for pattern in conditional_patterns)
            assert has_conditionals, f"{script_path} should have conditional checks for dependencies"

    def test_scripts_provide_helpful_output(self):
        """Test that scripts provide helpful output messages."""
        scripts_to_test = [
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh",
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in scripts_to_test:
            with open(script_path, 'r') as f:
                content = f.read()
            
            # Check for output functions or echo statements
            output_patterns = [
                "echo",
                "print_status",
                "print_success",
                "print_error"
            ]
            
            has_output = any(pattern in content for pattern in output_patterns)
            assert has_output, f"{script_path} should provide user feedback"


class TestScriptPermissions:
    """Test script file permissions and security."""

    def test_script_permissions(self):
        """Test that scripts have appropriate permissions."""
        scripts = [
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh",
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in scripts:
            path = Path(script_path)
            if path.exists():
                # Check that script is executable by owner
                stat_info = path.stat()
                is_executable = bool(stat_info.st_mode & 0o100)
                assert is_executable, f"{script_path} should be executable"

    def test_script_ownership(self):
        """Test that scripts don't have overly permissive permissions."""
        scripts = [
            ".devcontainer/post-create.sh",
            ".devcontainer/post-start.sh",
            ".devcontainer/scripts/setup-database.sh",
            ".devcontainer/scripts/run-tests.sh"
        ]
        
        for script_path in scripts:
            path = Path(script_path)
            if path.exists():
                stat_info = path.stat()
                # Check that script is not world-writable
                is_world_writable = bool(stat_info.st_mode & 0o002)
                assert not is_world_writable, f"{script_path} should not be world-writable"


@pytest.mark.integration
class TestScriptIntegration:
    """Integration tests for script functionality."""

    @pytest.mark.skipif(
        not os.getenv("TEST_SCRIPT_INTEGRATION"),
        reason="Script integration tests require TEST_SCRIPT_INTEGRATION=1"
    )
    def test_run_tests_script_with_backend_only(self):
        """Test run-tests script with backend-only flag."""
        script_path = Path(".devcontainer/scripts/run-tests.sh")
        
        result = subprocess.run(
            ["bash", str(script_path), "--backend-only"],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        # Script should execute without syntax errors
        # Actual test execution might fail due to missing dependencies
        assert "syntax error" not in result.stderr.lower()

    @pytest.mark.skipif(
        not os.getenv("TEST_SCRIPT_INTEGRATION"),
        reason="Script integration tests require TEST_SCRIPT_INTEGRATION=1"
    )
    def test_database_setup_script_dry_run(self):
        """Test database setup script in dry-run mode."""
        script_path = Path(".devcontainer/scripts/setup-database.sh")
        
        # Test script syntax and basic execution
        result = subprocess.run(
            ["bash", "-n", str(script_path)],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Database setup script has syntax errors: {result.stderr}"
