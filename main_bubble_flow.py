import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QTextEdit,
                             QSplitter, QComboBox, QLabel, QLineEdit, QListWidget,
                             QMenu, QAction, QFileDialog, QMessageBox, QGraphicsView,
                             QGraphicsScene, QGraphicsEllipseItem, QGraphicsTextItem,
                             QGraphicsLineItem, QGraphicsItem, QScrollArea, QGroupBox,
                             QGridLayout, QFrame, QDialog, QFormLayout, QGraphicsPathItem)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QPointF, QRectF, QLineF, QPropertyAnimation, QEasingCurve, pyqtProperty, QTimer
from PyQt5.QtGui import QFont, QColor, QPen, QBrush, QPainter, QPainterPath, QRadialGradient
from bubble_nodes import BubbleNode, BubbleNodeLibrary, FlowToCodeGenerator
from sounds import SoundEffects

class TrashCanZone(QGraphicsRectItem):
    """Trash can zone for deleting nodes by dragging"""
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        
        # Visual style - semi-transparent red
        self.normal_brush = QBrush(QColor(255, 0, 0, 30))
        self.hover_brush = QBrush(QColor(255, 0, 0, 80))
        self.setBrush(self.normal_brush)
        self.setPen(QPen(QColor(255, 0, 0, 150), 2, Qt.DashLine))
        self.setZValue(-1)  # Behind nodes
        
        # Add trash icon text
        self.icon = QGraphicsTextItem("🗑️", self)
        self.icon.setDefaultTextColor(QColor(255, 255, 255, 200))
        self.icon.setFont(QFont("Arial", 32))
        self.icon.setPos(width/2 - 20, height/2 - 25)
        
        self.label = QGraphicsTextItem("Drop to Delete", self)
        self.label.setDefaultTextColor(QColor(255, 255, 255, 150))
        self.label.setFont(QFont("Arial", 10, QFont.Bold))
        self.label.setPos(width/2 - 45, height/2 + 15)
        
        self.is_hovering = False
    
    def highlight(self, active):
        """Highlight when node is hovering over"""
        if active:
            self.setBrush(self.hover_brush)
            self.setPen(QPen(QColor(255, 0, 0, 255), 3, Qt.SolidLine))
            self.icon.setScale(1.2)
            self.is_hovering = True
        else:
            self.setBrush(self.normal_brush)
            self.setPen(QPen(QColor(255, 0, 0, 150), 2, Qt.DashLine))
            self.icon.setScale(1.0)
            self.is_hovering = False

class ConnectionPort(QGraphicsEllipseItem):
    """Small draggable dot for creating connections"""
    def __init__(self, parent_node, port_type, x, y):
        super().__init__(-8, -8, 16, 16)  # 16px diameter dot
        self.parent_node = parent_node
        self.port_type = port_type  # 'input' or 'output'
        self.setParentItem(parent_node)
        self.setPos(x, y)
        
        # Visual style
        self.setPen(QPen(QColor('#ffffff'), 2))
        self.setBrush(QBrush(QColor('#00ff88')))
        self.setZValue(10)  # Above the node
        
        # Make it interactive
        self.setAcceptHoverEvents(True)
        self.setCursor(Qt.CrossCursor)
        
        # Connection state
        self.is_dragging_connection = False
        self.temp_line = None
    
    def hoverEnterEvent(self, event):
        """Highlight on hover"""
        self.setBrush(QBrush(QColor('#00ffff')))  # Cyan on hover
        self.setScale(1.3)
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Remove highlight"""
        self.setBrush(QBrush(QColor('#00ff88')))  # Green normally
        self.setScale(1.0)
        super().hoverLeaveEvent(event)
    
    def mousePressEvent(self, event):
        """Start dragging connection"""
        if event.button() == Qt.LeftButton:
            self.is_dragging_connection = True
            self.setBrush(QBrush(QColor('#ffff00')))  # Yellow when dragging
            print(f"🔌 Starting connection from {self.parent_node.node_name} ({self.port_type})")
            SoundEffects.connection_start()
            event.accept()
    
    def mouseMoveEvent(self, event):
        """Draw temporary connection line"""
        if self.is_dragging_connection:
            # Get canvas
            canvas = None
            for view in self.scene().views():
                if hasattr(view, 'show_temp_connection_from_port'):
                    canvas = view
                    break
            
            if canvas:
                start_pos = self.scenePos()
                end_pos = event.scenePos()
                canvas.show_temp_connection_from_port(start_pos, end_pos)
            
            event.accept()
    
    def mouseReleaseEvent(self, event):
        """Complete connection"""
        if event.button() == Qt.LeftButton and self.is_dragging_connection:
            self.is_dragging_connection = False
            self.setBrush(QBrush(QColor('#00ff88')))  # Back to green
            
            # Find if we released over another port
            items = self.scene().items(event.scenePos())
            for item in items:
                if isinstance(item, ConnectionPort) and item != self and item.parent_node != self.parent_node:
                    # Connect the nodes
                    print(f"🔗 Connecting {self.parent_node.node_name} to {item.parent_node.node_name}")
                    canvas = None
                    for view in self.scene().views():
                        if hasattr(view, 'create_connection'):
                            canvas = view
                            break
                    
                    if canvas:
                        canvas.create_connection(self.parent_node, item.parent_node)
                        canvas.hide_temp_connection()
                    event.accept()
                    return
            
            # No valid target found
            print(f"🚫 No valid connection target")
            canvas = None
            for view in self.scene().views():
                if hasattr(view, 'hide_temp_connection'):
                    canvas = view
                    break
            if canvas:
                canvas.hide_temp_connection()
            
            event.accept()

class BubbleNodeGraphics(QGraphicsEllipseItem):
    """Visual representation of a bubble node with smooth animations"""
    def __init__(self, node_data, node_name, x=0, y=0):
        super().__init__(-50, -50, 100, 100)
        self.node_data = node_data
        self.node_name = node_name
        self.node_id = id(self)
        
        # Animation properties
        self._scale = 1.0
        self._opacity = 1.0
        self.is_dragging = False
        self.is_connecting = False
        
        # Connection properties (simplified - ports only)
        self.is_click_dragging_connection = False
        self.is_potential_drag_connection = False
        
        # Set position
        self.setPos(x, y)
        
        # Make it movable with smooth updates
        self.setFlag(QGraphicsItem.ItemIsMovable)
        self.setFlag(QGraphicsItem.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)  # Performance boost
        
        # Connection ports (dots on the node)
        self.input_port = None  # Left side
        self.output_port = None  # Right side
        self.create_connection_ports()
        
        # Set color with gradient
        color = QColor(node_data.get('color', '#667eea'))
        gradient = QRadialGradient(0, 0, 50)
        gradient.setColorAt(0, color.lighter(120))
        gradient.setColorAt(1, color)
        self.base_brush = QBrush(gradient)
        self.setBrush(self.base_brush)
        
        # Smooth pen
        self.base_pen = QPen(QColor('#ffffff'), 3)
        self.base_pen.setCapStyle(Qt.RoundCap)
        self.setPen(self.base_pen)
        
        # Add icon and text
        self.icon_text = QGraphicsTextItem(node_data.get('icon', '●'), self)
        self.icon_text.setDefaultTextColor(QColor('#ffffff'))
        self.icon_text.setFont(QFont('Arial', 24))
        self.icon_text.setPos(-15, -20)
        self.icon_text.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)
        
        self.text_item = QGraphicsTextItem(f"{node_data.get('icon', '📦')} {node_name}", self)
        self.text_item.setDefaultTextColor(QColor('#ffffff'))
        self.text_item.setFont(QFont("Arial", 10, QFont.Bold))
        text_rect = self.text_item.boundingRect()
        self.text_item.setPos(-text_rect.width()/2, -text_rect.height()/2)
        
        # Set tooltip with helpful information
        self.setToolTip(self.create_node_tooltip())
        
        self.label_text = QGraphicsTextItem(node_name, self)
        self.label_text.setDefaultTextColor(QColor('#ffffff'))
        self.label_text.setFont(QFont('Arial', 10, QFont.Bold))
        text_width = self.label_text.boundingRect().width()
        self.label_text.setPos(-text_width/2, 15)
        self.label_text.setFlag(QGraphicsItem.ItemIgnoresTransformations, False)
        
        # Store connections
        self.connections = []
        self.connection_lines = []
        
        # Hierarchy tracking
        self.hierarchy_level = 0  # 0 = root, 1 = first level, etc.
        self.parent_nodes = []  # Nodes that connect TO this node
        self.child_nodes = []   # Nodes that this connects TO
        self.properties = node_data.get('properties', {}).copy()
        
        # Hover effect
        self.setAcceptHoverEvents(True)
        
    def hoverEnterEvent(self, event):
        """Smooth scale up on hover"""
        self.animate_scale(1.1)
        self.setPen(QPen(QColor('#ffffff'), 4))
        super().hoverEnterEvent(event)
    
    def hoverLeaveEvent(self, event):
        """Smooth scale down on hover leave"""
        if not self.is_dragging and not self.is_connecting:
            self.animate_scale(1.0)
            self.setPen(self.base_pen)
        super().hoverLeaveEvent(event)
    
    def animate_scale(self, target_scale):
        """Smooth scale animation"""
        self.setTransformOriginPoint(self.boundingRect().center())
        self.setScale(target_scale)
    
    def create_node_tooltip(self):
        """Create informative tooltip for the node"""
        description = self.node_data.get('description', 'Node element')
        
        # Build tooltip with helpful information
        tooltip = f"<b>{self.node_data.get('icon', '📦')} {self.node_name}</b><br>"
        tooltip += f"<i>{description}</i><br><br>"
        
        # Add what this node does
        generates = self.node_data.get('generates', 'element')
        tooltip += f"<b>Generates:</b> {generates}<br>"
        
        # Add connection info
        inputs = self.node_data.get('inputs', [])
        outputs = self.node_data.get('outputs', [])
        
        if inputs:
            tooltip += f"<b>Accepts:</b> {', '.join(inputs)}<br>"
        if outputs:
            tooltip += f"<b>Provides:</b> {', '.join(outputs)}<br>"
        
        # Add suggestions for what to connect
        suggestions = self.get_connection_suggestions()
        if suggestions:
            tooltip += f"<br><b>💡 Try connecting to:</b><br>"
            for suggestion in suggestions[:3]:  # Show top 3
                tooltip += f"  • {suggestion}<br>"
        
        # Add properties if any
        properties = self.node_data.get('properties', {})
        if properties:
            tooltip += f"<br><b>Properties:</b> {len(properties)} editable"
        
        return tooltip
    
    def get_connection_suggestions(self):
        """Get suggested nodes to connect to"""
        suggestions_map = {
            'Page Root': ['Header', 'Section', 'Footer', 'Navbar'],
            'Header': ['Navbar', 'Heading', 'Logo'],
            'Section': ['Container', 'Heading', 'Text', 'Card'],
            'Container': ['Text', 'Button', 'Image', 'Flexbox'],
            'Navbar': ['Link', 'Button'],
            'Card': ['Heading', 'Text', 'Button', 'Image'],
            'Heading': ['Text', 'Paragraph'],
            'Button': ['Click Event', 'Link'],
        }
        return suggestions_map.get(self.node_name, ['Container', 'Text', 'Button'])
    
    def create_connection_ports(self):
        """Create input and output connection ports (dots)"""
        # Input port on the left side
        self.input_port = ConnectionPort(self, 'input', -50, 0)
        
        # Output port on the right side
        self.output_port = ConnectionPort(self, 'output', 50, 0)
    
    
    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            # Check if we should start connection (Ctrl+Click for backward compatibility)
            if event.modifiers() & Qt.ControlModifier:
                self.start_connection_from_node()
                event.accept()
                return  # Don't start dragging
            
            # Check if canvas is in connection mode (from Ctrl+Click)
            canvas = None
            for view in self.scene().views():
                if hasattr(view, 'connection_mode'):
                    canvas = view
                    break
            
            if canvas and canvas.connection_mode:
                if canvas.connection_start:
                    # This is the target node - create connection
                    if self != canvas.connection_start:
                        source_node = canvas.connection_start
                        canvas.create_connection(source_node, self)
                        canvas.end_connection_mode()
                        event.accept()
                        return
                else:
                    # This is the start node
                    canvas.start_connection(self)
                    event.accept()
                    return
            
            # Normal click - just pickup for dragging
            self.animate_scale(1.15)
            SoundEffects.node_pickup()
        elif event.button() == Qt.RightButton:
            self.show_context_menu(event.screenPos())
            event.accept()
            return
        super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Smooth dragging with connection line updates"""
        super().mouseMoveEvent(event)
        
        # Check if over trash can
        canvas = None
        for view in self.scene().views():
            if hasattr(view, 'trash_can'):
                canvas = view
                break
        
        if canvas and canvas.trash_can:
            if canvas.trash_can.contains(self.scenePos()):
                canvas.trash_can.highlight(True)
                self.setOpacity(0.5)  # Fade node when over trash
            else:
                canvas.trash_can.highlight(False)
                self.setOpacity(1.0)
        
        # Update all connection lines
        for line in self.connection_lines:
            line.update_position()
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release with smooth animation"""
        if event.button() == Qt.LeftButton:
            # Check if released over trash can
            canvas = None
            for view in self.scene().views():
                if hasattr(view, 'trash_can'):
                    canvas = view
                    break
            
            if canvas and canvas.trash_can and canvas.trash_can.contains(self.scenePos()):
                # Delete this node!
                print(f"🗑️ Deleting {self.node_name}")
                canvas.delete_node(self)
                canvas.trash_can.highlight(False)
                event.accept()
                return
            
            self.is_dragging = False
            self.animate_scale(1.0)
            self.setPen(self.base_pen)
            self.setOpacity(1.0)  # Restore full opacity
            SoundEffects.node_drop()
        
        super().mouseReleaseEvent(event)
    
    def start_connection_from_node(self):
        """Start connection mode from this node (Ctrl+Click)"""
        # Get the canvas view
        for view in self.scene().views():
            if hasattr(view, 'start_connection'):
                view.start_connection(self)
                self.is_connecting = True
                self.setPen(QPen(QColor('#00ff88'), 4))
                break
    
    def itemChange(self, change, value):
        """Handle item changes for smooth updates"""
        if change == QGraphicsItem.ItemPositionChange:
            # Update connection lines smoothly
            for line in self.connection_lines:
                line.update_position()
        return super().itemChange(change, value)
    
    def show_compatible_nodes_menu(self, screen_pos, scene_pos, canvas):
        """Show menu of compatible nodes to create and connect"""
        menu = QMenu()
        menu.setTitle("➕ Create & Connect Node")
        
        # Get compatible node suggestions based on current node type
        suggestions = self.get_compatible_nodes()
        
        actions = {}
        for category, nodes in suggestions.items():
            if nodes:
                # Add category header
                category_action = menu.addAction(f"━━ {category} ━━")
                category_action.setEnabled(False)
                
                # Add node options
                for node_name in nodes:
                    action = menu.addAction(f"  ➕ {node_name}")
                    actions[action] = (category, node_name)
        
        # Execute menu
        selected_action = menu.exec_(screen_pos)
        
        if selected_action and selected_action in actions:
            category, node_name = actions[selected_action]
            print(f"✨ Creating {node_name} and connecting...")
            
            # Create new node at release position
            node_data = BubbleNodeLibrary.get_node_by_name(node_name)
            if node_data:
                new_node = canvas.add_bubble_node(node_name, node_data, scene_pos.x(), scene_pos.y())
                # Connect source to new node
                canvas.create_connection(self, new_node)
                SoundEffects.connection_complete()
    
    def get_compatible_nodes(self):
        """Get suggested nodes based on current node type"""
        # Define compatibility rules
        compatibility = {
            'Page Root': {
                'Structure': ['Header', 'Section', 'Footer', 'Container'],
                'Components': ['Navbar', 'Hero Section', 'Card', 'Form']
            },
            'Header': {
                'Components': ['Navbar'],
                'Content': ['Heading', 'Text', 'Image']
            },
            'Section': {
                'Structure': ['Container'],
                'Content': ['Heading', 'Text', 'Button', 'Image'],
                'Components': ['Card', 'Hero Section']
            },
            'Container': {
                'Content': ['Heading', 'Text', 'Button', 'Image', 'Link'],
                'Layout': ['Flexbox', 'Grid', 'Center']
            },
            'Navbar': {
                'Content': ['Link', 'Button']
            },
            'Card': {
                'Content': ['Heading', 'Text', 'Button', 'Image']
            }
        }
        
        # Return suggestions for this node, or general suggestions
        if self.node_name in compatibility:
            return compatibility[self.node_name]
        else:
            # Default suggestions for unknown nodes
            return {
                'Content': ['Text', 'Heading', 'Button'],
                'Structure': ['Container', 'Section']
            }
    
    def show_context_menu(self, pos):
        menu = QMenu()
        edit_action = menu.addAction("✏️ Edit Properties")
        connect_action = menu.addAction("🔗 Start Connection")
        delete_action = menu.addAction("🗑️ Delete Node")
        
        action = menu.exec_(pos)
        if action == edit_action:
            self.edit_properties()
        elif action == connect_action:
            self.start_connection_from_node()
        elif action == delete_action:
            # Remove all connections first
            for line in self.connection_lines[:]:
                self.scene().removeItem(line)
            self.scene().removeItem(self)
    
    def edit_properties(self):
        dialog = NodePropertiesDialog(self.node_name, self.properties)
        if dialog.exec_() == QDialog.Accepted:
            self.properties = dialog.get_properties()

class ConnectionLine(QGraphicsPathItem):
    """Visual representation of a connection between nodes with smooth curves"""
    def __init__(self, start_node, end_node):
        super().__init__()
        self.start_node = start_node
        self.end_node = end_node
        
        # Smooth curved pen
        pen = QPen(QColor('#667eea'), 3)
        pen.setCapStyle(Qt.RoundCap)
        pen.setJoinStyle(Qt.RoundJoin)
        self.setPen(pen)
        
        self.setZValue(-1)
        self.setCacheMode(QGraphicsItem.DeviceCoordinateCache)  # Performance boost
        
        # Add to nodes' connection lists
        start_node.connection_lines.append(self)
        end_node.connection_lines.append(self)
        
        self.update_position()
    
    def update_position(self):
        """Update curved path position based on node positions"""
        start_pos = self.start_node.scenePos()
        end_pos = self.end_node.scenePos()
        
        # Create smooth curved path
        path = QPainterPath()
        path.moveTo(start_pos)
        
        # Calculate control points for bezier curve
        dx = end_pos.x() - start_pos.x()
        dy = end_pos.y() - start_pos.y()
        
        # Control points for smooth S-curve
        ctrl1 = QPointF(start_pos.x() + dx * 0.5, start_pos.y())
        ctrl2 = QPointF(start_pos.x() + dx * 0.5, end_pos.y())
        
        path.cubicTo(ctrl1, ctrl2, end_pos)
        self.setPath(path)

class NodePropertiesDialog(QDialog):
    """Dialog to edit node properties"""
    def __init__(self, node_name, properties, parent=None):
        super().__init__(parent)
        self.setWindowTitle(f"Edit {node_name} Properties")
        self.setMinimumWidth(400)
        
        self.properties = properties.copy()
        self.inputs = {}
        
        layout = QVBoxLayout(self)
        
        # Form for properties
        form = QFormLayout()
        
        for key, value in properties.items():
            input_widget = QLineEdit(str(value))
            self.inputs[key] = input_widget
            form.addRow(f"{key.title()}:", input_widget)
        
        layout.addLayout(form)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
    
    def get_properties(self):
        """Get updated properties"""
        return {key: widget.text() for key, widget in self.inputs.items()}

class BubbleFlowCanvas(QGraphicsView):
    """Canvas for bubble flow editor with 60fps optimization"""
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)
        
        # Set scene size
        self.scene.setSceneRect(-2000, -2000, 4000, 4000)
        
        # Performance optimizations for 60fps
        self.setViewportUpdateMode(QGraphicsView.SmartViewportUpdate)  # Minimal redraws
        self.setOptimizationFlag(QGraphicsView.DontAdjustForAntialiasing, True)
        self.setRenderHint(QPainter.Antialiasing, True)
        self.setRenderHint(QPainter.SmoothPixmapTransform, True)
        self.setRenderHint(QPainter.TextAntialiasing, True)
        
        # Enable OpenGL acceleration if available (huge performance boost)
        try:
            from PyQt5.QtWidgets import QOpenGLWidget
            self.setViewport(QOpenGLWidget())
        except:
            pass  # Fallback to software rendering
        
        # Enable dragging with smooth scrolling
        self.setDragMode(QGraphicsView.NoDrag)  # We'll handle dragging manually
        self.setTransformationAnchor(QGraphicsView.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.AnchorUnderMouse)
        
        # Set smooth background
        self.setBackgroundBrush(QBrush(QColor('#2c3e50')))
        
        # Connection mode
        self.connection_mode = False
        self.connection_start = None
        self.temp_connection_line = None
        self.is_panning = False
        self.last_pan_point = QPointF()
        
        # Store all nodes and connections
        self.nodes = []
        self.connections = []
        self.ghost_nodes = []  # Tutorial ghost nodes
        
        # Auto-generation settings
        self.auto_generate = True
        self.parent_app = None  # Will be set by BubbleFlowApp
        
        # Add trash can zone in bottom-right
        self.trash_can = TrashCanZone(1700, 1700, 150, 100)
        self.scene.addItem(self.trash_can)
        
        # FPS counter (optional, for debugging)
        self.fps_timer = QTimer()
        self.fps_timer.timeout.connect(self.update_scene)
        self.fps_timer.start(16)  # ~60fps (16ms per frame)
        
        # Show tutorial on empty canvas
        self.show_tutorial_ghosts()
    
    def update_scene(self):
        """Update scene at 60fps for smooth animations"""
        # Only update if there are active animations or connections being drawn
        if self.temp_connection_line:
            self.scene.update()
    
    def show_tutorial_ghosts(self):
        """Show ghost nodes as tutorial when canvas is empty"""
        if len(self.nodes) > 0:
            return  # Don't show if there are real nodes
        
        # Create ghost text items with helpful hints
        ghost1 = QGraphicsTextItem("👈 Start here!\nDrag 'Page Root'\nfrom the library")
        ghost1.setDefaultTextColor(QColor(255, 255, 255, 100))  # Semi-transparent
        ghost1.setFont(QFont("Arial", 14, QFont.Bold))
        ghost1.setPos(-300, -50)
        self.scene.addItem(ghost1)
        self.ghost_nodes.append(ghost1)
        
        ghost2 = QGraphicsTextItem("💡 Hover over nodes\nfor helpful tooltips!")
        ghost2.setDefaultTextColor(QColor(255, 255, 255, 100))
        ghost2.setFont(QFont("Arial", 12))
        ghost2.setPos(-300, 50)
        self.scene.addItem(ghost2)
        self.ghost_nodes.append(ghost2)
        
        ghost3 = QGraphicsTextItem("🔗 Drag green dots\nto connect nodes")
        ghost3.setDefaultTextColor(QColor(0, 255, 136, 120))
        ghost3.setFont(QFont("Arial", 12, QFont.Bold))
        ghost3.setPos(100, -50)
        self.scene.addItem(ghost3)
        self.ghost_nodes.append(ghost3)
        
        # Add example flow ghost
        example = QGraphicsTextItem("Example flow:\nPage Root → Header → Navbar\n           ↓\n        Section → Container → Text")
        example.setDefaultTextColor(QColor(255, 255, 255, 80))
        example.setFont(QFont("Courier", 10))
        example.setPos(-100, 100)
        self.scene.addItem(example)
        self.ghost_nodes.append(example)
    
    def hide_tutorial_ghosts(self):
        """Remove ghost tutorial nodes"""
        for ghost in self.ghost_nodes:
            self.scene.removeItem(ghost)
        self.ghost_nodes.clear()
    
    def trigger_auto_generate(self):
        """Trigger automatic code generation"""
        if self.auto_generate and self.parent_app:
            self.parent_app.generate_code()
    
    def delete_node(self, node):
        """Delete a node and all its connections"""
        # Remove all connection lines
        for line in node.connection_lines[:]:
            self.scene.removeItem(line)
            # Remove from connections list
            self.connections = [c for c in self.connections if c['line'] != line]
        
        # Remove from other nodes' connection lists
        for other_node in self.nodes:
            if node in other_node.connections:
                other_node.connections.remove(node)
            # Remove connection lines that reference this node
            other_node.connection_lines = [l for l in other_node.connection_lines if l not in node.connection_lines]
        
        # Remove from scene and nodes list
        self.scene.removeItem(node)
        if node in self.nodes:
            self.nodes.remove(node)
        
        print(f"✅ Deleted {node.node_name}")
        
        # Auto-generate code after deletion
        self.trigger_auto_generate()
    
    def auto_arrange_tree(self):
        """Arrange nodes in tree layout (top to bottom, hierarchical)"""
        print("🌳 Arranging nodes in tree layout...")
        
        # Find root nodes (hierarchy level 0)
        root_nodes = [n for n in self.nodes if n.hierarchy_level == 0]
        if not root_nodes:
            root_nodes = [self.nodes[0]] if self.nodes else []
        
        # Group nodes by hierarchy level
        levels = {}
        for node in self.nodes:
            level = node.hierarchy_level
            if level not in levels:
                levels[level] = []
            levels[level].append(node)
        
        # Arrange each level
        y_spacing = 200
        x_spacing = 250
        start_y = -400
        
        for level, nodes_in_level in sorted(levels.items()):
            y = start_y + (level * y_spacing)
            total_width = len(nodes_in_level) * x_spacing
            start_x = -total_width / 2
            
            for i, node in enumerate(nodes_in_level):
                x = start_x + (i * x_spacing)
                node.setPos(x, y)
        
        print(f"✅ Arranged {len(self.nodes)} nodes in {len(levels)} levels")
    
    def auto_arrange_horizontal(self):
        """Arrange nodes left to right"""
        print("➡️ Arranging nodes horizontally...")
        
        # Sort by hierarchy level
        sorted_nodes = sorted(self.nodes, key=lambda n: (n.hierarchy_level, n.node_name))
        
        x_spacing = 250
        y_spacing = 150
        start_x = -600
        
        for i, node in enumerate(sorted_nodes):
            x = start_x + (i * x_spacing)
            y = (i % 3) * y_spacing - y_spacing  # Stagger vertically
            node.setPos(x, y)
        
        print(f"✅ Arranged {len(self.nodes)} nodes horizontally")
    
    def auto_arrange_vertical(self):
        """Arrange nodes top to bottom"""
        print("⬇️ Arranging nodes vertically...")
        
        # Sort by hierarchy level
        sorted_nodes = sorted(self.nodes, key=lambda n: (n.hierarchy_level, n.node_name))
        
        y_spacing = 200
        x_spacing = 200
        start_y = -600
        
        for i, node in enumerate(sorted_nodes):
            y = start_y + (i * y_spacing)
            x = (i % 3) * x_spacing - x_spacing  # Stagger horizontally
            node.setPos(x, y)
        
        print(f"✅ Arranged {len(self.nodes)} nodes vertically")
    
    def add_bubble_node(self, node_name, node_data, x=0, y=0):
        """Add a new bubble node to the canvas"""
        # Hide tutorial ghosts when adding first real node
        if len(self.nodes) == 0:
            self.hide_tutorial_ghosts()
        
        bubble = BubbleNodeGraphics(node_data, node_name, x, y)
        self.scene.addItem(bubble)
        self.nodes.append(bubble)
        SoundEffects.node_added()
        
        # Auto-generate code
        self.trigger_auto_generate()
        
        return bubble
    
    def set_all_nodes_movable(self, movable):
        """Enable or disable movement for all nodes"""
        for node in self.nodes:
            node.setFlag(QGraphicsItem.ItemIsMovable, movable)
        if movable:
            print("✅ All nodes unlocked - can move again")
        else:
            print("🔒 All nodes locked - wiggle mode active")
    
    def start_connection(self, node):
        """Start creating a connection with visual feedback"""
        self.connection_mode = True
        self.connection_start = node
        node.is_connecting = True
        node.setPen(QPen(QColor('#00ff88'), 4))
    
    def mousePressEvent(self, event):
        """Handle mouse press for connection and panning"""
        item = self.itemAt(event.pos())
        
        if event.button() == Qt.MiddleButton or (event.button() == Qt.LeftButton and event.modifiers() & Qt.ShiftModifier):
            # Start panning
            self.is_panning = True
            self.last_pan_point = event.pos()
            self.setCursor(Qt.ClosedHandCursor)
            event.accept()
        elif self.connection_mode and event.button() == Qt.LeftButton:
            # If clicking ANYWHERE in viewport while in connection mode
            # Check if it's a valid target node
            if isinstance(item, BubbleNodeGraphics):
                # Let the node handle the connection
                super().mousePressEvent(event)
            else:
                # Clicking anywhere else (empty space, UI elements, etc.) cancels
                print("🚫 Clicked in viewport - cancelling wiggle mode")
                self.end_connection_mode()
                event.accept()
        else:
            super().mousePressEvent(event)
    
    def mouseMoveEvent(self, event):
        """Handle mouse move for panning and connection preview"""
        if self.is_panning:
            # Smooth panning
            delta = event.pos() - self.last_pan_point
            self.last_pan_point = event.pos()
            self.horizontalScrollBar().setValue(self.horizontalScrollBar().value() - delta.x())
            self.verticalScrollBar().setValue(self.verticalScrollBar().value() - delta.y())
            event.accept()
        elif self.connection_mode and self.connection_start:
            # Draw temporary connection line
            if self.temp_connection_line:
                self.scene.removeItem(self.temp_connection_line)
            
            start_pos = self.connection_start.scenePos()
            end_pos = self.mapToScene(event.pos())
            
            # Create temporary curved line
            path = QPainterPath()
            path.moveTo(start_pos)
            dx = end_pos.x() - start_pos.x()
            dy = end_pos.y() - start_pos.y()
            ctrl1 = QPointF(start_pos.x() + dx * 0.5, start_pos.y())
            ctrl2 = QPointF(start_pos.x() + dx * 0.5, end_pos.y())
            path.cubicTo(ctrl1, ctrl2, end_pos)
            
            self.temp_connection_line = self.scene.addPath(path, QPen(QColor('#00ff88'), 3, Qt.DashLine))
            self.temp_connection_line.setZValue(-2)
        else:
            super().mouseMoveEvent(event)
    
    def mouseReleaseEvent(self, event):
        """Handle mouse release"""
        if self.is_panning:
            self.is_panning = False
            self.setCursor(Qt.ArrowCursor)
            event.accept()
        else:
            super().mouseReleaseEvent(event)
    
    def wheelEvent(self, event):
        """Smooth zoom with mouse wheel"""
        zoom_factor = 1.15
        if event.angleDelta().y() > 0:
            self.scale(zoom_factor, zoom_factor)
        else:
            self.scale(1 / zoom_factor, 1 / zoom_factor)
    
    def end_connection_mode(self):
        """End connection mode"""
        self.connection_mode = False
        if self.connection_start:
            self.connection_start.is_connecting = False
            self.connection_start.setPen(self.connection_start.base_pen)
            self.connection_start.stop_wiggle()  # Stop wiggle animation
            self.connection_start = None
        if self.temp_connection_line:
            self.scene.removeItem(self.temp_connection_line)
            self.temp_connection_line = None
    
    def show_temp_connection_from_port(self, start_pos, end_pos):
        """Show temporary connection line when dragging from port"""
        if self.temp_connection_line:
            self.scene.removeItem(self.temp_connection_line)
        
        # Create curved line
        path = QPainterPath()
        path.moveTo(start_pos)
        
        # Control points for bezier curve
        ctrl1 = QPointF(start_pos.x() + (end_pos.x() - start_pos.x()) / 2, start_pos.y())
        ctrl2 = QPointF(start_pos.x() + (end_pos.x() - start_pos.x()) / 2, end_pos.y())
        path.cubicTo(ctrl1, ctrl2, end_pos)
        
        self.temp_connection_line = QGraphicsPathItem(path)
        self.temp_connection_line.setPen(QPen(QColor('#00ff88'), 3, Qt.DashLine))
        self.scene.addItem(self.temp_connection_line)
    
    def hide_temp_connection(self):
        """Hide temporary connection line"""
        if self.temp_connection_line:
            self.scene.removeItem(self.temp_connection_line)
            self.temp_connection_line = None
    
    def create_connection(self, start_node, end_node):
        """Create a connection between two nodes"""
        print(f"🔗 Attempting to connect: {start_node.node_name} → {end_node.node_name}")
        
        # Check if connection already exists
        for conn in self.connections:
            if (conn['from'] == start_node.node_id and conn['to'] == end_node.node_id) or \
               (conn['from'] == end_node.node_id and conn['to'] == start_node.node_id):
                print(f"⚠️ Connection already exists between {start_node.node_name} and {end_node.node_name}")
                return  # Connection already exists
        
        # Create visual connection line
        line = ConnectionLine(start_node, end_node)
        self.scene.addItem(line)
        
        # Store connection data
        self.connections.append({
            'line': line,
            'from': start_node.node_id,
            'to': end_node.node_id,
            'from_node': start_node,
            'to_node': end_node
        })
        
        # Update node connection lists (bidirectional)
        if end_node not in start_node.connections:
            start_node.connections.append(end_node)
        if start_node not in end_node.connections:
            end_node.connections.append(start_node)
        
        # Add connection line to both nodes
        start_node.connection_lines.append(line)
        end_node.connection_lines.append(line)
        
        # Update hierarchy: start_node is parent, end_node is child
        if end_node not in start_node.child_nodes:
            start_node.child_nodes.append(end_node)
        if start_node not in end_node.parent_nodes:
            end_node.parent_nodes.append(start_node)
        
        # Update hierarchy level (child is one level deeper than parent)
        if end_node.hierarchy_level <= start_node.hierarchy_level:
            end_node.hierarchy_level = start_node.hierarchy_level + 1
            print(f"   📊 Hierarchy: {start_node.node_name} (L{start_node.hierarchy_level}) → {end_node.node_name} (L{end_node.hierarchy_level})")
        
        # Visual and audio feedback
        print(f"✅ Connected: {start_node.node_name} → {end_node.node_name}")
        print(f"   Total connections: {len(self.connections)}")
        SoundEffects.connection_complete()
        
        # Auto-generate code
        self.trigger_auto_generate()
    
    def get_flow_data(self):
        """Get current flow as data"""
        nodes_data = []
        for node in self.nodes:
            node_obj = BubbleNode(
                node.node_id,
                node.node_name,
                node.scenePos().x(),
                node.scenePos().y()
            )
            node_obj.properties = node.properties
            nodes_data.append(node_obj)
        
        connections_data = [
            {'from': conn['from'], 'to': conn['to']}
            for conn in self.connections
        ]
        
        return nodes_data, connections_data
    
    def clear_canvas(self):
        """Clear all nodes and connections"""
        self.scene.clear()
        self.nodes = []
        self.connections = []

class BubbleFlowApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Bubble Flow Web Builder 🔮")
        self.setGeometry(100, 100, 1600, 900)
        
        self.node_library = BubbleNodeLibrary()
        
        self.init_ui()
        
    def init_ui(self):
        # Menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Toolbar
        toolbar = self.create_toolbar()
        main_layout.addWidget(toolbar)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Node library
        left_panel = self.create_node_library_panel()
        splitter.addWidget(left_panel)
        
        # Center - Canvas
        self.canvas = BubbleFlowCanvas()
        splitter.addWidget(self.canvas)
        
        # Right panel - Preview and code
        right_panel = self.create_preview_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([300, 800, 500])
        main_layout.addWidget(splitter)
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("New Flow", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_flow)
        file_menu.addAction(new_action)
        
        save_action = QAction("Save Flow", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_flow)
        file_menu.addAction(save_action)
        
        export_action = QAction("Export Code", self)
        export_action.triggered.connect(self.export_code)
        file_menu.addAction(export_action)
        
        # Help Menu
        help_menu = menubar.addMenu("❓ Help")
        guide_action = QAction("How to Use", self)
        guide_action.triggered.connect(self.show_help)
        help_menu.addAction(guide_action)
    
    def create_toolbar(self):
        toolbar = QWidget()
        layout = QHBoxLayout(toolbar)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("🔮 Bubble Flow Editor")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        layout.addWidget(title)
        
        # Instructions
        instructions = QLabel("💡 DRAG green dots to connect nodes | Ctrl+Click for alt method | Shift+Drag=Pan | Scroll=Zoom | 🔊 Sounds")
        instructions.setStyleSheet("color: #95a5a6; font-size: 11px;")
        layout.addWidget(instructions)
        
        layout.addStretch()
        
        # Generate button
        generate_btn = QPushButton("⚡ Generate Code")
        generate_btn.setStyleSheet("background: #667eea; color: white; padding: 8px 16px; font-weight: bold; border-radius: 4px;")
        generate_btn.setToolTip("Generate HTML/CSS/JS from your bubble flow")
        generate_btn.clicked.connect(self.generate_code)
        layout.addWidget(generate_btn)
        
        # Clear button
        clear_btn = QPushButton("🗑️ Clear All")
        clear_btn.setToolTip("Clear all nodes and connections")
        clear_btn.clicked.connect(self.clear_canvas)
        layout.addWidget(clear_btn)
        
        return toolbar
    
    def create_node_library_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("📦 Node Library")
        title.setFont(QFont("Arial", 12, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Category tabs
        self.category_tabs = QTabWidget()
        
        categories = self.node_library.get_all_categories()
        for category_name, nodes in categories.items():
            category_widget = self.create_category_widget(nodes)
            self.category_tabs.addTab(category_widget, category_name)
        
        layout.addWidget(self.category_tabs)
        
        return panel
    
    def create_category_widget(self, nodes):
        """Create widget for a category of nodes"""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        container = QWidget()
        layout = QVBoxLayout(container)
        layout.setSpacing(5)
        
        for node_name, node_data in nodes.items():
            node_btn = self.create_node_button(node_name, node_data)
            layout.addWidget(node_btn)
        
        layout.addStretch()
        scroll.setWidget(container)
        
        return scroll
    
    def create_node_button(self, node_name, node_data):
        """Create a button for a node type"""
        btn = QPushButton(f"{node_data['icon']} {node_name}")
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {node_data['color']};
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                font-weight: bold;
                border-radius: 5px;
            }}
            QPushButton:hover {{
                opacity: 0.8;
            }}
        """)
        btn.setToolTip(node_data['description'])
        btn.clicked.connect(lambda: self.add_node_to_canvas(node_name, node_data))
        return btn
    
    def add_node_to_canvas(self, node_name, node_data):
        """Add a node to the canvas"""
        # Add at center of view
        center = self.canvas.mapToScene(self.canvas.viewport().rect().center())
        self.canvas.add_bubble_node(node_name, node_data, center.x(), center.y())
    
    def create_preview_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Tabs
        self.preview_tabs = QTabWidget()
        
        # Preview tab
        self.preview_widget = QWebEngineView()
        self.preview_tabs.addTab(self.preview_widget, "🖥️ Preview")
        
        # HTML tab
        self.html_editor = QTextEdit()
        self.html_editor.setFont(QFont("Consolas", 10))
        self.html_editor.setReadOnly(True)
        html_container = self.create_code_tab(self.html_editor, "HTML")
        self.preview_tabs.addTab(html_container, "📄 HTML")
        
        # CSS tab
        self.css_editor = QTextEdit()
        self.css_editor.setFont(QFont("Consolas", 10))
        self.css_editor.setReadOnly(True)
        css_container = self.create_code_tab(self.css_editor, "CSS")
        self.preview_tabs.addTab(css_container, "🎨 CSS")
        
        # JS tab
        self.js_editor = QTextEdit()
        self.js_editor.setFont(QFont("Consolas", 10))
        self.js_editor.setReadOnly(True)
        js_container = self.create_code_tab(self.js_editor, "JS")
        self.preview_tabs.addTab(js_container, "⚡ JS")
        
        layout.addWidget(self.preview_tabs)
        
        return panel
    
    def create_code_tab(self, editor, code_type):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        copy_btn = QPushButton(f"📋 Copy {code_type}")
        copy_btn.setStyleSheet("background: #2196F3; color: white; padding: 8px; font-weight: bold;")
        copy_btn.clicked.connect(lambda: self.copy_code(editor))
        layout.addWidget(copy_btn)
        
        layout.addWidget(editor)
        return container
    
    def generate_code(self):
        """Generate code from current flow"""
        nodes, connections = self.canvas.get_flow_data()
        
        if not nodes:
            QMessageBox.warning(self, "No Nodes", "Add some nodes to the canvas first!")
            return
        
        # Generate code
        html, css, js = FlowToCodeGenerator.generate_from_flow(nodes, connections)
        
        # Update editors
        self.html_editor.setPlainText(html)
        self.css_editor.setPlainText(css)
        self.js_editor.setPlainText(js)
        
        # Update preview
        self.preview_widget.setHtml(html)
        
        QMessageBox.information(self, "Success", "Code generated successfully!")
    
    def copy_code(self, editor):
        clipboard = QApplication.clipboard()
        clipboard.setText(editor.toPlainText())
        QMessageBox.information(self, "Copied", "Code copied to clipboard!")
    
    def new_flow(self):
        reply = QMessageBox.question(self, 'New Flow', 
                                     'Clear current flow?',
                                     QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.clear_canvas()
    
    def clear_canvas(self):
        self.canvas.clear_canvas()
        self.html_editor.clear()
        self.css_editor.clear()
        self.js_editor.clear()
        self.preview_widget.setHtml("")
    
    def save_flow(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Flow", "", "Bubble Flow (*.bflow)"
        )
        if file_path:
            nodes, connections = self.canvas.get_flow_data()
            data = {
                'nodes': [n.to_dict() for n in nodes],
                'connections': connections
            }
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            QMessageBox.information(self, "Saved", "Flow saved successfully!")
    
    def export_code(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if folder:
            html = self.html_editor.toPlainText()
            css = self.css_editor.toPlainText()
            js = self.js_editor.toPlainText()
            
            if not html:
                QMessageBox.warning(self, "No Code", "Generate code first!")
                return
            
            with open(os.path.join(folder, 'index.html'), 'w') as f:
                f.write(html)
            with open(os.path.join(folder, 'styles.css'), 'w') as f:
                f.write(css)
            with open(os.path.join(folder, 'script.js'), 'w') as f:
                f.write(js)
            
            QMessageBox.information(self, "Exported", f"Files exported to {folder}")
    
    def show_help(self):
        help_text = """
🔮 Bubble Flow Web Builder - Complete Guide

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📦 ADDING NODES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Click any node button in the left panel
2. Node appears at center of view
3. Drag to position (smooth animations!)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🔗 CONNECTING NODES (3 Easy Methods!)
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Method 1: Hold-to-Connect ⭐ (EASIEST!)
   • Click and HOLD a bubble for 3 seconds
   • Node wiggles and highlights green
   • Click another node to connect
   • No keyboard, no menus!

Method 2: Ctrl+Click (FASTEST!)
   • Hold Ctrl + Click on first node
   • Click second node to connect
   • Power user favorite!

Method 3: Right-Click Menu
   • Right-click on first node
   • Select "🔗 Start Connection"
   • Click on second node
   • Most discoverable!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🖱️ NAVIGATION
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Drag nodes: Left-click + drag
• Pan canvas: Shift + Left-drag OR Middle-click + drag
• Zoom: Mouse wheel scroll
• Select: Click on node

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✏️ EDITING
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Edit properties: Right-click → "Edit Properties"
• Delete node: Right-click → "Delete Node"
• Delete connection: (coming soon)

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚡ GENERATING CODE
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
1. Build your flow with nodes
2. Connect them logically
3. Click "⚡ Generate Code"
4. View in Preview/HTML/CSS/JS tabs
5. Export when ready!

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📚 NODE CATEGORIES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Structure: Page Root, Section, Container, Header, Footer
Content: Text, Heading, Button, Image, Link, Input
Styling: Colors, Fonts, Spacing, Borders, Shadows, Size
Layout: Flexbox, Grid, Center
Components: Navbar, Hero, Card, Form
JavaScript: Click Events, Show/Hide, Scroll, Alerts
Logic: If/Else, Loops, Variables

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
💡 PRO TIPS
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
✓ Start with "Page Root" node
✓ Connect structure nodes to build hierarchy
✓ Add styling nodes to customize appearance
✓ Use component nodes for quick layouts
✓ Smooth 60fps animations for fluid experience
✓ Curved connection lines for better visibility
✓ Hover over nodes for scale animation
✓ Gradient backgrounds on all bubbles

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎨 VISUAL FEATURES
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
• Smooth 60fps rendering
• Animated node scaling on hover
• Smooth curved connection lines
• Live connection preview while dragging
• Color-coded node categories
• Gradient bubble backgrounds
• OpenGL acceleration (if available)

Enjoy building! 🚀
        """
        QMessageBox.information(self, "How to Use - Bubble Flow Editor", help_text)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = BubbleFlowApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
