"""
Test cases for dev container integration and setup.
"""

import os
import subprocess
import pytest
import json
from pathlib import Path


class TestDevContainerConfiguration:
    """Test dev container configuration and setup."""

    def test_devcontainer_json_exists(self):
        """Test that devcontainer.json exists and is valid."""
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        assert devcontainer_path.exists(), "devcontainer.json should exist"
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        # Verify required fields
        assert "name" in config
        assert "dockerComposeFile" in config
        assert "service" in config
        assert "workspaceFolder" in config
        assert config["name"] == "Wellows Development Environment"

    def test_devcontainer_extensions(self):
        """Test that required VS Code extensions are configured."""
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        extensions = config["customizations"]["vscode"]["extensions"]
        
        # Test essential extensions are included
        essential_extensions = [
            "ms-python.python",
            "ms-python.black-formatter",
            "ms-vscode.vscode-typescript-next",
            "esbenp.prettier-vscode",
            "ms-azuretools.vscode-docker",
            "github.copilot"
        ]
        
        for ext in essential_extensions:
            assert ext in extensions, f"Extension {ext} should be configured"

    def test_devcontainer_port_forwarding(self):
        """Test that required ports are configured for forwarding."""
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        forwarded_ports = config["forwardPorts"]
        required_ports = [3000, 8000, 5432, 6379]
        
        for port in required_ports:
            assert port in forwarded_ports, f"Port {port} should be forwarded"

    def test_devcontainer_features(self):
        """Test that dev container features are properly configured."""
        devcontainer_path = Path(".devcontainer/devcontainer.json")
        
        with open(devcontainer_path, 'r') as f:
            config = json.load(f)
        
        features = config.get("features", {})
        
        # Check for essential features
        assert "ghcr.io/devcontainers/features/common-utils:2" in features
        assert "ghcr.io/devcontainers/features/git:1" in features
        assert "ghcr.io/devcontainers/features/github-cli:1" in features


class TestDevContainerScripts:
    """Test dev container setup scripts."""

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

    def test_utility_scripts_exist(self):
        """Test that utility scripts exist and are executable."""
        scripts_dir = Path(".devcontainer/scripts")
        assert scripts_dir.exists(), "scripts directory should exist"
        
        required_scripts = [
            "setup-database.sh",
            "run-tests.sh"
        ]
        
        for script_name in required_scripts:
            script_path = scripts_dir / script_name
            assert script_path.exists(), f"{script_name} should exist"
            assert os.access(script_path, os.X_OK), f"{script_name} should be executable"

    def test_script_shebang(self):
        """Test that scripts have proper shebang."""
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


class TestDockerComposeIntegration:
    """Test Docker Compose integration with dev container."""

    def test_docker_compose_dev_exists(self):
        """Test that docker-compose.dev.yml exists."""
        compose_path = Path("docker-compose.dev.yml")
        assert compose_path.exists(), "docker-compose.dev.yml should exist"

    def test_dev_service_configuration(self):
        """Test that dev service is properly configured."""
        # This would require PyYAML to parse the compose file
        # For now, we'll check file existence and basic structure
        compose_path = Path("docker-compose.dev.yml")
        
        with open(compose_path, 'r') as f:
            content = f.read()
        
        # Check for essential service configurations
        assert "dev:" in content, "dev service should be defined"
        assert "postgres:" in content, "postgres service should be defined"
        assert "redis:" in content, "redis service should be defined"


class TestEnvironmentSetup:
    """Test environment setup and configuration."""

    def test_env_example_exists(self):
        """Test that .env.example exists."""
        env_example_path = Path(".env.example")
        assert env_example_path.exists(), ".env.example should exist"

    def test_env_example_contains_required_vars(self):
        """Test that .env.example contains required environment variables."""
        env_example_path = Path(".env.example")
        
        with open(env_example_path, 'r') as f:
            content = f.read()
        
        required_vars = [
            "DATABASE_URL",
            "SECRET_KEY",
            "OPENAI_API_KEY",
            "REDIS_URL"
        ]
        
        for var in required_vars:
            assert var in content, f"{var} should be in .env.example"

    def test_requirements_dev_exists(self):
        """Test that development requirements file exists."""
        req_path = Path(".devcontainer/requirements.dev.txt")
        assert req_path.exists(), "requirements.dev.txt should exist"

    def test_requirements_dev_contains_essential_packages(self):
        """Test that dev requirements contain essential packages."""
        req_path = Path(".devcontainer/requirements.dev.txt")
        
        with open(req_path, 'r') as f:
            content = f.read()
        
        essential_packages = [
            "black",
            "isort",
            "pylint",
            "pytest",
            "mypy"
        ]
        
        for package in essential_packages:
            assert package in content, f"{package} should be in requirements.dev.txt"


@pytest.mark.integration
class TestDevContainerBuild:
    """Integration tests for dev container build process."""

    @pytest.mark.skipif(
        not os.getenv("TEST_DEVCONTAINER_BUILD"),
        reason="Dev container build tests require TEST_DEVCONTAINER_BUILD=1"
    )
    def test_devcontainer_builds_successfully(self):
        """Test that dev container builds without errors."""
        # This test would require Docker and would be slow
        # Only run when explicitly requested
        result = subprocess.run(
            ["docker", "build", "-f", ".devcontainer/Dockerfile", "."],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Dev container build failed: {result.stderr}"

    @pytest.mark.skipif(
        not os.getenv("TEST_DEVCONTAINER_BUILD"),
        reason="Dev container build tests require TEST_DEVCONTAINER_BUILD=1"
    )
    def test_docker_compose_dev_starts(self):
        """Test that docker-compose.dev.yml starts successfully."""
        result = subprocess.run(
            ["docker-compose", "-f", "docker-compose.dev.yml", "config"],
            capture_output=True,
            text=True
        )
        
        assert result.returncode == 0, f"Docker compose config invalid: {result.stderr}"


class TestAliasesAndCommands:
    """Test that development aliases and commands are properly set up."""

    def test_alias_definitions_in_post_create(self):
        """Test that aliases are defined in post-create script."""
        script_path = Path(".devcontainer/post-create.sh")
        
        with open(script_path, 'r') as f:
            content = f.read()
        
        expected_aliases = [
            "alias runapi=",
            "alias runfrontend=",
            "alias test-backend=",
            "alias backend=",
            "alias frontend="
        ]
        
        for alias in expected_aliases:
            assert alias in content, f"Alias {alias} should be defined in post-create.sh"

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
            "alias gl="
        ]
        
        for alias in git_aliases:
            assert alias in content, f"Git alias {alias} should be defined"
