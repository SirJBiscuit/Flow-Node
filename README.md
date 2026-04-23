# Flow Node - Visual Web Builder 🎨🔗

A powerful Python-based visual node editor for web development. Create HTML, CSS, and JavaScript through an intuitive bubble flow interface with drag-and-drop connections, auto-code generation, and intelligent layout management.

## ✨ Features

### 🔗 Flow Node Editor (NEW!)
- **🎨 Bubble Flow Interface**: Visual node-based web design
- **🔌 Connection Ports**: Drag green dots to connect nodes intuitively
- **⚡ Auto-Code Generation**: Code updates automatically as you build
- **📊 Hierarchy System**: Automatic parent-child relationship tracking
- **🗑️ Trash Can Delete**: Drag nodes to delete with visual feedback
- **💡 Rich Tooltips**: Hover for helpful info and connection suggestions
- **👻 Ghost Tutorial**: Interactive guide for new users
- **🎯 Auto-Arrange**: Tree, horizontal, and vertical layout modes
- **🔊 Sound Effects**: Audio feedback for all interactions

### Core Functionality
- **🖥️ Live Preview**: See your changes in real-time in the viewport
- **🎯 Visual Element Builder**: Create elements using visual selectors and settings
- **⚡ Code Generation**: Automatically generates clean, optimized HTML, CSS, and JavaScript
- **📑 Multiple Tabs**: Switch between Preview, HTML, CSS, and JavaScript views
- **📋 Copy to Clipboard**: Easy copy buttons for each code type with confirmation

### Element Management
- **📦 Element List View**: See all your elements in an organized list
- **✏️ Edit Elements**: Click any element to load its settings and modify it
- **🗑️ Delete Elements**: Remove individual elements or clear all
- **↕️ Reorder Elements**: Move elements up/down to change their order
- **🔄 Update Elements**: Modify existing elements without recreating them

### Project Management
- **📁 New Project**: Start fresh with a clean slate
- **💾 Save Project**: Save your work as `.wbp` project files
- **📂 Open Project**: Load previously saved projects
- **💾 Save As**: Save project with a new name
- **📤 Export**: Export complete HTML/CSS/JS files ready for deployment

### Templates
- **Blank**: Start from scratch
- **Modern Landing Page**: Professional hero section with CTA
- **Dark Theme Portfolio**: Sleek dark mode portfolio layout
- **Gradient Hero Section**: Eye-catching gradient background
- **Card Grid Layout**: Responsive card-based design
- **Minimalist Blog**: Clean blog layout
- **Pricing Table**: Professional pricing plans
- **Contact Form**: Ready-to-use contact form
- **Feature Showcase**: Highlight product features

### Customization
- **🌙 Dark Mode**: Toggle dark mode for comfortable night coding
- **⚙️ Settings**: Customize app preferences
- **🎨 Compact UI**: Space-efficient interface with emoji icons
- **🔧 Advanced Controls**: Fine-tune every aspect of your elements

## 📦 Installation

1. Install Python 3.8 or higher
2. Install dependencies:
```bash
pip install -r requirements.txt
```

## 🚀 Usage

Run the application:
```bash
python main.py
```

### Quick Start Guide:

#### Creating Elements
1. **Select Element Type**: Choose from div, button, heading, paragraph, link, input, etc.
2. **Configure Settings**: 
   - **Content**: Set text content
   - **Size**: Adjust width/height in pixels
   - **Colors**: Pick background, text, and border colors
   - **Typography**: Set font size
   - **Spacing**: Configure padding and margin
   - **Border**: Customize radius, width, and color
3. **Add Element**: Click "➕ Add Element" to add it to your page
4. **View Preview**: See your element appear in the live preview

#### Managing Elements
- **Select**: Click any element in the Elements list to edit it
- **Update**: After editing, click "✏️ Update" to save changes
- **Delete**: Select an element and click "🗑️ Delete"
- **Reorder**: Use ↑ and ↓ buttons to move elements
- **Clear All**: Remove all elements (with confirmation)

#### Working with Projects
- **File Menu**:
  - `Ctrl+N`: New Project
  - `Ctrl+O`: Open Project
  - `Ctrl+S`: Save Project
  - `Ctrl+Shift+S`: Save As
  - Export HTML/CSS/JS files

#### Using Templates
- **Templates Menu**: Click any template to load pre-built designs
- Templates include complete layouts ready to customize

#### Viewing Code
- **Preview Tab**: Live website preview
- **HTML Tab**: View and copy HTML code
- **CSS Tab**: View and copy CSS styles
- **JS Tab**: View and copy JavaScript code

#### Settings
- **⚙️ Settings Menu → Preferences**:
  - Enable Dark Mode for night coding
  - Enable Auto-save (future feature)

## 🎮 Controls

### Menu Bar
- **📁 File**: New, Open, Save, Save As, Export, Exit
- **📋 Templates**: 9 pre-built templates to choose from
- **⚙️ Settings**: Preferences and customization

### Left Panel
- **📦 Elements List**: Shows all added elements
- **Element Controls**: Move up/down, delete, clear all
- **🔧 Settings Panel**: Configure element properties

### Right Panel
- **🖥️ Preview**: Live website preview
- **📄 HTML**: Generated HTML with copy button
- **🎨 CSS**: Generated CSS with copy button
- **⚡ JS**: Generated JavaScript with copy button

## 📝 Project File Format

Projects are saved as `.wbp` (Web Builder Project) files containing:
- All element configurations
- App settings (dark mode, etc.)
- JSON format for easy editing

## 🎨 Element Types

- **div**: Generic container
- **button**: Interactive button
- **heading (h1, h2, h3)**: Page headings
- **paragraph**: Text paragraphs
- **link**: Hyperlinks
- **image**: Images (placeholder)
- **input**: Text input fields
- **textarea**: Multi-line text input
- **container**: Layout container
- **section**: Page section

## 🔮 Future Enhancements

- Drag and drop element positioning
- Visual grid/flexbox layout builder
- Responsive design preview (mobile/tablet/desktop)
- Custom CSS properties editor
- Animation and transition builder
- Component library
- Import existing HTML/CSS
- Undo/redo functionality
- Keyboard shortcuts
- Code syntax highlighting
- Live collaboration

## 💡 Tips

- Use templates as starting points and customize them
- Click elements in the list to quickly edit them
- Save your work frequently with `Ctrl+S`
- Export to files when ready to deploy
- Try dark mode for comfortable night coding
- Use the Update button to modify existing elements

## 🐛 Troubleshooting

- If preview doesn't update, switch tabs to refresh
- Save projects before closing to avoid data loss
- Use Export to get standalone HTML/CSS/JS files

## 📄 Requirements

- Python 3.8+
- PyQt5 5.15.9
- PyQtWebEngine 5.15.6

## 📜 License

Free to use and modify for personal and commercial projects.
