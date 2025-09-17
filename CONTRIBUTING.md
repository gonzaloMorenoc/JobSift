# Contributing to JobSift

We love your input! We want to make contributing to JobSift as easy and transparent as possible, whether it's:

- Reporting a bug
- Discussing the current state of the code
- Submitting a fix
- Proposing new features
- Becoming a maintainer

## Development Process

We use GitHub to host code, track issues and feature requests, and accept pull requests.

### Pull Request Process

1. **Fork** the repo and create your branch from `main`
2. **Update** tests if you've added code that should be tested
3. **Ensure** the test suite passes (`make test`)
4. **Format** your code (`make format`)
5. **Lint** your code (`make lint`)
6. **Update** documentation if needed
7. **Submit** your pull request!

### Branch Naming Convention

- `feature/description-of-feature` - for new features
- `fix/description-of-bug` - for bug fixes
- `docs/description-of-change` - for documentation updates
- `refactor/description-of-refactor` - for code refactoring

### Commit Messages

Use conventional commits format:

```
feat: add Google Calendar sync functionality
fix: resolve JWT token refresh issue
docs: update API documentation
refactor: simplify interview service logic
```

## Code Style

### Backend (Python)

- Use **Black** for formatting (`black .`)
- Use **isort** for import sorting (`isort .`)
- Follow **PEP 8** guidelines
- Use type hints where possible
- Add docstrings to public functions

### Frontend (TypeScript)

- Use **Prettier** for formatting
- Follow **ESLint** rules
- Use **TypeScript** strict mode
- Use functional components with hooks
- Follow React best practices

## Testing

- Write tests for new features
- Maintain test coverage above 80%
- Use meaningful test names
- Test both happy and error paths

### Running Tests

```bash
# All tests
make test

# Backend only
cd backend && pytest

# Frontend only  
cd frontend && npm test

# Coverage report
make test-coverage
```

## Issue Reporting

**Great Bug Reports** tend to have:

- A quick summary
- Steps to reproduce
- Expected vs actual behavior
- Screenshots (if applicable)
- Your environment (OS, browser, etc.)
- Additional context

**Use our templates** when creating issues.

## Feature Requests

We track feature requests as GitHub issues. When requesting features:

- Explain the problem this feature would solve
- Describe the solution you'd like
- Consider alternative solutions
- Add mockups or examples if helpful

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

Don't hesitate to ask! Create a discussion or reach out to the maintainers.