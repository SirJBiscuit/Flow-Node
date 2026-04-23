import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QTextEdit,
                             QSplitter, QComboBox, QLabel, QSpinBox, QColorDialog,
                             QGroupBox, QScrollArea, QLineEdit, QListWidget, QListWidgetItem,
                             QMenuBar, QMenu, QAction, QFileDialog, QDialog, QCheckBox,
                             QMessageBox, QToolButton, QGridLayout, QFrame, QSlider)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl, QSize
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
from components import ComponentLibrary

class ComponentPreviewWidget(QFrame):
    """Widget to display a component preview"""
    def __init__(self, name, component_data, parent=None):
        super().__init__(parent)
        self.name = name
        self.component_data = component_data
        self.setFrameStyle(QFrame.Box | QFrame.Raised)
        self.setLineWidth(2)
        self.setCursor(Qt.PointingHandCursor)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        
        # Component name
        name_label = QLabel(name)
        name_label.setFont(QFont("Arial", 11, QFont.Bold))
        name_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(name_label)
        
        # Preview description
        preview_label = QLabel(component_data['preview'])
        preview_label.setWordWrap(True)
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet("color: #666; font-size: 10px;")
        layout.addWidget(preview_label)
        
        # Hover effect
        self.setStyleSheet("""
            ComponentPreviewWidget {
                background: white;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
            }
            ComponentPreviewWidget:hover {
                border-color: #667eea;
                background: #f8f9ff;
            }
        """)

class CustomizationPanel(QGroupBox):
    """Panel for customizing component properties"""
    def __init__(self, parent=None):
        super().__init__("🎨 Customize Component", parent)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(10)
        
        # Text/Content
        text_group = QGroupBox("📝 Content")
        text_layout = QVBoxLayout()
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Button text, title, etc...")
        text_layout.addWidget(self.text_input)
        text_group.setLayout(text_layout)
        layout.addWidget(text_group)
        
        # Size
        size_group = QGroupBox("📏 Size")
        size_layout = QVBoxLayout()
        
        self.size_combo = QComboBox()
        self.size_combo.addItems(['Small', 'Medium', 'Large', 'Extra Large'])
        self.size_combo.setCurrentIndex(1)
        size_layout.addWidget(self.size_combo)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # Color Scheme
        color_group = QGroupBox("🎨 Color Scheme")
        color_layout = QVBoxLayout()
        
        self.color_combo = QComboBox()
        self.color_combo.addItems([
            'Purple (Default)',
            'Blue',
            'Green',
            'Red',
            'Orange',
            'Pink',
            'Dark',
            'Custom...'
        ])
        color_layout.addWidget(self.color_combo)
        
        self.custom_color_btn = QPushButton("Pick Custom Color")
        self.custom_color_btn.clicked.connect(self.pick_custom_color)
        self.custom_color_btn.setVisible(False)
        color_layout.addWidget(self.custom_color_btn)
        
        self.color_combo.currentTextChanged.connect(
            lambda t: self.custom_color_btn.setVisible(t == 'Custom...')
        )
        
        color_group.setLayout(color_layout)
        layout.addWidget(color_group)
        
        # Shadow
        shadow_group = QGroupBox("💫 Shadow")
        shadow_layout = QVBoxLayout()
        
        self.shadow_check = QCheckBox("Enable Shadow")
        self.shadow_check.setChecked(True)
        shadow_layout.addWidget(self.shadow_check)
        
        shadow_intensity_layout = QHBoxLayout()
        shadow_intensity_layout.addWidget(QLabel("Intensity:"))
        self.shadow_slider = QSlider(Qt.Horizontal)
        self.shadow_slider.setRange(0, 100)
        self.shadow_slider.setValue(50)
        shadow_intensity_layout.addWidget(self.shadow_slider)
        shadow_layout.addLayout(shadow_intensity_layout)
        
        shadow_group.setLayout(shadow_layout)
        layout.addWidget(shadow_group)
        
        # Border Radius
        radius_group = QGroupBox("🔲 Corners")
        radius_layout = QVBoxLayout()
        
        radius_slider_layout = QHBoxLayout()
        radius_slider_layout.addWidget(QLabel("Roundness:"))
        self.radius_slider = QSlider(Qt.Horizontal)
        self.radius_slider.setRange(0, 50)
        self.radius_slider.setValue(8)
        self.radius_value_label = QLabel("8px")
        self.radius_slider.valueChanged.connect(
            lambda v: self.radius_value_label.setText(f"{v}px")
        )
        radius_slider_layout.addWidget(self.radius_slider)
        radius_slider_layout.addWidget(self.radius_value_label)
        radius_layout.addLayout(radius_slider_layout)
        
        radius_group.setLayout(radius_layout)
        layout.addWidget(radius_group)
        
        # Additional fields (dynamic based on component)
        self.additional_group = QGroupBox("⚙️ Additional Options")
        self.additional_layout = QVBoxLayout()
        self.additional_group.setLayout(self.additional_layout)
        layout.addWidget(self.additional_group)
        
        layout.addStretch()
        
        self.custom_color = None
        
    def pick_custom_color(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.custom_color = color.name()
            self.custom_color_btn.setStyleSheet(f"background-color: {color.name()};")
    
    def get_customization(self):
        """Get current customization settings"""
        return {
            'text': self.text_input.text() or 'Click Me',
            'size': self.size_combo.currentText(),
            'color_scheme': self.color_combo.currentText(),
            'custom_color': self.custom_color,
            'shadow': self.shadow_check.isChecked(),
            'shadow_intensity': self.shadow_slider.value(),
            'border_radius': self.radius_slider.value()
        }

class ComponentBuilderApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Component-Based Web Builder 🎨")
        self.setGeometry(100, 100, 1600, 900)
        
        self.component_library = ComponentLibrary()
        self.selected_components = []
        self.current_component = None
        
        self.init_ui()
        
    def init_ui(self):
        # Menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        
        # Main splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Component Library
        left_panel = self.create_component_library_panel()
        splitter.addWidget(left_panel)
        
        # Middle panel - Customization
        middle_panel = self.create_customization_panel()
        splitter.addWidget(middle_panel)
        
        # Right panel - Preview and Code
        right_panel = self.create_preview_panel()
        splitter.addWidget(right_panel)
        
        splitter.setSizes([400, 350, 850])
        main_layout.addWidget(splitter)
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        save_action = QAction("Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        export_action = QAction("Export HTML/CSS/JS", self)
        export_action.triggered.connect(self.export_files)
        file_menu.addAction(export_action)
        
        # Help Menu
        help_menu = menubar.addMenu("❓ Help")
        guide_action = QAction("Quick Start Guide", self)
        guide_action.triggered.connect(self.show_guide)
        help_menu.addAction(guide_action)
        
    def create_component_library_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("📦 Component Library")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Category selector
        category_layout = QHBoxLayout()
        category_layout.addWidget(QLabel("Category:"))
        self.category_combo = QComboBox()
        self.category_combo.addItems(self.component_library.get_all_components().keys())
        self.category_combo.currentTextChanged.connect(self.load_category_components)
        category_layout.addWidget(self.category_combo)
        layout.addLayout(category_layout)
        
        # Component grid
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        self.component_grid_widget = QWidget()
        self.component_grid = QGridLayout(self.component_grid_widget)
        self.component_grid.setSpacing(10)
        scroll.setWidget(self.component_grid_widget)
        
        layout.addWidget(scroll)
        
        # Load first category
        self.load_category_components(self.category_combo.currentText())
        
        return panel
    
    def load_category_components(self, category):
        """Load components for selected category"""
        # Clear existing
        while self.component_grid.count():
            item = self.component_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get components for category
        all_components = self.component_library.get_all_components()
        components = all_components.get(category, {})
        
        # Add component previews
        row, col = 0, 0
        for name, data in components.items():
            preview = ComponentPreviewWidget(name, data)
            preview.mousePressEvent = lambda e, n=name, d=data: self.select_component(n, d)
            self.component_grid.addWidget(preview, row, col)
            
            col += 1
            if col > 1:  # 2 columns
                col = 0
                row += 1
    
    def create_customization_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Title
        title = QLabel("⚙️ Customize")
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Selected component info
        self.selected_info = QLabel("Select a component to customize")
        self.selected_info.setAlignment(Qt.AlignCenter)
        self.selected_info.setStyleSheet("color: #666; padding: 10px;")
        layout.addWidget(self.selected_info)
        
        # Customization panel
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        self.customization_panel = CustomizationPanel()
        scroll.setWidget(self.customization_panel)
        layout.addWidget(scroll)
        
        # Add button
        self.add_btn = QPushButton("➕ Add to Page")
        self.add_btn.setStyleSheet("""
            QPushButton {
                background: #667eea;
                color: white;
                border: none;
                padding: 12px;
                font-size: 16px;
                font-weight: bold;
                border-radius: 8px;
            }
            QPushButton:hover {
                background: #5568d3;
            }
        """)
        self.add_btn.clicked.connect(self.add_component_to_page)
        self.add_btn.setEnabled(False)
        layout.addWidget(self.add_btn)
        
        return panel
    
    def create_preview_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        
        # Tabs
        self.tab_widget = QTabWidget()
        
        # Preview tab
        preview_container = QWidget()
        preview_layout = QVBoxLayout(preview_container)
        
        # Components list
        comp_list_label = QLabel("📋 Added Components")
        comp_list_label.setFont(QFont("Arial", 11, QFont.Bold))
        preview_layout.addWidget(comp_list_label)
        
        self.components_list = QListWidget()
        self.components_list.setMaximumHeight(100)
        preview_layout.addWidget(self.components_list)
        
        # Preview
        self.preview_widget = QWebEngineView()
        preview_layout.addWidget(self.preview_widget)
        
        self.tab_widget.addTab(preview_container, "🖥️ Preview")
        
        # HTML tab
        self.html_editor = QTextEdit()
        self.html_editor.setFont(QFont("Consolas", 10))
        self.html_editor.setReadOnly(True)
        html_container = self.create_code_tab(self.html_editor, "HTML")
        self.tab_widget.addTab(html_container, "📄 HTML")
        
        # CSS tab
        self.css_editor = QTextEdit()
        self.css_editor.setFont(QFont("Consolas", 10))
        self.css_editor.setReadOnly(True)
        css_container = self.create_code_tab(self.css_editor, "CSS")
        self.tab_widget.addTab(css_container, "🎨 CSS")
        
        layout.addWidget(self.tab_widget)
        
        self.update_preview()
        
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
    
    def select_component(self, name, data):
        """Handle component selection"""
        self.current_component = {'name': name, 'data': data}
        self.selected_info.setText(f"Selected: {name}")
        self.add_btn.setEnabled(True)
        
        # Set default text
        if 'text' in data.get('customizable', []):
            self.customization_panel.text_input.setText(name.split()[0])
    
    def add_component_to_page(self):
        """Add customized component to the page"""
        if not self.current_component:
            return
        
        customization = self.customization_panel.get_customization()
        
        # Apply customization to component
        component = self.apply_customization(
            self.current_component['data'],
            customization
        )
        
        self.selected_components.append({
            'name': self.current_component['name'],
            'html': component['html'],
            'css': component['css'],
            'customization': customization
        })
        
        self.components_list.addItem(f"{len(self.selected_components)}. {self.current_component['name']}")
        self.update_preview()
        
        QMessageBox.information(self, "Added!", f"{self.current_component['name']} added to page!")
    
    def apply_customization(self, component_data, customization):
        """Apply customization settings to component"""
        html = component_data['html']
        css = component_data['css']
        
        # Replace placeholders
        html = html.replace('{text}', customization['text'])
        html = html.replace('{title}', customization['text'])
        html = html.replace('{placeholder}', customization['text'])
        html = html.replace('{label}', customization['text'])
        html = html.replace('{brand}', customization['text'])
        html = html.replace('{subtitle}', 'Subtitle text here')
        html = html.replace('{description}', 'Description text here')
        html = html.replace('{price}', '$99')
        html = html.replace('{icon}', '⭐')
        html = html.replace('{number}', '1,234')
        
        # Apply size modifications
        size_multipliers = {'Small': 0.8, 'Medium': 1.0, 'Large': 1.2, 'Extra Large': 1.5}
        multiplier = size_multipliers.get(customization['size'], 1.0)
        
        # Apply color scheme
        color_schemes = {
            'Purple (Default)': '#667eea',
            'Blue': '#3498db',
            'Green': '#27ae60',
            'Red': '#e74c3c',
            'Orange': '#f39c12',
            'Pink': '#e91e63',
            'Dark': '#2c3e50'
        }
        
        primary_color = color_schemes.get(customization['color_scheme'], '#667eea')
        if customization['color_scheme'] == 'Custom...' and customization['custom_color']:
            primary_color = customization['custom_color']
        
        # Replace colors in CSS
        css = css.replace('#667eea', primary_color)
        css = css.replace('#764ba2', primary_color)
        
        # Apply border radius
        if customization['border_radius'] != 8:
            import re
            css = re.sub(r'border-radius:\s*\d+px', f'border-radius: {customization["border_radius"]}px', css)
        
        # Apply shadow
        if not customization['shadow']:
            import re
            css = re.sub(r'box-shadow:[^;]+;', '', css)
        
        return {'html': html, 'css': css}
    
    def update_preview(self):
        """Update preview with all components"""
        html_parts = []
        css_parts = []
        
        for comp in self.selected_components:
            html_parts.append(comp['html'])
            css_parts.append(comp['css'])
        
        html = '\n'.join(html_parts) if html_parts else '<div style="text-align:center; padding:50px; color:#999;">Add components to see preview</div>'
        css = '\n\n'.join(css_parts)
        
        full_html = f"""<!DOCTYPE html>
<html>
<head>
    <style>
        body {{
            margin: 0;
            padding: 20px;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: #f5f5f5;
        }}
        * {{
            box-sizing: border-box;
        }}
        {css}
    </style>
</head>
<body>
    {html}
</body>
</html>"""
        
        self.preview_widget.setHtml(full_html)
        self.html_editor.setPlainText(html)
        self.css_editor.setPlainText(css)
    
    def copy_code(self, editor):
        clipboard = QApplication.clipboard()
        clipboard.setText(editor.toPlainText())
        QMessageBox.information(self, "Copied!", "Code copied to clipboard!")
    
    def new_project(self):
        self.selected_components = []
        self.components_list.clear()
        self.update_preview()
    
    def save_project(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project", "", "Web Builder Project (*.wbp)"
        )
        if file_path:
            with open(file_path, 'w') as f:
                json.dump({'components': self.selected_components}, f, indent=2)
            QMessageBox.information(self, "Saved!", "Project saved successfully!")
    
    def export_files(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if folder:
            html_parts = [comp['html'] for comp in self.selected_components]
            css_parts = [comp['css'] for comp in self.selected_components]
            
            full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>My Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {chr(10).join(html_parts)}
</body>
</html>"""
            
            css = f"""* {{
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}}

body {{
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}}

{chr(10).join(css_parts)}"""
            
            with open(os.path.join(folder, 'index.html'), 'w') as f:
                f.write(full_html)
            with open(os.path.join(folder, 'styles.css'), 'w') as f:
                f.write(css)
            
            QMessageBox.information(self, "Exported!", f"Files exported to {folder}")
    
    def show_guide(self):
        guide = """
        🎨 Component-Based Web Builder - Quick Guide
        
        1. SELECT a component from the library (left panel)
        2. CUSTOMIZE it using the options (middle panel)
        3. CLICK "Add to Page" to add it
        4. VIEW your page in the Preview tab
        5. EXPORT when ready!
        
        Tips:
        - Try different color schemes
        - Adjust shadows and corners
        - Mix and match components
        - Export to get HTML/CSS files
        """
        QMessageBox.information(self, "Quick Guide", guide)

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = ComponentBuilderApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
