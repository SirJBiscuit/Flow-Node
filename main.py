import sys
import json
import os
from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, 
                             QHBoxLayout, QPushButton, QTabWidget, QTextEdit,
                             QSplitter, QComboBox, QLabel, QSpinBox, QColorDialog,
                             QGroupBox, QScrollArea, QLineEdit, QListWidget, QListWidgetItem,
                             QMenuBar, QMenu, QAction, QFileDialog, QDialog, QCheckBox,
                             QMessageBox, QToolButton)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QFont, QColor, QPalette, QIcon
import json

class SettingsDialog(QDialog):
    def __init__(self, parent=None, current_settings=None):
        super().__init__(parent)
        self.setWindowTitle("Settings")
        self.setModal(True)
        self.setMinimumWidth(400)
        
        self.settings = current_settings or {'dark_mode': False, 'auto_save': False}
        
        layout = QVBoxLayout(self)
        
        # Dark Mode
        self.dark_mode_check = QCheckBox("Enable Dark Mode")
        self.dark_mode_check.setChecked(self.settings.get('dark_mode', False))
        layout.addWidget(self.dark_mode_check)
        
        # Auto Save
        self.auto_save_check = QCheckBox("Auto-save on changes")
        self.auto_save_check.setChecked(self.settings.get('auto_save', False))
        layout.addWidget(self.auto_save_check)
        
        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)
        
    def get_settings(self):
        return {
            'dark_mode': self.dark_mode_check.isChecked(),
            'auto_save': self.auto_save_check.isChecked()
        }

class VisualWebBuilder(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Visual Web Builder")
        self.setGeometry(100, 100, 1600, 900)
        
        # Current element settings
        self.current_settings = {
            'element_type': 'div',
            'text': 'Sample Text',
            'width': '300',
            'height': '200',
            'bg_color': '#ffffff',
            'text_color': '#000000',
            'font_size': '16',
            'padding': '10',
            'margin': '10',
            'border_radius': '0',
            'border_width': '0',
            'border_color': '#000000',
            'display': 'block',
            'align': 'left'
        }
        
        # Elements list
        self.elements = []
        
        # Selected element index
        self.selected_element_index = None
        
        # Current file path
        self.current_file = None
        
        # App settings
        self.app_settings = {'dark_mode': False, 'auto_save': False}
        
        self.init_ui()
        self.update_preview()
        
    def init_ui(self):
        # Menu bar
        self.create_menu_bar()
        
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(5)
        
        # Main content area with splitter
        splitter = QSplitter(Qt.Horizontal)
        
        # Left panel - Settings and Elements
        left_panel = self.create_left_panel()
        splitter.addWidget(left_panel)
        
        # Right panel - Preview/Code tabs
        self.tab_widget = QTabWidget()
        self.tab_widget.currentChanged.connect(self.on_tab_changed)
        
        # Preview tab
        self.preview_widget = QWebEngineView()
        self.tab_widget.addTab(self.preview_widget, "🖥️ Preview")
        
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
        
        # JavaScript tab
        self.js_editor = QTextEdit()
        self.js_editor.setFont(QFont("Consolas", 10))
        self.js_editor.setReadOnly(True)
        js_container = self.create_code_tab(self.js_editor, "JavaScript")
        self.tab_widget.addTab(js_container, "⚡ JS")
        
        splitter.addWidget(self.tab_widget)
        splitter.setSizes([350, 1250])
        
        main_layout.addWidget(splitter)
        
    def create_menu_bar(self):
        menubar = self.menuBar()
        
        # File Menu
        file_menu = menubar.addMenu("📁 File")
        
        new_action = QAction("New Project", self)
        new_action.setShortcut("Ctrl+N")
        new_action.triggered.connect(self.new_project)
        file_menu.addAction(new_action)
        
        open_action = QAction("Open Project...", self)
        open_action.setShortcut("Ctrl+O")
        open_action.triggered.connect(self.open_project)
        file_menu.addAction(open_action)
        
        save_action = QAction("Save Project", self)
        save_action.setShortcut("Ctrl+S")
        save_action.triggered.connect(self.save_project)
        file_menu.addAction(save_action)
        
        save_as_action = QAction("Save Project As...", self)
        save_as_action.setShortcut("Ctrl+Shift+S")
        save_as_action.triggered.connect(self.save_project_as)
        file_menu.addAction(save_as_action)
        
        file_menu.addSeparator()
        
        export_action = QAction("Export HTML/CSS/JS...", self)
        export_action.triggered.connect(self.export_files)
        file_menu.addAction(export_action)
        
        file_menu.addSeparator()
        
        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)
        
        # Templates Menu
        templates_menu = menubar.addMenu("📋 Templates")
        
        templates = [
            'Blank',
            'Modern Landing Page',
            'Dark Theme Portfolio',
            'Gradient Hero Section',
            'Card Grid Layout',
            'Minimalist Blog',
            'Pricing Table',
            'Contact Form',
            'Feature Showcase'
        ]
        
        for template in templates:
            action = QAction(template, self)
            action.triggered.connect(lambda checked, t=template: self.load_template(t))
            templates_menu.addAction(action)
        
        # Settings Menu
        settings_menu = menubar.addMenu("⚙️ Settings")
        
        preferences_action = QAction("Preferences...", self)
        preferences_action.triggered.connect(self.open_settings)
        settings_menu.addAction(preferences_action)
        
    def create_left_panel(self):
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(5)
        
        # Elements List Section
        elements_group = QGroupBox("📦 Elements")
        elements_layout = QVBoxLayout()
        
        self.elements_list = QListWidget()
        self.elements_list.itemClicked.connect(self.on_element_selected)
        elements_layout.addWidget(self.elements_list)
        
        # Element control buttons
        element_buttons = QHBoxLayout()
        
        move_up_btn = QPushButton("↑")
        move_up_btn.setMaximumWidth(40)
        move_up_btn.clicked.connect(self.move_element_up)
        element_buttons.addWidget(move_up_btn)
        
        move_down_btn = QPushButton("↓")
        move_down_btn.setMaximumWidth(40)
        move_down_btn.clicked.connect(self.move_element_down)
        element_buttons.addWidget(move_down_btn)
        
        delete_btn = QPushButton("🗑️ Delete")
        delete_btn.clicked.connect(self.delete_element)
        element_buttons.addWidget(delete_btn)
        
        clear_btn = QPushButton("Clear All")
        clear_btn.clicked.connect(self.clear_all)
        element_buttons.addWidget(clear_btn)
        
        elements_layout.addLayout(element_buttons)
        elements_group.setLayout(elements_layout)
        layout.addWidget(elements_group)
        
        # Settings Panel
        settings_scroll = self.create_settings_panel()
        layout.addWidget(settings_scroll)
        
        return panel
        
    def create_settings_panel(self):
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        
        panel = QWidget()
        layout = QVBoxLayout(panel)
        layout.setContentsMargins(5, 5, 5, 5)
        layout.setSpacing(3)
        
        # Element Type Group
        element_group = QGroupBox("🔧 Element Type")
        element_layout = QVBoxLayout()
        element_layout.setSpacing(3)
        
        self.element_type_combo = QComboBox()
        self.element_type_combo.addItems([
            'div', 'button', 'heading (h1)', 'heading (h2)', 'heading (h3)',
            'paragraph', 'link', 'image', 'input', 'textarea', 'container', 'section'
        ])
        self.element_type_combo.currentTextChanged.connect(self.on_setting_changed)
        element_layout.addWidget(self.element_type_combo)
        
        element_group.setLayout(element_layout)
        layout.addWidget(element_group)
        
        # Content Group
        content_group = QGroupBox("📝 Content")
        content_layout = QVBoxLayout()
        content_layout.setSpacing(3)
        
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Enter text...")
        self.text_input.setText(self.current_settings['text'])
        self.text_input.textChanged.connect(self.on_setting_changed)
        content_layout.addWidget(self.text_input)
        
        content_group.setLayout(content_layout)
        layout.addWidget(content_group)
        
        # Size Group
        size_group = QGroupBox("📏 Size")
        size_layout = QVBoxLayout()
        size_layout.setSpacing(3)
        
        width_layout = QHBoxLayout()
        width_layout.addWidget(QLabel("W:"))
        self.width_input = QLineEdit()
        self.width_input.setText(self.current_settings['width'])
        self.width_input.textChanged.connect(self.on_setting_changed)
        width_layout.addWidget(self.width_input)
        width_layout.addWidget(QLabel("px"))
        size_layout.addLayout(width_layout)
        
        height_layout = QHBoxLayout()
        height_layout.addWidget(QLabel("H:"))
        self.height_input = QLineEdit()
        self.height_input.setText(self.current_settings['height'])
        self.height_input.textChanged.connect(self.on_setting_changed)
        height_layout.addWidget(self.height_input)
        height_layout.addWidget(QLabel("px"))
        size_layout.addLayout(height_layout)
        
        size_group.setLayout(size_layout)
        layout.addWidget(size_group)
        
        # Colors Group
        colors_group = QGroupBox("🎨 Colors")
        colors_layout = QVBoxLayout()
        colors_layout.setSpacing(3)
        
        bg_layout = QHBoxLayout()
        bg_layout.addWidget(QLabel("BG:"))
        self.bg_color_btn = QPushButton()
        self.bg_color_btn.setFixedHeight(25)
        self.bg_color_btn.setStyleSheet(f"background-color: {self.current_settings['bg_color']}; border: 1px solid #ccc;")
        self.bg_color_btn.clicked.connect(lambda: self.pick_color('bg_color'))
        bg_layout.addWidget(self.bg_color_btn)
        colors_layout.addLayout(bg_layout)
        
        text_color_layout = QHBoxLayout()
        text_color_layout.addWidget(QLabel("Text:"))
        self.text_color_btn = QPushButton()
        self.text_color_btn.setFixedHeight(25)
        self.text_color_btn.setStyleSheet(f"background-color: {self.current_settings['text_color']}; border: 1px solid #ccc;")
        self.text_color_btn.clicked.connect(lambda: self.pick_color('text_color'))
        text_color_layout.addWidget(self.text_color_btn)
        colors_layout.addLayout(text_color_layout)
        
        colors_group.setLayout(colors_layout)
        layout.addWidget(colors_group)
        
        # Typography Group
        typo_group = QGroupBox("🔤 Typography")
        typo_layout = QHBoxLayout()
        typo_layout.setSpacing(3)
        
        typo_layout.addWidget(QLabel("Size:"))
        self.font_size_spin = QSpinBox()
        self.font_size_spin.setRange(8, 72)
        self.font_size_spin.setValue(int(self.current_settings['font_size']))
        self.font_size_spin.valueChanged.connect(self.on_setting_changed)
        typo_layout.addWidget(self.font_size_spin)
        typo_layout.addWidget(QLabel("px"))
        
        typo_group.setLayout(typo_layout)
        layout.addWidget(typo_group)
        
        # Spacing Group
        spacing_group = QGroupBox("📐 Spacing")
        spacing_layout = QVBoxLayout()
        spacing_layout.setSpacing(3)
        
        padding_layout = QHBoxLayout()
        padding_layout.addWidget(QLabel("Pad:"))
        self.padding_spin = QSpinBox()
        self.padding_spin.setRange(0, 100)
        self.padding_spin.setValue(int(self.current_settings['padding']))
        self.padding_spin.valueChanged.connect(self.on_setting_changed)
        padding_layout.addWidget(self.padding_spin)
        padding_layout.addWidget(QLabel("px"))
        spacing_layout.addLayout(padding_layout)
        
        margin_layout = QHBoxLayout()
        margin_layout.addWidget(QLabel("Mar:"))
        self.margin_spin = QSpinBox()
        self.margin_spin.setRange(0, 100)
        self.margin_spin.setValue(int(self.current_settings['margin']))
        self.margin_spin.valueChanged.connect(self.on_setting_changed)
        margin_layout.addWidget(self.margin_spin)
        margin_layout.addWidget(QLabel("px"))
        spacing_layout.addLayout(margin_layout)
        
        spacing_group.setLayout(spacing_layout)
        layout.addWidget(spacing_group)
        
        # Border Group
        border_group = QGroupBox("🔲 Border")
        border_layout = QVBoxLayout()
        border_layout.setSpacing(3)
        
        border_radius_layout = QHBoxLayout()
        border_radius_layout.addWidget(QLabel("Rad:"))
        self.border_radius_spin = QSpinBox()
        self.border_radius_spin.setRange(0, 50)
        self.border_radius_spin.setValue(int(self.current_settings['border_radius']))
        self.border_radius_spin.valueChanged.connect(self.on_setting_changed)
        border_radius_layout.addWidget(self.border_radius_spin)
        border_radius_layout.addWidget(QLabel("px"))
        border_layout.addLayout(border_radius_layout)
        
        border_width_layout = QHBoxLayout()
        border_width_layout.addWidget(QLabel("Width:"))
        self.border_width_spin = QSpinBox()
        self.border_width_spin.setRange(0, 20)
        self.border_width_spin.setValue(int(self.current_settings['border_width']))
        self.border_width_spin.valueChanged.connect(self.on_setting_changed)
        border_width_layout.addWidget(self.border_width_spin)
        border_width_layout.addWidget(QLabel("px"))
        border_layout.addLayout(border_width_layout)
        
        border_color_layout = QHBoxLayout()
        border_color_layout.addWidget(QLabel("Color:"))
        self.border_color_btn = QPushButton()
        self.border_color_btn.setFixedHeight(25)
        self.border_color_btn.setStyleSheet(f"background-color: {self.current_settings['border_color']}; border: 1px solid #ccc;")
        self.border_color_btn.clicked.connect(lambda: self.pick_color('border_color'))
        border_color_layout.addWidget(self.border_color_btn)
        border_layout.addLayout(border_color_layout)
        
        border_group.setLayout(border_layout)
        layout.addWidget(border_group)
        
        # Add/Update Element Button
        button_layout = QHBoxLayout()
        add_btn = QPushButton("➕ Add Element")
        add_btn.setStyleSheet("background-color: #4CAF50; color: white; padding: 8px; font-weight: bold;")
        add_btn.clicked.connect(self.add_element)
        button_layout.addWidget(add_btn)
        
        update_btn = QPushButton("✏️ Update")
        update_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px; font-weight: bold;")
        update_btn.clicked.connect(self.update_selected_element)
        button_layout.addWidget(update_btn)
        
        layout.addLayout(button_layout)
        
        layout.addStretch()
        
        scroll.setWidget(panel)
        return scroll
        
    def create_code_tab(self, editor, code_type):
        container = QWidget()
        layout = QVBoxLayout(container)
        
        # Copy button
        copy_btn = QPushButton(f"Copy {code_type} Code")
        copy_btn.setStyleSheet("background-color: #2196F3; color: white; padding: 8px;")
        copy_btn.clicked.connect(lambda: self.copy_code(editor))
        layout.addWidget(copy_btn)
        
        layout.addWidget(editor)
        
        return container
        
    def pick_color(self, color_type):
        color = QColorDialog.getColor()
        if color.isValid():
            self.current_settings[color_type] = color.name()
            if color_type == 'bg_color':
                self.bg_color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            elif color_type == 'text_color':
                self.text_color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            elif color_type == 'border_color':
                self.border_color_btn.setStyleSheet(f"background-color: {color.name()}; border: 1px solid #ccc;")
            self.on_setting_changed()
            
    def on_setting_changed(self):
        self.current_settings['element_type'] = self.element_type_combo.currentText()
        self.current_settings['text'] = self.text_input.text()
        self.current_settings['width'] = self.width_input.text()
        self.current_settings['height'] = self.height_input.text()
        self.current_settings['font_size'] = str(self.font_size_spin.value())
        self.current_settings['padding'] = str(self.padding_spin.value())
        self.current_settings['margin'] = str(self.margin_spin.value())
        self.current_settings['border_radius'] = str(self.border_radius_spin.value())
        self.current_settings['border_width'] = str(self.border_width_spin.value())
        
    def add_element(self):
        self.elements.append(self.current_settings.copy())
        self.update_elements_list()
        self.update_preview()
        
    def update_selected_element(self):
        if self.selected_element_index is not None and 0 <= self.selected_element_index < len(self.elements):
            self.elements[self.selected_element_index] = self.current_settings.copy()
            self.update_elements_list()
            self.update_preview()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an element to update.")
    
    def on_element_selected(self, item):
        self.selected_element_index = self.elements_list.row(item)
        if 0 <= self.selected_element_index < len(self.elements):
            elem = self.elements[self.selected_element_index]
            self.current_settings = elem.copy()
            self.load_settings_to_ui()
    
    def load_settings_to_ui(self):
        self.element_type_combo.setCurrentText(self.current_settings['element_type'])
        self.text_input.setText(self.current_settings['text'])
        self.width_input.setText(self.current_settings['width'])
        self.height_input.setText(self.current_settings['height'])
        self.font_size_spin.setValue(int(self.current_settings['font_size']))
        self.padding_spin.setValue(int(self.current_settings['padding']))
        self.margin_spin.setValue(int(self.current_settings['margin']))
        self.border_radius_spin.setValue(int(self.current_settings['border_radius']))
        self.border_width_spin.setValue(int(self.current_settings['border_width']))
        self.bg_color_btn.setStyleSheet(f"background-color: {self.current_settings['bg_color']}; border: 1px solid #ccc;")
        self.text_color_btn.setStyleSheet(f"background-color: {self.current_settings['text_color']}; border: 1px solid #ccc;")
        self.border_color_btn.setStyleSheet(f"background-color: {self.current_settings['border_color']}; border: 1px solid #ccc;")
    
    def delete_element(self):
        if self.selected_element_index is not None and 0 <= self.selected_element_index < len(self.elements):
            del self.elements[self.selected_element_index]
            self.selected_element_index = None
            self.update_elements_list()
            self.update_preview()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an element to delete.")
    
    def move_element_up(self):
        if self.selected_element_index is not None and self.selected_element_index > 0:
            self.elements[self.selected_element_index], self.elements[self.selected_element_index - 1] = \
                self.elements[self.selected_element_index - 1], self.elements[self.selected_element_index]
            self.selected_element_index -= 1
            self.update_elements_list()
            self.elements_list.setCurrentRow(self.selected_element_index)
            self.update_preview()
    
    def move_element_down(self):
        if self.selected_element_index is not None and self.selected_element_index < len(self.elements) - 1:
            self.elements[self.selected_element_index], self.elements[self.selected_element_index + 1] = \
                self.elements[self.selected_element_index + 1], self.elements[self.selected_element_index]
            self.selected_element_index += 1
            self.update_elements_list()
            self.elements_list.setCurrentRow(self.selected_element_index)
            self.update_preview()
    
    def update_elements_list(self):
        self.elements_list.clear()
        for i, elem in enumerate(self.elements):
            elem_type = elem['element_type'].split()[0]
            text = elem['text'][:20] + '...' if len(elem['text']) > 20 else elem['text']
            self.elements_list.addItem(f"{i+1}. {elem_type}: {text}")
        
    def clear_all(self):
        reply = QMessageBox.question(self, 'Clear All', 
                                     'Are you sure you want to clear all elements?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.elements = []
            self.selected_element_index = None
            self.update_elements_list()
            self.update_preview()
        
    def update_preview(self):
        html = self.generate_html()
        css = self.generate_css()
        js = self.generate_js()
        
        # Update code editors
        self.html_editor.setPlainText(html)
        self.css_editor.setPlainText(css)
        self.js_editor.setPlainText(js)
        
        # Update preview
        full_html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                {css}
            </style>
        </head>
        <body>
            {html}
            <script>
                {js}
            </script>
        </body>
        </html>
        """
        self.preview_widget.setHtml(full_html)
        
    def generate_html(self):
        if not self.elements:
            return "<div class='container'>\n    <h1>Add elements using the panel on the left</h1>\n</div>"
        
        html = "<div class='container'>\n"
        for i, elem in enumerate(self.elements):
            elem_type = elem['element_type'].split()[0]
            text = elem['text']
            
            if elem_type == 'heading':
                tag = elem['element_type'].split('(')[1].strip(')')
                html += f"    <{tag} class='element-{i}'>{text}</{tag}>\n"
            elif elem_type == 'paragraph':
                html += f"    <p class='element-{i}'>{text}</p>\n"
            elif elem_type == 'button':
                html += f"    <button class='element-{i}'>{text}</button>\n"
            elif elem_type == 'link':
                html += f"    <a href='#' class='element-{i}'>{text}</a>\n"
            elif elem_type == 'input':
                html += f"    <input type='text' placeholder='{text}' class='element-{i}' />\n"
            else:
                html += f"    <div class='element-{i}'>{text}</div>\n"
        
        html += "</div>"
        return html
        
    def generate_css(self):
        css = """* {
    box-sizing: border-box;
}

body {
    margin: 0;
    padding: 20px;
    font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
}

"""
        
        for i, elem in enumerate(self.elements):
            css += f""".element-{i} {{
    width: {elem['width']}px;
    height: {elem['height']}px;
    background-color: {elem['bg_color']};
    color: {elem['text_color']};
    font-size: {elem['font_size']}px;
    padding: {elem['padding']}px;
    margin: {elem['margin']}px;
    border-radius: {elem['border_radius']}px;
    border: {elem['border_width']}px solid {elem['border_color']};
    display: {elem['display']};
    text-align: {elem['align']};
}}

"""
        
        return css
        
    def generate_js(self):
        js = """// Interactive functionality
document.addEventListener('DOMContentLoaded', function() {
    // Add button click handlers
    const buttons = document.querySelectorAll('button');
    buttons.forEach(button => {
        button.addEventListener('click', function() {
            console.log('Button clicked:', this.textContent);
        });
    });
    
    // Add hover effects
    const elements = document.querySelectorAll('[class^="element-"]');
    elements.forEach(elem => {
        elem.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.02)';
            this.style.transition = 'transform 0.3s ease';
        });
        elem.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });
});
"""
        return js
        
    def load_template(self, template_name):
        self.elements = []
        
        if template_name == 'Modern Landing Page':
            self.elements = [
                {'element_type': 'heading (h1)', 'text': 'Welcome to Our Platform', 'width': '800', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#2c3e50', 'font_size': '52', 'padding': '20', 'margin': '40',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'paragraph', 'text': 'Build amazing things with our powerful tools', 'width': '700', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#7f8c8d', 'font_size': '22', 'padding': '10', 'margin': '20',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'button', 'text': 'Get Started Free', 'width': '220', 'height': '55',
                 'bg_color': '#3498db', 'text_color': '#ffffff', 'font_size': '18', 'padding': '15', 'margin': '30',
                 'border_radius': '30', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'}
            ]
        elif template_name == 'Dark Theme Portfolio':
            self.elements = [
                {'element_type': 'container', 'text': 'Portfolio', 'width': '100%', 'height': '80',
                 'bg_color': '#1a1a1a', 'text_color': '#ffffff', 'font_size': '28', 'padding': '25', 'margin': '0',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'heading (h2)', 'text': 'John Doe', 'width': '600', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#ffffff', 'font_size': '42', 'padding': '20', 'margin': '30',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'paragraph', 'text': 'Full Stack Developer & Designer', 'width': '500', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#888888', 'font_size': '20', 'padding': '10', 'margin': '10',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'}
            ]
        elif template_name == 'Gradient Hero Section':
            self.elements = [
                {'element_type': 'div', 'text': 'Transform Your Business', 'width': '100%', 'height': '500',
                 'bg_color': '#667eea', 'text_color': '#ffffff', 'font_size': '48', 'padding': '80', 'margin': '0',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'button', 'text': 'Learn More', 'width': '180', 'height': '50',
                 'bg_color': '#ffffff', 'text_color': '#667eea', 'font_size': '16', 'padding': '12', 'margin': '20',
                 'border_radius': '25', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'}
            ]
        elif template_name == 'Card Grid Layout':
            self.elements = [
                {'element_type': 'div', 'text': 'Feature One', 'width': '320', 'height': '220',
                 'bg_color': '#ffffff', 'text_color': '#2c3e50', 'font_size': '24', 'padding': '30', 'margin': '15',
                 'border_radius': '12', 'border_width': '1', 'border_color': '#e0e0e0', 'display': 'block', 'align': 'center'},
                {'element_type': 'div', 'text': 'Feature Two', 'width': '320', 'height': '220',
                 'bg_color': '#ffffff', 'text_color': '#2c3e50', 'font_size': '24', 'padding': '30', 'margin': '15',
                 'border_radius': '12', 'border_width': '1', 'border_color': '#e0e0e0', 'display': 'block', 'align': 'center'},
                {'element_type': 'div', 'text': 'Feature Three', 'width': '320', 'height': '220',
                 'bg_color': '#ffffff', 'text_color': '#2c3e50', 'font_size': '24', 'padding': '30', 'margin': '15',
                 'border_radius': '12', 'border_width': '1', 'border_color': '#e0e0e0', 'display': 'block', 'align': 'center'}
            ]
        elif template_name == 'Minimalist Blog':
            self.elements = [
                {'element_type': 'heading (h1)', 'text': 'My Blog', 'width': '700', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#000000', 'font_size': '42', 'padding': '10', 'margin': '50',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'left'},
                {'element_type': 'heading (h2)', 'text': 'Article Title', 'width': '700', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#333333', 'font_size': '32', 'padding': '10', 'margin': '20',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'left'},
                {'element_type': 'paragraph', 'text': 'This is a sample blog post excerpt...', 'width': '700', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#666666', 'font_size': '18', 'padding': '10', 'margin': '10',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'left'}
            ]
        elif template_name == 'Pricing Table':
            self.elements = [
                {'element_type': 'heading (h2)', 'text': 'Pricing Plans', 'width': '600', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#2c3e50', 'font_size': '38', 'padding': '20', 'margin': '30',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'div', 'text': 'Basic - $9/mo', 'width': '280', 'height': '350',
                 'bg_color': '#f8f9fa', 'text_color': '#2c3e50', 'font_size': '24', 'padding': '40', 'margin': '15',
                 'border_radius': '10', 'border_width': '2', 'border_color': '#dee2e6', 'display': 'block', 'align': 'center'},
                {'element_type': 'div', 'text': 'Pro - $29/mo', 'width': '280', 'height': '350',
                 'bg_color': '#3498db', 'text_color': '#ffffff', 'font_size': '24', 'padding': '40', 'margin': '15',
                 'border_radius': '10', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'}
            ]
        elif template_name == 'Contact Form':
            self.elements = [
                {'element_type': 'heading (h2)', 'text': 'Get In Touch', 'width': '500', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#2c3e50', 'font_size': '36', 'padding': '15', 'margin': '25',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'input', 'text': 'Your Name', 'width': '400', 'height': '45',
                 'bg_color': '#ffffff', 'text_color': '#333333', 'font_size': '16', 'padding': '12', 'margin': '10',
                 'border_radius': '5', 'border_width': '1', 'border_color': '#cccccc', 'display': 'block', 'align': 'left'},
                {'element_type': 'input', 'text': 'Your Email', 'width': '400', 'height': '45',
                 'bg_color': '#ffffff', 'text_color': '#333333', 'font_size': '16', 'padding': '12', 'margin': '10',
                 'border_radius': '5', 'border_width': '1', 'border_color': '#cccccc', 'display': 'block', 'align': 'left'},
                {'element_type': 'button', 'text': 'Send Message', 'width': '180', 'height': '45',
                 'bg_color': '#27ae60', 'text_color': '#ffffff', 'font_size': '16', 'padding': '12', 'margin': '15',
                 'border_radius': '5', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'}
            ]
        elif template_name == 'Feature Showcase':
            self.elements = [
                {'element_type': 'heading (h1)', 'text': 'Amazing Features', 'width': '700', 'height': 'auto',
                 'bg_color': 'transparent', 'text_color': '#2c3e50', 'font_size': '44', 'padding': '20', 'margin': '35',
                 'border_radius': '0', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'center'},
                {'element_type': 'div', 'text': '⚡ Fast Performance', 'width': '500', 'height': '100',
                 'bg_color': '#ecf0f1', 'text_color': '#2c3e50', 'font_size': '22', 'padding': '25', 'margin': '12',
                 'border_radius': '8', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'left'},
                {'element_type': 'div', 'text': '🔒 Secure & Reliable', 'width': '500', 'height': '100',
                 'bg_color': '#ecf0f1', 'text_color': '#2c3e50', 'font_size': '22', 'padding': '25', 'margin': '12',
                 'border_radius': '8', 'border_width': '0', 'border_color': '#000000', 'display': 'block', 'align': 'left'}
            ]
        
        self.update_elements_list()
        self.update_preview()
        
    def copy_code(self, editor):
        clipboard = QApplication.clipboard()
        clipboard.setText(editor.toPlainText())
        QMessageBox.information(self, "Copied", "Code copied to clipboard!")
        
    def on_tab_changed(self, index):
        if index > 0:
            self.update_preview()
    
    def new_project(self):
        if self.elements:
            reply = QMessageBox.question(self, 'New Project', 
                                         'Current project will be lost. Continue?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        
        self.elements = []
        self.selected_element_index = None
        self.current_file = None
        self.setWindowTitle("Visual Web Builder - New Project")
        self.update_elements_list()
        self.update_preview()
    
    def open_project(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Open Project", "", "Web Builder Project (*.wbp);;All Files (*)"
        )
        if file_path:
            try:
                with open(file_path, 'r') as f:
                    data = json.load(f)
                    self.elements = data.get('elements', [])
                    self.app_settings = data.get('settings', {'dark_mode': False, 'auto_save': False})
                    self.current_file = file_path
                    self.setWindowTitle(f"Visual Web Builder - {os.path.basename(file_path)}")
                    self.update_elements_list()
                    self.update_preview()
                    if self.app_settings.get('dark_mode'):
                        self.apply_dark_mode()
                    QMessageBox.information(self, "Success", "Project loaded successfully!")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to open project: {str(e)}")
    
    def save_project(self):
        if self.current_file:
            self.save_to_file(self.current_file)
        else:
            self.save_project_as()
    
    def save_project_as(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Project As", "", "Web Builder Project (*.wbp);;All Files (*)"
        )
        if file_path:
            if not file_path.endswith('.wbp'):
                file_path += '.wbp'
            self.save_to_file(file_path)
            self.current_file = file_path
            self.setWindowTitle(f"Visual Web Builder - {os.path.basename(file_path)}")
    
    def save_to_file(self, file_path):
        try:
            data = {
                'elements': self.elements,
                'settings': self.app_settings
            }
            with open(file_path, 'w') as f:
                json.dump(data, f, indent=2)
            QMessageBox.information(self, "Success", "Project saved successfully!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to save project: {str(e)}")
    
    def export_files(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Export Folder")
        if folder:
            try:
                html_content = self.generate_html()
                css_content = self.generate_css()
                js_content = self.generate_js()
                
                full_html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Exported Website</title>
    <link rel="stylesheet" href="styles.css">
</head>
<body>
    {html_content}
    <script src="script.js"></script>
</body>
</html>"""
                
                with open(os.path.join(folder, 'index.html'), 'w') as f:
                    f.write(full_html)
                with open(os.path.join(folder, 'styles.css'), 'w') as f:
                    f.write(css_content)
                with open(os.path.join(folder, 'script.js'), 'w') as f:
                    f.write(js_content)
                
                QMessageBox.information(self, "Success", f"Files exported to {folder}")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to export files: {str(e)}")
    
    def open_settings(self):
        dialog = SettingsDialog(self, self.app_settings)
        if dialog.exec_() == QDialog.Accepted:
            new_settings = dialog.get_settings()
            
            if new_settings['dark_mode'] != self.app_settings.get('dark_mode'):
                if new_settings['dark_mode']:
                    self.apply_dark_mode()
                else:
                    self.apply_light_mode()
            
            self.app_settings = new_settings
    
    def apply_dark_mode(self):
        dark_palette = QPalette()
        dark_palette.setColor(QPalette.Window, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.WindowText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Base, QColor(35, 35, 35))
        dark_palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ToolTipBase, QColor(25, 25, 25))
        dark_palette.setColor(QPalette.ToolTipText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Text, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.Button, QColor(53, 53, 53))
        dark_palette.setColor(QPalette.ButtonText, QColor(255, 255, 255))
        dark_palette.setColor(QPalette.BrightText, QColor(255, 0, 0))
        dark_palette.setColor(QPalette.Link, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
        dark_palette.setColor(QPalette.HighlightedText, QColor(35, 35, 35))
        
        QApplication.instance().setPalette(dark_palette)
    
    def apply_light_mode(self):
        QApplication.instance().setPalette(QApplication.style().standardPalette())

def main():
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    window = VisualWebBuilder()
    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
