# Contributing to Clash Royale Analyzer

Thank you for your interest in contributing! This document provides guidelines for contributing to the project.

## How to Contribute

### Reporting Bugs

1. Check if the bug has already been reported in Issues
2. Create a new issue with:
   - Clear title and description
   - Steps to reproduce
   - Expected vs actual behavior
   - Screenshots if applicable
   - System information (OS, Python/Node version)

### Suggesting Features

1. Check if the feature has been suggested
2. Create a new issue describing:
   - The feature and its benefits
   - Use cases
   - Possible implementation approach

### Code Contributions

#### Setup Development Environment

```bash
# Fork and clone the repository
git clone https://github.com/your-username/NewClashRoyaleBot.git
cd NewClashRoyaleBot

# Create a branch
git checkout -b feature/your-feature-name

# Follow SETUP.md to set up the project
```

#### Code Style

**Python (Backend)**
- Follow PEP 8
- Use type hints
- Add docstrings for functions and classes
- Run `black` for formatting
- Run `pylint` for linting

**TypeScript (Frontend)**
- Follow the existing code style
- Use TypeScript strict mode
- Add JSDoc comments for complex functions
- Run `npm run lint`

#### Making Changes

1. Make your changes
2. Test thoroughly
3. Update documentation if needed
4. Commit with clear messages:
   ```
   feat: add card synergy detection
   fix: correct win probability calculation
   docs: update setup instructions
   ```

#### Pull Request Process

1. Update README.md with any new features
2. Ensure all tests pass
3. Update CHANGELOG.md
4. Submit pull request with:
   - Clear description of changes
   - Link to related issues
   - Screenshots/videos if UI changes

### Improving Documentation

- Fix typos
- Clarify unclear sections
- Add examples
- Improve setup instructions
- Translate to other languages

### Training Better Models

Contributions to improve the card detection model are highly valuable:

1. Collect and label more training data
2. Experiment with different model architectures
3. Improve detection accuracy
4. Share your trained models

## Development Guidelines

### Project Structure

```
NewClashRoyaleBot/
├── backend/           # Python/FastAPI backend
│   ├── app/
│   │   ├── api/      # API endpoints
│   │   ├── services/ # Business logic
│   │   └── models/   # Database models
├── frontend/         # React/TypeScript frontend
│   └── src/
│       ├── components/
│       ├── pages/
│       └── services/
```

### Commit Message Format

Use conventional commits:
- `feat:` New feature
- `fix:` Bug fix
- `docs:` Documentation changes
- `style:` Code style changes
- `refactor:` Code refactoring
- `test:` Adding tests
- `chore:` Maintenance tasks

### Testing

#### Backend Tests

```bash
cd backend
pytest tests/
```

#### Frontend Tests

```bash
cd frontend
npm test
```

### Code Review

All submissions require review. We use GitHub pull requests for this purpose.

## Community

- Be respectful and inclusive
- Help others learn and improve
- Share knowledge and insights
- Follow the Code of Conduct

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Mentioned in release notes
- Given credit in documentation

## Questions?

Feel free to ask questions by:
- Creating an issue
- Joining discussions
- Reaching out to maintainers

Thank you for contributing! 🎮
