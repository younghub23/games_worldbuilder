# Contributing to Empire Genesis

Thank you for your interest in contributing!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Follow [DEVELOPMENT_SETUP.md](DEVELOPMENT_SETUP.md)
4. Create a feature branch

## Code Style

### Unity (C#)
- Follow [Microsoft C# Coding Conventions](https://docs.microsoft.com/en-us/dotnet/csharp/programming-guide/inside-a-program/coding-conventions)
- Use PascalCase for public members
- Use camelCase for private members
- Add XML documentation for public APIs

### Backend (JavaScript/Node.js)
- Follow [Airbnb JavaScript Style Guide](https://github.com/airbnb/javascript)
- Use ESLint configuration provided
- Add JSDoc comments for functions

## Commit Messages

Format: `type: subject`

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `refactor`: Code refactoring
- `test`: Adding tests
- `chore`: Maintenance

Examples:
```
feat: Add building rotation feature
fix: Resolve resource overflow bug
docs: Update API specification
```

## Pull Request Process

1. Update documentation if needed
2. Add tests for new features
3. Ensure all tests pass
4. Update CHANGELOG.md
5. Request review from maintainers

## Testing

### Backend
```bash
cd backend
npm test
```

### Unity
- Use Unity Test Runner (Window → General → Test Runner)
- Add PlayMode tests for game logic
- Add EditMode tests for utilities

## Questions?

Open an issue or join our Discord (link in README).
