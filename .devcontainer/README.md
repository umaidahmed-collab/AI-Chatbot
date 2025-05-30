# Dev Container - Wellows Development Environment

## Overview

This directory contains the development container configuration for the Wellows AI Chatbot project. The dev container provides a consistent, fully-configured development environment that works across different machines and operating systems.

## 🏗️ Structure

```
.devcontainer/
├── README.md              # This documentation
├── devcontainer.json      # Dev container configuration
├── Dockerfile             # Container image definition
├── requirements.dev.txt   # Development Python dependencies
├── post-create.sh         # Post-creation setup script
├── post-start.sh          # Post-start setup script
└── scripts/               # Utility scripts
    ├── setup-database.sh  # Database initialization
    └── run-tests.sh       # Comprehensive test runner
```

## 🚀 Quick Start

### Prerequisites
- **VS Code** with Remote-Containers extension
- **Docker Desktop** (Windows/Mac) or **Docker Engine** (Linux)
- **Git** for cloning the repository

### Getting Started
1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd wellows-chatbot
   ```

2. **Open in VS Code**:
   ```bash
   code .
   ```

3. **Reopen in Container**:
   - Press `Ctrl+Shift+P` (or `Cmd+Shift+P` on Mac)
   - Type "Remote-Containers: Reopen in Container"
   - Select the command and wait for the container to build

4. **Start developing**:
   ```bash
   runapi      # Start backend API
   runfrontend # Start frontend (in another terminal)
   ```

## 🔧 Configuration Details

### devcontainer.json
The main configuration file that defines:
- **Base image**: Custom Dockerfile with Python and Node.js
- **VS Code extensions**: Pre-installed development tools
- **Port forwarding**: Automatic port mapping for services
- **Settings**: Optimized VS Code configuration
- **Features**: Additional dev container features

### Key Features
- **Multi-language support**: Python 3.11 + Node.js 18
- **Database services**: PostgreSQL and Redis
- **AI/ML tools**: OpenAI, LangChain, ChromaDB
- **Development tools**: Git, GitHub CLI, testing frameworks
- **Code quality**: Linting, formatting, type checking

## 🛠️ Included Tools

### Development Tools
- **Python 3.11**: Latest Python with pip
- **Node.js 18**: JavaScript runtime with npm
- **Git**: Version control with GitHub CLI
- **Docker**: Container management tools
- **PostgreSQL Client**: Database interaction tools
- **Redis CLI**: Cache management tools

### VS Code Extensions
- **Python**: Full Python development support
- **TypeScript**: JavaScript/TypeScript development
- **Docker**: Container management
- **GitHub**: Git integration and Copilot
- **Testing**: pytest and Jest integration
- **Linting**: ESLint, Pylint, and formatters

### Productivity Features
- **Oh My Zsh**: Enhanced shell experience
- **Aliases**: Convenient shortcuts for common tasks
- **Auto-completion**: Intelligent code completion
- **Debugging**: Integrated debugging support
- **Testing**: One-click test execution

## 📝 Scripts and Automation

### post-create.sh
Runs once when the container is first created:
- Installs Python and Node.js dependencies
- Sets up Git configuration
- Creates useful shell aliases
- Configures development environment
- Sets up pre-commit hooks

### post-start.sh
Runs every time the container starts:
- Checks service availability
- Displays helpful information
- Shows project structure
- Provides quick start commands

### Utility Scripts

#### setup-database.sh
```bash
# Initialize database tables
.devcontainer/scripts/setup-database.sh
```

#### run-tests.sh
```bash
# Run comprehensive test suite
.devcontainer/scripts/run-tests.sh

# Run specific test types
.devcontainer/scripts/run-tests.sh --backend-only
.devcontainer/scripts/run-tests.sh --frontend-only
.devcontainer/scripts/run-tests.sh --no-lint
```

## 🔗 Port Forwarding

The dev container automatically forwards these ports:

| Port | Service | Description |
|------|---------|-------------|
| 3000 | Frontend | React development server |
| 8000 | Backend | FastAPI application |
| 5432 | PostgreSQL | Database server |
| 6379 | Redis | Cache server |

## 🎯 Useful Aliases

The dev container includes helpful aliases:

### Project Navigation
```bash
backend     # cd /workspace/backend
frontend    # cd /workspace/frontend
docs        # cd /workspace/docs
```

### Development Commands
```bash
runapi      # Start backend API server
runfrontend # Start frontend development server
test-backend   # Run backend tests
test-frontend  # Run frontend tests
```

### Code Quality
```bash
lint        # Run linting on both backend and frontend
format      # Format code in both backend and frontend
```

### Docker Commands
```bash
dc          # docker-compose
dcup        # docker-compose up
dcdown      # docker-compose down
dcbuild     # docker-compose build
dclogs      # docker-compose logs -f
```

### Git Commands
```bash
gs          # git status
ga          # git add
gc          # git commit
gp          # git push
gl          # git pull
gb          # git branch
gco         # git checkout
gd          # git diff
glog        # git log --oneline --graph --decorate
```

## 🔧 Customization

### Adding Extensions
Edit `.devcontainer/devcontainer.json`:
```json
{
  "customizations": {
    "vscode": {
      "extensions": [
        "existing.extension",
        "new.extension.id"
      ]
    }
  }
}
```

### Adding Dependencies
Edit the appropriate requirements file:
- **Python**: `.devcontainer/requirements.dev.txt`
- **Node.js**: `frontend/package.json`

### Custom Scripts
Add scripts to `.devcontainer/scripts/` and make them executable:
```bash
chmod +x .devcontainer/scripts/your-script.sh
```

## 🐛 Troubleshooting

### Container Won't Start
1. **Check Docker**: Ensure Docker is running
2. **Rebuild**: Try "Remote-Containers: Rebuild Container"
3. **Clean up**: Remove old containers and images
4. **Check logs**: Look at Docker logs for errors

### Port Conflicts
```bash
# Check what's using a port
lsof -i :8000

# Kill process using port
kill -9 <PID>
```

### Permission Issues
```bash
# Fix ownership issues
sudo chown -R vscode:vscode /workspace

# Fix script permissions
chmod +x .devcontainer/scripts/*.sh
```

### Database Connection Issues
```bash
# Check PostgreSQL status
pg_isready -h postgres -p 5432

# Check Redis status
redis-cli -h redis ping

# Restart services
docker-compose restart postgres redis
```

## 🔄 Updates and Maintenance

### Updating the Container
1. **Pull latest changes**: `git pull origin main`
2. **Rebuild container**: "Remote-Containers: Rebuild Container"
3. **Update dependencies**: Run post-create script manually if needed

### Adding New Features
1. **Update configuration**: Modify `devcontainer.json`
2. **Add dependencies**: Update requirements files
3. **Update scripts**: Enhance setup scripts
4. **Test changes**: Rebuild and test the container
5. **Document changes**: Update this README

## 📊 Performance Tips

### Faster Startup
- Use Docker volume mounts for node_modules
- Cache dependencies in Docker layers
- Use .dockerignore to exclude unnecessary files

### Resource Management
- Allocate sufficient memory to Docker
- Use multi-stage builds for smaller images
- Clean up unused containers and images regularly

## 🤝 Contributing

### Making Changes
1. **Test locally**: Ensure changes work in your environment
2. **Update documentation**: Keep README up to date
3. **Test on different platforms**: Windows, Mac, Linux
4. **Submit PR**: Include description of changes

### Best Practices
- Keep container size reasonable
- Use official base images when possible
- Document all custom configurations
- Test with fresh container builds
- Consider different development workflows

## 📚 Additional Resources

- [VS Code Dev Containers Documentation](https://code.visualstudio.com/docs/remote/containers)
- [Dev Container Specification](https://containers.dev/)
- [Docker Documentation](https://docs.docker.com/)
- [Dev Container Features](https://github.com/devcontainers/features)

## 🆘 Getting Help

### Support Channels
- **GitHub Issues**: Report container-related problems
- **Team Chat**: Ask questions about the development environment
- **Documentation**: Check the main project documentation

### Common Questions
- **Q**: Can I use this without VS Code?
  **A**: The container is optimized for VS Code, but you can use it with other editors that support dev containers.

- **Q**: How do I add a new service?
  **A**: Update `docker-compose.dev.yml` and `devcontainer.json` port forwarding.

- **Q**: Can I customize the shell?
  **A**: Yes, modify the post-create script to install your preferred shell configuration.
