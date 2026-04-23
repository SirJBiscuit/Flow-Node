"""
Bubble Node System - Visual flow-based web creation
"""

class BubbleNode:
    """Base class for all bubble nodes"""
    def __init__(self, node_id, node_type, x=0, y=0):
        self.id = node_id
        self.type = node_type
        self.x = x
        self.y = y
        self.inputs = []
        self.outputs = []
        self.properties = {}
        self.connections = []  # List of connected node IDs
        
    def to_dict(self):
        return {
            'id': self.id,
            'type': self.type,
            'x': self.x,
            'y': self.y,
            'properties': self.properties,
            'connections': self.connections
        }

class BubbleNodeLibrary:
    """Library of available bubble node types"""
    
    @staticmethod
    def get_all_categories():
        return {
            'Structure': BubbleNodeLibrary.get_structure_nodes(),
            'Content': BubbleNodeLibrary.get_content_nodes(),
            'Styling': BubbleNodeLibrary.get_styling_nodes(),
            'Layout': BubbleNodeLibrary.get_layout_nodes(),
            'Components': BubbleNodeLibrary.get_component_nodes(),
            'JavaScript': BubbleNodeLibrary.get_javascript_nodes(),
            'Logic': BubbleNodeLibrary.get_logic_nodes(),
        }
    
    @staticmethod
    def get_node_by_name(node_name):
        """Find node data by name across all categories"""
        all_categories = BubbleNodeLibrary.get_all_categories()
        for category_name, nodes in all_categories.items():
            if node_name in nodes:
                return nodes[node_name]
        return None
    
    @staticmethod
    def get_structure_nodes():
        """HTML Structure nodes"""
        return {
            'Page Root': {
                'color': '#667eea',
                'icon': '🌐',
                'description': 'Root page container',
                'inputs': [],
                'outputs': ['body'],
                'properties': {
                    'title': 'My Website',
                    'lang': 'en'
                },
                'generates': 'html_structure'
            },
            'Section': {
                'color': '#3498db',
                'icon': '📦',
                'description': 'Section container',
                'inputs': ['parent'],
                'outputs': ['children'],
                'properties': {
                    'id': '',
                    'class': ''
                },
                'generates': 'html_element'
            },
            'Container': {
                'color': '#2ecc71',
                'icon': '🎁',
                'description': 'Generic div container',
                'inputs': ['parent'],
                'outputs': ['children'],
                'properties': {
                    'id': '',
                    'class': 'container'
                },
                'generates': 'html_element'
            },
            'Header': {
                'color': '#9b59b6',
                'icon': '📌',
                'description': 'Header section',
                'inputs': ['parent'],
                'outputs': ['children'],
                'properties': {},
                'generates': 'html_element'
            },
            'Footer': {
                'color': '#34495e',
                'icon': '📍',
                'description': 'Footer section',
                'inputs': ['parent'],
                'outputs': ['children'],
                'properties': {},
                'generates': 'html_element'
            }
        }
    
    @staticmethod
    def get_content_nodes():
        """Content nodes"""
        return {
            'Text': {
                'color': '#e74c3c',
                'icon': '📝',
                'description': 'Text content',
                'inputs': ['parent'],
                'outputs': [],
                'properties': {
                    'text': 'Sample text',
                    'tag': 'p'
                },
                'generates': 'html_element'
            },
            'Heading': {
                'color': '#e67e22',
                'icon': '📰',
                'description': 'Heading (H1-H6)',
                'inputs': ['parent'],
                'outputs': [],
                'properties': {
                    'text': 'Heading',
                    'level': 'h1'
                },
                'generates': 'html_element'
            },
            'Button': {
                'color': '#1abc9c',
                'icon': '🔘',
                'description': 'Button element',
                'inputs': ['parent'],
                'outputs': ['onclick'],
                'properties': {
                    'text': 'Click Me',
                    'type': 'button'
                },
                'generates': 'html_element'
            },
            'Image': {
                'color': '#f39c12',
                'icon': '🖼️',
                'description': 'Image element',
                'inputs': ['parent'],
                'outputs': [],
                'properties': {
                    'src': 'image.jpg',
                    'alt': 'Image description'
                },
                'generates': 'html_element'
            },
            'Link': {
                'color': '#3498db',
                'icon': '🔗',
                'description': 'Hyperlink',
                'inputs': ['parent'],
                'outputs': [],
                'properties': {
                    'text': 'Link',
                    'href': '#'
                },
                'generates': 'html_element'
            },
            'Input Field': {
                'color': '#95a5a6',
                'icon': '📥',
                'description': 'Input field',
                'inputs': ['parent'],
                'outputs': ['value'],
                'properties': {
                    'type': 'text',
                    'placeholder': 'Enter text...'
                },
                'generates': 'html_element'
            }
        }
    
    @staticmethod
    def get_styling_nodes():
        """CSS Styling nodes"""
        return {
            'Background Color': {
                'color': '#e91e63',
                'icon': '🎨',
                'description': 'Set background color',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'color': '#ffffff'
                },
                'generates': 'css_property'
            },
            'Text Color': {
                'color': '#9c27b0',
                'icon': '✏️',
                'description': 'Set text color',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'color': '#000000'
                },
                'generates': 'css_property'
            },
            'Font Style': {
                'color': '#673ab7',
                'icon': '🔤',
                'description': 'Font properties',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'size': '16px',
                    'weight': 'normal',
                    'family': 'Arial'
                },
                'generates': 'css_property'
            },
            'Spacing': {
                'color': '#00bcd4',
                'icon': '📐',
                'description': 'Padding and margin',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'padding': '10px',
                    'margin': '10px'
                },
                'generates': 'css_property'
            },
            'Border': {
                'color': '#009688',
                'icon': '🔲',
                'description': 'Border properties',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'width': '1px',
                    'style': 'solid',
                    'color': '#000000',
                    'radius': '0px'
                },
                'generates': 'css_property'
            },
            'Shadow': {
                'color': '#607d8b',
                'icon': '💫',
                'description': 'Box shadow',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'x': '0px',
                    'y': '4px',
                    'blur': '10px',
                    'color': 'rgba(0,0,0,0.1)'
                },
                'generates': 'css_property'
            },
            'Size': {
                'color': '#ff5722',
                'icon': '📏',
                'description': 'Width and height',
                'inputs': ['element'],
                'outputs': ['styled'],
                'properties': {
                    'width': 'auto',
                    'height': 'auto'
                },
                'generates': 'css_property'
            }
        }
    
    @staticmethod
    def get_layout_nodes():
        """Layout nodes"""
        return {
            'Flexbox': {
                'color': '#4caf50',
                'icon': '📊',
                'description': 'Flexbox layout',
                'inputs': ['container'],
                'outputs': ['layout'],
                'properties': {
                    'direction': 'row',
                    'justify': 'flex-start',
                    'align': 'flex-start',
                    'gap': '10px'
                },
                'generates': 'css_layout'
            },
            'Grid': {
                'color': '#8bc34a',
                'icon': '⊞',
                'description': 'CSS Grid layout',
                'inputs': ['container'],
                'outputs': ['layout'],
                'properties': {
                    'columns': '3',
                    'rows': 'auto',
                    'gap': '20px'
                },
                'generates': 'css_layout'
            },
            'Center': {
                'color': '#cddc39',
                'icon': '🎯',
                'description': 'Center content',
                'inputs': ['element'],
                'outputs': ['centered'],
                'properties': {
                    'horizontal': True,
                    'vertical': True
                },
                'generates': 'css_layout'
            }
        }
    
    @staticmethod
    def get_component_nodes():
        """Pre-built component nodes"""
        return {
            'Navbar': {
                'color': '#ff9800',
                'icon': '🧭',
                'description': 'Navigation bar',
                'inputs': ['parent'],
                'outputs': ['children'],
                'properties': {
                    'brand': 'Brand',
                    'links': ['Home', 'About', 'Contact']
                },
                'generates': 'component'
            },
            'Hero Section': {
                'color': '#ff5722',
                'icon': '🎯',
                'description': 'Hero banner',
                'inputs': ['parent'],
                'outputs': [],
                'properties': {
                    'title': 'Welcome',
                    'subtitle': 'Subtitle text',
                    'button_text': 'Get Started'
                },
                'generates': 'component'
            },
            'Card': {
                'color': '#795548',
                'icon': '🎴',
                'description': 'Card component',
                'inputs': ['parent'],
                'outputs': ['children'],
                'properties': {
                    'title': 'Card Title',
                    'description': 'Card description'
                },
                'generates': 'component'
            },
            'Form': {
                'color': '#607d8b',
                'icon': '📋',
                'description': 'Form container',
                'inputs': ['parent'],
                'outputs': ['fields', 'submit'],
                'properties': {
                    'action': '#',
                    'method': 'post'
                },
                'generates': 'component'
            }
        }
    
    @staticmethod
    def get_javascript_nodes():
        """JavaScript nodes"""
        return {
            'Click Event': {
                'color': '#ffc107',
                'icon': '👆',
                'description': 'Handle click events',
                'inputs': ['element'],
                'outputs': ['action'],
                'properties': {},
                'generates': 'javascript'
            },
            'Show/Hide': {
                'color': '#ff9800',
                'icon': '👁️',
                'description': 'Toggle visibility',
                'inputs': ['trigger', 'target'],
                'outputs': [],
                'properties': {
                    'initial': 'visible'
                },
                'generates': 'javascript'
            },
            'Scroll To': {
                'color': '#ff5722',
                'icon': '⬇️',
                'description': 'Smooth scroll',
                'inputs': ['trigger'],
                'outputs': [],
                'properties': {
                    'target': '#section'
                },
                'generates': 'javascript'
            },
            'Alert': {
                'color': '#f44336',
                'icon': '⚠️',
                'description': 'Show alert',
                'inputs': ['trigger'],
                'outputs': [],
                'properties': {
                    'message': 'Hello!'
                },
                'generates': 'javascript'
            },
            'Form Submit': {
                'color': '#e91e63',
                'icon': '📤',
                'description': 'Handle form submission',
                'inputs': ['form'],
                'outputs': ['data'],
                'properties': {},
                'generates': 'javascript'
            }
        }
    
    @staticmethod
    def get_logic_nodes():
        """Logic and control nodes"""
        return {
            'If/Else': {
                'color': '#9c27b0',
                'icon': '🔀',
                'description': 'Conditional logic',
                'inputs': ['condition'],
                'outputs': ['true', 'false'],
                'properties': {
                    'condition': 'value > 0'
                },
                'generates': 'logic'
            },
            'Loop': {
                'color': '#673ab7',
                'icon': '🔁',
                'description': 'Repeat elements',
                'inputs': ['items'],
                'outputs': ['item'],
                'properties': {
                    'count': '3'
                },
                'generates': 'logic'
            },
            'Variable': {
                'color': '#3f51b5',
                'icon': '📊',
                'description': 'Store value',
                'inputs': [],
                'outputs': ['value'],
                'properties': {
                    'name': 'myVar',
                    'value': ''
                },
                'generates': 'logic'
            }
        }

class FlowToCodeGenerator:
    """Converts bubble flow to HTML/CSS/JS"""
    
    @staticmethod
    def generate_from_flow(nodes, connections):
        """Generate code from node flow"""
        html = FlowToCodeGenerator.generate_html(nodes, connections)
        css = FlowToCodeGenerator.generate_css(nodes, connections)
        js = FlowToCodeGenerator.generate_js(nodes, connections)
        
        return html, css, js
    
    @staticmethod
    def generate_html(nodes, connections):
        """Generate HTML from nodes"""
        # Find root node
        root_nodes = [n for n in nodes if n.type == 'Page Root']
        if not root_nodes:
            return '<div>No page root found</div>'
        
        root = root_nodes[0]
        
        # Build HTML tree
        html_parts = []
        html_parts.append('<!DOCTYPE html>')
        html_parts.append('<html lang="en">')
        html_parts.append('<head>')
        html_parts.append('    <meta charset="UTF-8">')
        html_parts.append('    <meta name="viewport" content="width=device-width, initial-scale=1.0">')
        html_parts.append(f'    <title>{root.properties.get("title", "My Website")}</title>')
        html_parts.append('    <link rel="stylesheet" href="styles.css">')
        html_parts.append('</head>')
        html_parts.append('<body>')
        
        # Generate body content from connected nodes
        body_content = FlowToCodeGenerator._generate_element_html(nodes, connections, root, indent=1)
        html_parts.append(body_content)
        
        html_parts.append('    <script src="script.js"></script>')
        html_parts.append('</body>')
        html_parts.append('</html>')
        
        return '\n'.join(html_parts)
    
    @staticmethod
    def _generate_element_html(nodes, connections, parent_node, indent=0):
        """Recursively generate HTML for elements"""
        html_parts = []
        indent_str = '    ' * indent
        
        # Find children of this node
        children = FlowToCodeGenerator._get_connected_nodes(nodes, connections, parent_node.id, 'output')
        
        for child in children:
            node_type = child.type
            props = child.properties
            
            if node_type == 'Section':
                html_parts.append(f'{indent_str}<section id="{props.get("id", "")}" class="{props.get("class", "")}">')
                child_html = FlowToCodeGenerator._generate_element_html(nodes, connections, child, indent + 1)
                html_parts.append(child_html)
                html_parts.append(f'{indent_str}</section>')
                
            elif node_type == 'Container':
                html_parts.append(f'{indent_str}<div id="{props.get("id", "")}" class="{props.get("class", "container")}">')
                child_html = FlowToCodeGenerator._generate_element_html(nodes, connections, child, indent + 1)
                html_parts.append(child_html)
                html_parts.append(f'{indent_str}</div>')
                
            elif node_type == 'Header':
                html_parts.append(f'{indent_str}<header>')
                child_html = FlowToCodeGenerator._generate_element_html(nodes, connections, child, indent + 1)
                html_parts.append(child_html)
                html_parts.append(f'{indent_str}</header>')
                
            elif node_type == 'Footer':
                html_parts.append(f'{indent_str}<footer>')
                child_html = FlowToCodeGenerator._generate_element_html(nodes, connections, child, indent + 1)
                html_parts.append(child_html)
                html_parts.append(f'{indent_str}</footer>')
                
            elif node_type == 'Text':
                tag = props.get('tag', 'p')
                text = props.get('text', 'Sample text')
                html_parts.append(f'{indent_str}<{tag}>{text}</{tag}>')
                
            elif node_type == 'Heading':
                level = props.get('level', 'h1')
                text = props.get('text', 'Heading')
                html_parts.append(f'{indent_str}<{level}>{text}</{level}>')
                
            elif node_type == 'Button':
                text = props.get('text', 'Click Me')
                html_parts.append(f'{indent_str}<button id="btn-{child.id}">{text}</button>')
                
            elif node_type == 'Image':
                src = props.get('src', 'image.jpg')
                alt = props.get('alt', 'Image')
                html_parts.append(f'{indent_str}<img src="{src}" alt="{alt}">')
                
            elif node_type == 'Link':
                href = props.get('href', '#')
                text = props.get('text', 'Link')
                html_parts.append(f'{indent_str}<a href="{href}">{text}</a>')
                
            elif node_type == 'Input Field':
                input_type = props.get('type', 'text')
                placeholder = props.get('placeholder', '')
                html_parts.append(f'{indent_str}<input type="{input_type}" placeholder="{placeholder}">')
        
        return '\n'.join(html_parts)
    
    @staticmethod
    def _get_connected_nodes(nodes, connections, node_id, direction='output'):
        """Get nodes connected to this node"""
        connected = []
        for conn in connections:
            if direction == 'output' and conn['from'] == node_id:
                target_node = next((n for n in nodes if n.id == conn['to']), None)
                if target_node:
                    connected.append(target_node)
            elif direction == 'input' and conn['to'] == node_id:
                source_node = next((n for n in nodes if n.id == conn['from']), None)
                if source_node:
                    connected.append(source_node)
        return connected
    
    @staticmethod
    def generate_css(nodes, connections):
        """Generate CSS from styling nodes"""
        css_parts = []
        css_parts.append('* { box-sizing: border-box; margin: 0; padding: 0; }')
        css_parts.append('body { font-family: Arial, sans-serif; }')
        css_parts.append('.container { max-width: 1200px; margin: 0 auto; padding: 20px; }')
        
        # Process styling nodes
        for node in nodes:
            if node.type in ['Background Color', 'Text Color', 'Font Style', 'Spacing', 'Border', 'Shadow', 'Size']:
                # Find what element this styling applies to
                target_nodes = FlowToCodeGenerator._get_connected_nodes(nodes, connections, node.id, 'input')
                for target in target_nodes:
                    selector = f'#{target.id}' if hasattr(target, 'id') else '.element'
                    styles = FlowToCodeGenerator._generate_css_properties(node)
                    if styles:
                        css_parts.append(f'{selector} {{ {styles} }}')
        
        return '\n'.join(css_parts)
    
    @staticmethod
    def _generate_css_properties(node):
        """Generate CSS properties from styling node"""
        props = node.properties
        styles = []
        
        if node.type == 'Background Color':
            styles.append(f'background-color: {props.get("color", "#ffffff")}')
        elif node.type == 'Text Color':
            styles.append(f'color: {props.get("color", "#000000")}')
        elif node.type == 'Font Style':
            styles.append(f'font-size: {props.get("size", "16px")}')
            styles.append(f'font-weight: {props.get("weight", "normal")}')
            styles.append(f'font-family: {props.get("family", "Arial")}')
        elif node.type == 'Spacing':
            styles.append(f'padding: {props.get("padding", "10px")}')
            styles.append(f'margin: {props.get("margin", "10px")}')
        elif node.type == 'Border':
            styles.append(f'border: {props.get("width", "1px")} {props.get("style", "solid")} {props.get("color", "#000")}')
            styles.append(f'border-radius: {props.get("radius", "0px")}')
        elif node.type == 'Shadow':
            x = props.get("x", "0px")
            y = props.get("y", "4px")
            blur = props.get("blur", "10px")
            color = props.get("color", "rgba(0,0,0,0.1)")
            styles.append(f'box-shadow: {x} {y} {blur} {color}')
        elif node.type == 'Size':
            styles.append(f'width: {props.get("width", "auto")}')
            styles.append(f'height: {props.get("height", "auto")}')
        
        return '; '.join(styles)
    
    @staticmethod
    def generate_js(nodes, connections):
        """Generate JavaScript from JS nodes"""
        js_parts = []
        js_parts.append('document.addEventListener("DOMContentLoaded", function() {')
        
        # Process JavaScript nodes
        for node in nodes:
            if node.type == 'Click Event':
                # Find connected button
                targets = FlowToCodeGenerator._get_connected_nodes(nodes, connections, node.id, 'input')
                for target in targets:
                    js_parts.append(f'    document.getElementById("btn-{target.id}").addEventListener("click", function() {{')
                    js_parts.append(f'        console.log("Button clicked");')
                    js_parts.append(f'    }});')
            
            elif node.type == 'Alert':
                message = node.properties.get('message', 'Hello!')
                js_parts.append(f'    alert("{message}");')
        
        js_parts.append('});')
        
        return '\n'.join(js_parts)
