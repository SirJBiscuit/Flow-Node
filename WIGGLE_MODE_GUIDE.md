# Wiggle Mode - Complete Guide 🎯

## How to Use Hold-to-Connect

### Step-by-Step:

1. **Click and HOLD** any bubble for 3 seconds
   - Don't move mouse (20px tolerance)
   - Don't release mouse button

2. **Wiggle Activates!** 🎉
   - Bubble wiggles (±10° rotation)
   - Bubble turns GREEN
   - ALL nodes LOCK (can't move)
   - Console: "🎉 WIGGLE ACTIVATED!"

3. **Click Target Node**
   - Click any other bubble to connect
   - Connection created instantly
   - Wiggle stops
   - All nodes unlock

4. **Or Cancel**
   - Click empty space to cancel
   - Wiggle stops
   - All nodes unlock

---

## Visual Feedback

### During Hold (0-3 seconds)
- ⏱️ Timer counting down
- Normal appearance
- Can still cancel by moving or releasing

### Wiggle Active
- 🎨 **Green border** (#00ff88, 4px thick)
- 🔄 **Wiggle animation** (60fps, ±10°)
- 🔒 **All nodes locked** (can't drag ANY bubble)
- 💬 **Console messages** showing status

### After Connection
- ✅ Wiggle stops immediately
- ✅ Green highlight removed
- ✅ All nodes unlocked
- ✅ Curved connection line appears

### After Cancel
- 🚫 Wiggle stops
- 🚫 Green highlight removed
- 🚫 All nodes unlocked
- 🚫 No connection made

---

## Console Messages

You'll see these messages in the console:

```
⏱️ Hold timer started for Button - hold for 3 seconds!
✅ Hold timer completed for Button!
🎉 WIGGLE ACTIVATED for Button!
   Click another node to connect!
   Click empty space to cancel!
🔒 All nodes locked - wiggle mode active

[If you click another node:]
✅ Connected: Button → Text
🛑 Stopping wiggle for Button
✅ All nodes unlocked - can move again

[If you click empty space:]
🚫 Clicked empty space - cancelling wiggle mode
🛑 Stopping wiggle for Button
✅ All nodes unlocked - can move again
```

---

## Key Features

### 1. **All Nodes Lock During Wiggle**
- Can't drag ANY bubble while wiggle is active
- Prevents accidental movement
- Focuses on making the connection

### 2. **Green Highlight Persists**
- Source node stays green until connection made
- Easy to see which node is waiting
- Clear visual state

### 3. **Click Empty Space to Cancel**
- Don't want to connect? Just click anywhere
- Instant cancel
- Everything returns to normal

### 4. **Instant Connection**
- Click target node = immediate connection
- No second hold needed
- Fast and responsive

### 5. **20 Pixel Tolerance**
- Small mouse movements won't cancel
- More forgiving than before
- Easier to hold steady

---

## Troubleshooting

### Wiggle Won't Start?
**Check console for:**
- "❌ Hold cancelled - moved X pixels" → You moved too much
- "❌ Hold cancelled - mouse released" → You released too early

**Solution:**
- Hold perfectly still for 3 full seconds
- Don't release mouse button

### Can't Click Target Node?
**Check:**
- Is source node wiggling and green? ✅
- Are you clicking directly on target bubble? ✅
- Console shows "🔒 All nodes locked"? ✅

**Solution:**
- Click center of target bubble
- Make sure wiggle is active first

### Wiggle Won't Stop?
**Try:**
- Click empty space to cancel
- Click another node to complete connection
- Console will show "🛑 Stopping wiggle"

---

## Technical Details

### Hold Detection
```python
# 3 second timer
self.hold_timer.start(3000)

# 20 pixel movement tolerance
if distance > 20:
    cancel_hold()
```

### Wiggle Animation
```python
# 60fps smooth rotation
self.wiggle_timer.start(16)

# ±10 degree oscillation
rotation = math.sin(self.wiggle_angle) * 10
```

### Node Locking
```python
# Lock all nodes
for node in self.nodes:
    node.setFlag(QGraphicsItem.ItemIsMovable, False)

# Unlock all nodes
for node in self.nodes:
    node.setFlag(QGraphicsItem.ItemIsMovable, True)
```

### Green Highlight
```python
# Apply green border
self.setPen(QPen(QColor('#00ff88'), 4))

# Restore normal border
self.setPen(self.base_pen)
```

---

## Comparison with Other Methods

| Feature | Hold-to-Connect | Ctrl+Click | Right-Click |
|---------|----------------|------------|-------------|
| **Keyboard Required** | ❌ No | ✅ Yes | ❌ No |
| **Menu Navigation** | ❌ No | ❌ No | ✅ Yes |
| **Visual Feedback** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Speed** | ⭐⭐⭐ (3sec) | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Touch-Friendly** | ⭐⭐⭐⭐⭐ | ⭐ | ⭐⭐ |
| **Beginner-Friendly** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **Locks Nodes** | ✅ Yes | ❌ No | ❌ No |

---

## Best Practices

### When to Use Hold-to-Connect:
✅ First time using the app
✅ Teaching someone
✅ Using touchscreen
✅ No keyboard available
✅ Want clear visual feedback

### When to Use Ctrl+Click:
✅ You're a power user
✅ Making many connections quickly
✅ Keyboard is handy
✅ Speed is priority

### When to Use Right-Click:
✅ You forgot the shortcut
✅ Exploring the interface
✅ Want menu-based workflow

---

## Summary

**Hold-to-Connect is the most intuitive way to connect nodes!**

✅ No keyboard needed
✅ Clear visual feedback (wiggle + green)
✅ Locks all nodes during connection
✅ Click empty space to cancel
✅ Perfect for beginners and touchscreens

**Just hold for 3 seconds and watch the magic happen!** 🎉
