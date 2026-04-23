# GitHub Setup Instructions for Flow Node

## Step 1: Initialize Git Repository

Open a terminal in the project directory and run:

```bash
cd "C:\Users\Jeremiah Payne\CascadeProjects\WebsiteCreator"
git init
git add .
git commit -m "Initial commit: Flow Node visual web builder with bubble flow editor"
```

## Step 2: Create GitHub Repository

1. Go to https://github.com/new
2. Repository name: `flow-node`
3. Description: `Visual node-based web builder with drag-and-drop connections and auto-code generation`
4. Choose Public or Private
5. **DO NOT** initialize with README (we already have one)
6. Click "Create repository"

## Step 3: Link and Push to GitHub

After creating the repository on GitHub, run these commands:

```bash
# Add the remote repository (replace YOUR_USERNAME with your GitHub username)
git remote add origin https://github.com/YOUR_USERNAME/flow-node.git

# Push to GitHub
git branch -M main
git push -u origin main
```

## Alternative: Using GitHub CLI

If you have GitHub CLI installed:

```bash
cd "C:\Users\Jeremiah Payne\CascadeProjects\WebsiteCreator"
git init
git add .
git commit -m "Initial commit: Flow Node visual web builder"
gh repo create flow-node --public --source=. --remote=origin --push
```

## What's Included

Your repository will contain:

### Core Files
- `main_bubble_flow.py` - Flow Node visual editor
- `main.py` - Traditional element builder
- `bubble_nodes.py` - Node definitions and library
- `sounds.py` - Sound effects system
- `components.py` - Component definitions
- `main_components.py` - Component management

### Documentation
- `README.md` - Project overview and features
- `FEATURE_ROADMAP.md` - Planned features and implementation timeline
- `NEW_FEATURES_SUMMARY.md` - Detailed feature documentation
- `CONNECTION_GUIDE.md` - Connection system guide
- `HOLD_TO_CONNECT.md` - Legacy connection documentation

### Configuration
- `requirements.txt` - Python dependencies
- `.gitignore` - Git ignore rules

## Repository Description

Use this for your GitHub repository description:

```
🎨 Flow Node - Visual node-based web builder. Create HTML/CSS/JS through intuitive bubble flow interface with drag-and-drop connections, auto-code generation, hierarchy tracking, and intelligent layouts. Built with Python & PyQt5.
```

## Topics/Tags to Add

Add these topics to your GitHub repository for better discoverability:

- `visual-editor`
- `node-editor`
- `web-builder`
- `pyqt5`
- `python`
- `html-generator`
- `css-generator`
- `drag-and-drop`
- `flow-based-programming`
- `visual-programming`
- `code-generator`
- `web-development`
- `gui-application`

## After Pushing

1. Add a nice cover image/screenshot to the README
2. Create a `screenshots/` folder with demo images
3. Consider adding a demo GIF showing the flow editor in action
4. Add a LICENSE file (MIT recommended)
5. Enable GitHub Pages if you want to host documentation

## Future Updates

To push updates:

```bash
git add .
git commit -m "Description of changes"
git push
```

## Branching Strategy

Consider using branches for new features:

```bash
# Create a new feature branch
git checkout -b feature/split-view-ui

# After completing the feature
git checkout main
git merge feature/split-view-ui
git push
```

## Quick Commands Reference

```bash
# Check status
git status

# Stage all changes
git add .

# Commit changes
git commit -m "Your message"

# Push to GitHub
git push

# Pull latest changes
git pull

# View commit history
git log --oneline

# Create new branch
git checkout -b branch-name

# Switch branches
git checkout branch-name
```

---

**Ready to share your Flow Node visual web builder with the world!** 🚀
