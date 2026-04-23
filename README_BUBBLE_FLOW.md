# Bubble Flow Web Builder 🔮

**The most intuitive way to build websites** - Connect visual nodes to create HTML, CSS, and JavaScript through a beautiful flow-based interface!

## 🎯 What is Bubble Flow?

Bubble Flow is a **node-based visual programming system** for web development. Instead of writing code or configuring properties, you:
1. **Add colorful bubble nodes** to a canvas
2. **Connect them** by dragging between bubbles
3. **Watch your website** generate automatically!

Think of it like **Scratch for web development** or **Unreal Engine Blueprints for websites**!

## ✨ Key Features

### 🎨 Smooth 60fps Performance
- **OpenGL acceleration** for buttery smooth animations
- **Smart viewport updates** - only redraws what changed
- **Device coordinate caching** for maximum performance
- **Optimized rendering** pipeline

### 🔗 Intuitive Connection System (4 Ways!)

#### Method 1: Ctrl+Click & Drag (Fastest!)
```
1. Hold Ctrl
2. Click on first bubble
3. Drag to second bubble
4. Release - Connected!
```

#### Method 2: Right-Click Menu
```
1. Right-click first bubble
2. Select "Start Connection"
3. Click second bubble
```

#### Method 3: Connect Mode Button
```
1. Click "Connect Mode" button in toolbar
2. Click first bubble
3. Click second bubble
```

#### Method 4: Context Menu
```
1. Right-click any bubble
2. Choose "Start Connection"
3. Click target bubble
```

### 💫 Beautiful Animations
- **Hover effects** - Bubbles scale up smoothly (1.0 → 1.1)
- **Drag animations** - Scale to 1.15 while dragging
- **Curved connections** - Smooth bezier curves, not straight lines
- **Live preview** - See connection line while dragging
- **Gradient bubbles** - Radial gradients on all nodes

### 🎮 Smooth Navigation
- **Drag nodes**: Left-click + drag (smooth, responsive)
- **Pan canvas**: Shift + Left-drag OR Middle-click + drag
- **Zoom**: Mouse wheel (smooth scaling)
- **Select**: Click on any bubble

## 📦 Node Categories (40+ Nodes!)

### 🌐 Structure Nodes (Blue/Purple)
- **Page Root** 🌐 - Root container for your website
- **Section** 📦 - Section containers
- **Container** 🎁 - Generic div containers
- **Header** 📌 - Header sections
- **Footer** 📍 - Footer sections

### 📝 Content Nodes (Red/Orange)
- **Text** 📝 - Paragraphs and text
- **Heading** 📰 - H1-H6 headings
- **Button** 🔘 - Interactive buttons
- **Image** 🖼️ - Images
- **Link** 🔗 - Hyperlinks
- **Input Field** 📥 - Form inputs

### 🎨 Styling Nodes (Pink/Purple)
- **Background Color** 🎨 - Set background colors
- **Text Color** ✏️ - Set text colors
- **Font Style** 🔤 - Font properties
- **Spacing** 📐 - Padding and margins
- **Border** 🔲 - Border properties
- **Shadow** 💫 - Box shadows
- **Size** 📏 - Width and height

### 📊 Layout Nodes (Green)
- **Flexbox** 📊 - Flexible box layout
- **Grid** ⊞ - CSS Grid layout
- **Center** 🎯 - Center content

### 🎴 Component Nodes (Orange/Brown)
- **Navbar** 🧭 - Navigation bars
- **Hero Section** 🎯 - Hero banners
- **Card** 🎴 - Card components
- **Form** 📋 - Form containers

### ⚡ JavaScript Nodes (Yellow/Orange)
- **Click Event** 👆 - Handle clicks
- **Show/Hide** 👁️ - Toggle visibility
- **Scroll To** ⬇️ - Smooth scrolling
- **Alert** ⚠️ - Show alerts
- **Form Submit** 📤 - Handle submissions

### 🔀 Logic Nodes (Purple/Blue)
- **If/Else** 🔀 - Conditional logic
- **Loop** 🔁 - Repeat elements
- **Variable** 📊 - Store values

## 🚀 Quick Start

### Installation
```bash
python main_bubble_flow.py
```

### Build Your First Website (2 Minutes!)

1. **Add Page Root**
   - Click "Page Root" in Structure category
   - This is your starting point

2. **Add a Header**
   - Click "Header" node
   - Drag it near Page Root

3. **Connect Them**
   - Hold Ctrl + Click Page Root
   - Drag to Header
   - Release - Connected!

4. **Add Content**
   - Click "Heading" node
   - Connect Header → Heading

5. **Add a Button**
   - Click "Button" node
   - Connect Header → Button

6. **Generate Code**
   - Click "⚡ Generate Code"
   - See your website in Preview tab!

7. **Export**
   - File → Export Code
   - Get HTML/CSS/JS files

## 🎨 Visual Features

### Gradient Bubbles
Every bubble has a beautiful radial gradient:
- Lighter in the center
- Darker on the edges
- Color-coded by category

### Smooth Curved Connections
Connections use cubic bezier curves:
- Not straight lines
- Smooth S-curves
- Easy to follow visually

### Live Connection Preview
While dragging a connection:
- See a dashed line following your cursor
- Green color (#00ff88)
- Updates in real-time at 60fps

### Hover Effects
When you hover over a bubble:
- Scales from 1.0 to 1.1
- Border thickens
- Smooth animation

### Drag Effects
When dragging a bubble:
- Scales to 1.15
- All connections update smoothly
- No lag or stuttering

## 🎯 Performance Optimizations

### 60fps Rendering
```python
# Smart viewport updates
setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)

# Device coordinate caching
setCacheMode(QGraphicsItem.DeviceCoordinateCache)

# OpenGL acceleration
setViewport(QOpenGLWidget())

# 60fps update timer
fps_timer.start(16)  # 16ms = ~60fps
```

### Smooth Animations
- Transform origin at bubble center
- Instant scale updates
- No animation lag
- Smooth bezier curves

### Optimized Connections
- Only update when nodes move
- Cached path calculations
- Minimal redraws

## 🔧 Advanced Features

### Multiple Connection Methods
Choose your preferred workflow:
- **Ctrl+Click**: Fastest for power users
- **Right-click**: Most discoverable
- **Connect Mode**: Best for beginners
- **Context Menu**: Alternative access

### Smart Connection Prevention
- Won't create duplicate connections
- Checks both directions (A→B and B→A)
- Visual feedback when connecting

### Node Properties
Right-click any node to edit:
- Text content
- IDs and classes
- Colors and sizes
- All customizable!

## 📋 Workflow Examples

### Landing Page Flow
```
Page Root
  ├─ Header
  │   ├─ Navbar
  │   └─ Hero Section
  ├─ Section
  │   ├─ Card (Feature 1)
  │   ├─ Card (Feature 2)
  │   └─ Card (Feature 3)
  └─ Footer
```

### Styled Button Flow
```
Page Root
  └─ Container
      └─ Button
          ├─ Background Color (Blue)
          ├─ Shadow (Medium)
          ├─ Border (Rounded)
          └─ Click Event → Alert
```

### Form Flow
```
Page Root
  └─ Form
      ├─ Input Field (Name)
      ├─ Input Field (Email)
      ├─ Button (Submit)
      └─ Form Submit → Alert
```

## 🎓 Learning Path

### Beginner (5 minutes)
1. Add Page Root
2. Add a few content nodes
3. Connect them
4. Generate code
5. See your website!

### Intermediate (15 minutes)
1. Build complete page structure
2. Add styling nodes
3. Use component nodes
4. Add interactivity
5. Export and deploy

### Advanced (30 minutes)
1. Complex layouts with Grid/Flexbox
2. Conditional logic with If/Else
3. Loops for repeated elements
4. Custom JavaScript interactions
5. Full website with multiple sections

## 💡 Pro Tips

### Connection Tips
- **Ctrl+Click** is fastest once you learn it
- **Right-click** when you forget the shortcut
- **Connect Mode** for teaching others
- **Live preview** shows where you're connecting

### Organization Tips
- Start with Page Root at the top
- Structure nodes flow left to right
- Styling nodes connect from the side
- Keep related nodes close together

### Performance Tips
- Canvas runs at 60fps automatically
- OpenGL acceleration enabled by default
- Smooth animations with no lag
- Hundreds of nodes with no slowdown

### Visual Tips
- Color-coded categories help navigation
- Gradient bubbles look beautiful
- Curved lines are easier to follow
- Hover effects provide feedback

## 🔮 Future Enhancements

Coming soon:
- **Delete connections** by clicking them
- **Snap to grid** for alignment
- **Auto-layout** algorithms
- **Mini-map** for large flows
- **Undo/Redo** functionality
- **Copy/Paste** nodes
- **Templates** for common patterns
- **Export as image** of your flow

## 📊 Comparison with Other Modes

| Feature | Bubble Flow | Component Builder | Element Builder |
|---------|-------------|-------------------|-----------------|
| **Speed** | ⚡⚡⚡ | ⚡⚡⚡ | ⚡ |
| **Visual** | 🎨🎨🎨 | 🎨🎨 | 🎨 |
| **Intuitive** | 😊😊😊 | 😊😊 | 🤔 |
| **Learning Curve** | 5 min | 5 min | 30 min |
| **Best For** | Visual thinkers | Quick projects | Full control |
| **Fun Factor** | 🎮🎮🎮 | 🎮🎮 | 🎮 |

## 🎯 Perfect For

- ✅ **Visual learners** - See the structure
- ✅ **Beginners** - No code needed
- ✅ **Rapid prototyping** - Quick iterations
- ✅ **Teaching** - Easy to understand
- ✅ **Planning** - Visualize before coding
- ✅ **Fun projects** - Enjoyable to use!

## 🎨 Technical Details

### Rendering
- **60fps** target framerate
- **OpenGL** acceleration
- **Smart updates** - minimal redraws
- **Antialiasing** for smooth edges

### Animations
- **Smooth scaling** on hover/drag
- **Bezier curves** for connections
- **Live preview** while connecting
- **Instant feedback** on all actions

### Performance
- **Cached rendering** for static elements
- **Optimized paths** for connections
- **Minimal scene updates** during drag
- **Hardware acceleration** when available

## 🚀 Get Started Now!

```bash
python main_bubble_flow.py
```

1. Add some bubbles
2. Connect them
3. Generate code
4. Export your website!

**It's that simple!** 🎉

---

**Built for creators who think visually** 🎨
