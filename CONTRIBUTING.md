# Contributing to SentinelAI

Thank you for your interest in contributing to **SentinelAI**! We welcome improvements, bug fixes, algorithmic enhancements, and documentation updates.

## Development Workflow

1. **Fork the Repository** to your own GitHub account.
2. **Clone your fork**:
   ```bash
   git clone https://github.com/<your-username>/SentinelAI.git
   cd SentinelAI
   ```
3. **Create a Feature Branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```
4. **Backend Setup**:
   ```bash
   cd sentinel-ai/backend
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```
5. **Frontend Setup**:
   ```bash
   cd sentinel-ai/frontend
   npm install
   npm run dev
   ```

## Commit Guidelines

- Use conventional commits format:
  - `feat:` for new capabilities or modules
  - `fix:` for bug fixes
  - `docs:` for documentation updates
  - `perf:` for model inference or memory optimizations
  - `refactor:` for code restructuring

## Submitting Pull Requests

- Ensure all code compiles cleanly and existing tests pass.
- Provide a clear summary of changes and attach screenshots or metrics if modifying UI/ML performance.
- Open a Pull Request against the `main` branch.
