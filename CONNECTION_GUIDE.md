# 🔗 Node Connection Guide - Complete System

## 🎯 Three Ways to Connect Nodes

### 1️⃣ **Drag-to-Connect** (Primary Method)
**How it works:**
1. Click on a node
2. Drag **far** (50+ pixels) toward target
3. Release on target node OR empty space

**If you release on a node:**
- ✅ Instant connection created
- 🔊 Success sound plays
- 📏 Curved connection line appears

**If you release on empty space:**
- 💡 **Smart Menu Appears!**
- Shows compatible nodes you can create
- Select a node type
- New node created at cursor position
- Automatically connected!

---

### 2️⃣ **Hold-to-Wiggle** (Alternative)
**How it works:**
1. Click and **hold perfectly still** for 1 second
2. Node starts wiggling and turns green
3. All nodes lock (can't move)
4. Click target node to connect
5. OR click empty space to cancel

**Visual feedback:**
- 🎨 Green border during wiggle
- 🔄 ±10° rotation animation
- 🔒 All nodes locked
- 🔊 Rising three-tone sound

---

### 3️⃣ **Ctrl+Click** (Keyboard Method)
**How it works:**
1. Hold **Ctrl** and click source node
2. Node turns green
3. Click target node
4. Connection created!

---

## 💡 Smart Node Suggestions

When you drag to empty space, the system suggests **compatible nodes** based on what you're connecting from:

### From **Page Root**:
```
━━ Structure ━━
  ➕ Header
  ➕ Section
  ➕ Footer
  ➕ Container
━━ Components ━━
  ➕ Navbar
  ➕ Hero Section
  ➕ Card
  ➕ Form
```

### From **Header**:
```
━━ Components ━━
  ➕ Navbar
━━ Content ━━
  ➕ Heading
  ➕ Text
  ➕ Image
```

### From **Section**:
```
━━ Structure ━━
  ➕ Container
━━ Content ━━
  ➕ Heading
  ➕ Text
  ➕ Button
  ➕ Image
━━ Components ━━
  ➕ Card
  ➕ Hero Section
```

### From **Container**:
```
━━ Content ━━
  ➕ Heading
  ➕ Text
  ➕ Button
  ➕ Image
  ➕ Link
━━ Layout ━━
  ➕ Flexbox
  ➕ Grid
  ➕ Center
```

### From **Navbar**:
```
━━ Content ━━
  ➕ Link
  ➕ Button
```

### From **Card**:
```
━━ Content ━━
  ➕ Heading
  ➕ Text
  ➕ Button
  ➕ Image
```

### From **Other Nodes** (Default):
```
━━ Content ━━
  ➕ Text
  ➕ Heading
  ➕ Button
━━ Structure ━━
  ➕ Container
  ➕ Section
```

---

## 🎮 Movement vs Connection

### **Normal Dragging** (Move nodes)
- Click and drag **< 50 pixels**
- Node repositions
- No connection created
- Wiggle timer cancels

### **Drag-to-Connect** (Create connections)
- Click and drag **≥ 50 pixels**
- Connection mode activates
- 🔊 Connection start sound
- Release on target or empty space

### **Hold-to-Wiggle** (Alternative connection)
- Click and **don't move** (< 5 pixels)
- Hold for **1 full second**
- Wiggle activates
- Click to connect

---

## 📏 Distance Thresholds

| Movement | Behavior |
|----------|----------|
| **0-5 px** | Wiggle timer active |
| **5-49 px** | Normal drag, wiggle cancelled |
| **50+ px** | Drag-to-connect mode! |

---

## 🔊 Sound Effects

### Connection Sounds:
- **Node Pickup**: High beep (800 Hz, 50ms)
- **Connection Start**: Medium-high beep (700 Hz, 60ms)
- **Connection Complete**: Two-tone success (800→1000 Hz)
- **Node Drop**: Medium beep (600 Hz, 80ms)

### Special Sounds:
- **Wiggle Activate**: Rising three-tone (600→800→1000 Hz)
- **Node Added**: High success beep (1000 Hz, 100ms)
- **Cancel**: Low beep (400 Hz, 100ms)

---

## ✨ Smart Features

### 1. **Auto-Create & Connect**
Drag to empty space → Select node type → Instantly created and connected!

### 2. **Compatible Suggestions**
Only shows nodes that make sense to connect based on source node type.

### 3. **Visual Feedback**
- Green border during connection mode
- Wiggle animation for hold-to-connect
- Curved bezier connection lines
- Smooth 60fps animations

### 4. **Flexible Workflow**
- Drag for quick connections
- Hold for precise control
- Ctrl+Click for keyboard users
- Right-click menu for exploration

---

## 🎯 Best Practices

### For Quick Building:
1. Add **Page Root** first
2. Drag far from Page Root to empty space
3. Select **Header** from menu
4. Drag from Header to empty space
5. Select **Navbar** from menu
6. Continue building your page!

### For Precise Control:
1. Add all nodes you need first
2. Use **Hold-to-Wiggle** for careful connections
3. Nodes lock during wiggle (no accidental moves)
4. Click target when ready

### For Keyboard Users:
1. **Ctrl+Click** source node
2. Click target node
3. Fast and precise!

---

## 🐛 Troubleshooting

### Connection not creating?
**Check:**
- Did you drag far enough? (50+ pixels)
- Did you release on a node or empty space?
- Is the connection line visible during drag?

**Solution:**
- Drag further from source node
- Make sure to release on target node
- Or release on empty space to see menu

### Wiggle won't activate?
**Check:**
- Are you holding perfectly still? (< 5 pixels)
- Did you wait full 1 second?
- Console shows "Hold timer started"?

**Solution:**
- Hold mouse perfectly still
- Wait for full second
- Watch for wiggle animation

### Can't move nodes?
**Check:**
- Is wiggle mode active?
- Console shows "All nodes locked"?

**Solution:**
- Click empty space to cancel wiggle
- Or complete the connection
- Nodes will unlock automatically

---

## 🎨 Visual Indicators

### Connection Mode Active:
- ✅ Green border (4px, #00ff88)
- ✅ Dashed preview line
- ✅ Cursor shows connection intent

### Wiggle Mode Active:
- ✅ Green border
- ✅ ±10° rotation animation
- ✅ All nodes locked
- ✅ Waiting for target click

### Normal Mode:
- ✅ Standard border
- ✅ Nodes movable
- ✅ No special effects

---

## 🚀 Quick Reference

| Action | Result |
|--------|--------|
| **Drag < 50px** | Move node |
| **Drag ≥ 50px to node** | Connect nodes |
| **Drag ≥ 50px to empty** | Show create menu |
| **Hold still 1 sec** | Wiggle mode |
| **Ctrl+Click** | Start connection |
| **Right-click** | Context menu |
| **Click empty (wiggle)** | Cancel wiggle |

---

## 💪 Power User Tips

1. **Chain Creation**: Drag to empty → Select node → Drag from new node → Repeat!
2. **Batch Connections**: Add all nodes first, then connect with Ctrl+Click
3. **Visual Building**: Use drag-to-connect for intuitive flow creation
4. **Keyboard Speed**: Ctrl+Click is fastest for experienced users
5. **Exploration**: Right-click any node to see all options

---

## 🎉 Summary

The Bubble Flow connection system is designed to be:
- **Intuitive**: Drag to connect, just like drawing
- **Smart**: Suggests compatible nodes automatically
- **Flexible**: Multiple methods for different workflows
- **Visual**: Clear feedback at every step
- **Fast**: Optimized for rapid prototyping

**Just drag and build!** 🚀
