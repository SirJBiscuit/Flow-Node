"""
Component Library - Pre-designed beautiful UI components
"""

class ComponentLibrary:
    """Library of pre-designed, beautiful UI components"""
    
    @staticmethod
    def get_all_components():
        """Returns all available components organized by category"""
        return {
            'Buttons': ComponentLibrary.get_buttons(),
            'Cards': ComponentLibrary.get_cards(),
            'Forms': ComponentLibrary.get_forms(),
            'Navigation': ComponentLibrary.get_navigation(),
            'Headers': ComponentLibrary.get_headers(),
            'Footers': ComponentLibrary.get_footers(),
            'Widgets': ComponentLibrary.get_widgets(),
            'Sliders': ComponentLibrary.get_sliders(),
        }
    
    @staticmethod
    def get_buttons():
        """Pre-designed button components"""
        return {
            'Primary Button': {
                'html': '<button class="btn-primary">{text}</button>',
                'css': '''.btn-primary {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    padding: 12px 32px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
}
.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: 0 6px 20px rgba(102, 126, 234, 0.6);
}''',
                'preview': 'Gradient purple button with shadow',
                'customizable': ['text', 'size', 'color', 'shadow', 'rounded']
            },
            'Outline Button': {
                'html': '<button class="btn-outline">{text}</button>',
                'css': '''.btn-outline {
    background: transparent;
    color: #667eea;
    border: 2px solid #667eea;
    padding: 12px 32px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 8px;
    cursor: pointer;
    transition: all 0.3s ease;
}
.btn-outline:hover {
    background: #667eea;
    color: white;
    transform: scale(1.05);
}''',
                'preview': 'Outlined button with hover fill',
                'customizable': ['text', 'size', 'color', 'rounded']
            },
            'Neon Button': {
                'html': '<button class="btn-neon">{text}</button>',
                'css': '''.btn-neon {
    background: #000;
    color: #00ff88;
    border: 2px solid #00ff88;
    padding: 14px 36px;
    font-size: 16px;
    font-weight: 700;
    border-radius: 4px;
    cursor: pointer;
    text-transform: uppercase;
    letter-spacing: 2px;
    box-shadow: 0 0 20px rgba(0, 255, 136, 0.5);
    transition: all 0.3s ease;
}
.btn-neon:hover {
    box-shadow: 0 0 30px rgba(0, 255, 136, 0.8), 0 0 60px rgba(0, 255, 136, 0.4);
    transform: scale(1.05);
}''',
                'preview': 'Cyberpunk neon glow button',
                'customizable': ['text', 'size', 'color', 'shadow']
            },
            'Glassmorphism Button': {
                'html': '<button class="btn-glass">{text}</button>',
                'css': '''.btn-glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    color: white;
    padding: 14px 32px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 12px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
}
.btn-glass:hover {
    background: rgba(255, 255, 255, 0.2);
    transform: translateY(-2px);
}''',
                'preview': 'Frosted glass effect button',
                'customizable': ['text', 'size', 'rounded', 'shadow']
            },
            'Animated Button': {
                'html': '<button class="btn-animated">{text}</button>',
                'css': '''.btn-animated {
    background: #ff6b6b;
    color: white;
    border: none;
    padding: 14px 36px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
}
.btn-animated::before {
    content: '';
    position: absolute;
    top: 0;
    left: -100%;
    width: 100%;
    height: 100%;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.3), transparent);
    transition: left 0.5s;
}
.btn-animated:hover::before {
    left: 100%;
}
.btn-animated:hover {
    transform: scale(1.05);
    box-shadow: 0 5px 20px rgba(255, 107, 107, 0.4);
}''',
                'preview': 'Button with shine animation',
                'customizable': ['text', 'size', 'color', 'shadow', 'rounded']
            },
            'Icon Button': {
                'html': '<button class="btn-icon">⭐ {text}</button>',
                'css': '''.btn-icon {
    background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    color: white;
    border: none;
    padding: 12px 28px;
    font-size: 16px;
    font-weight: 600;
    border-radius: 10px;
    cursor: pointer;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.3s ease;
    box-shadow: 0 4px 15px rgba(245, 87, 108, 0.3);
}
.btn-icon:hover {
    transform: translateY(-3px);
    box-shadow: 0 6px 25px rgba(245, 87, 108, 0.5);
}''',
                'preview': 'Button with icon and gradient',
                'customizable': ['text', 'size', 'color', 'shadow', 'rounded']
            }
        }
    
    @staticmethod
    def get_cards():
        """Pre-designed card components"""
        return {
            'Modern Card': {
                'html': '''<div class="card-modern">
    <h3>{title}</h3>
    <p>{description}</p>
</div>''',
                'css': '''.card-modern {
    background: white;
    padding: 30px;
    border-radius: 16px;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.card-modern:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(0, 0, 0, 0.15);
}
.card-modern h3 {
    margin: 0 0 15px 0;
    color: #2c3e50;
    font-size: 24px;
}
.card-modern p {
    margin: 0;
    color: #7f8c8d;
    line-height: 1.6;
}''',
                'preview': 'Clean white card with hover lift',
                'customizable': ['size', 'color', 'shadow', 'rounded']
            },
            'Gradient Card': {
                'html': '''<div class="card-gradient">
    <h3>{title}</h3>
    <p>{description}</p>
</div>''',
                'css': '''.card-gradient {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    padding: 35px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 15px 35px rgba(102, 126, 234, 0.3);
    transition: all 0.3s ease;
}
.card-gradient:hover {
    transform: scale(1.02);
    box-shadow: 0 20px 45px rgba(102, 126, 234, 0.4);
}
.card-gradient h3 {
    margin: 0 0 15px 0;
    font-size: 26px;
}
.card-gradient p {
    margin: 0;
    opacity: 0.9;
    line-height: 1.6;
}''',
                'preview': 'Purple gradient card',
                'customizable': ['size', 'color', 'shadow', 'rounded']
            },
            'Glass Card': {
                'html': '''<div class="card-glass">
    <h3>{title}</h3>
    <p>{description}</p>
</div>''',
                'css': '''.card-glass {
    background: rgba(255, 255, 255, 0.1);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 30px;
    border-radius: 20px;
    color: white;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.card-glass:hover {
    background: rgba(255, 255, 255, 0.15);
    transform: translateY(-3px);
}
.card-glass h3 {
    margin: 0 0 15px 0;
    font-size: 24px;
}
.card-glass p {
    margin: 0;
    opacity: 0.9;
    line-height: 1.6;
}''',
                'preview': 'Glassmorphism card effect',
                'customizable': ['size', 'rounded', 'shadow']
            },
            'Pricing Card': {
                'html': '''<div class="card-pricing">
    <div class="price-tag">{price}</div>
    <h3>{title}</h3>
    <p>{description}</p>
    <button class="card-btn">Choose Plan</button>
</div>''',
                'css': '''.card-pricing {
    background: white;
    padding: 40px 30px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 40px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
    border: 2px solid transparent;
}
.card-pricing:hover {
    border-color: #667eea;
    transform: translateY(-5px);
    box-shadow: 0 15px 50px rgba(102, 126, 234, 0.2);
}
.price-tag {
    font-size: 48px;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 20px;
}
.card-pricing h3 {
    margin: 0 0 15px 0;
    color: #2c3e50;
    font-size: 24px;
}
.card-pricing p {
    margin: 0 0 25px 0;
    color: #7f8c8d;
    line-height: 1.6;
}
.card-btn {
    background: #667eea;
    color: white;
    border: none;
    padding: 12px 32px;
    border-radius: 8px;
    font-weight: 600;
    cursor: pointer;
    transition: all 0.3s ease;
}
.card-btn:hover {
    background: #5568d3;
    transform: scale(1.05);
}''',
                'preview': 'Pricing plan card with button',
                'customizable': ['size', 'color', 'shadow', 'rounded']
            }
        }
    
    @staticmethod
    def get_forms():
        """Pre-designed form components"""
        return {
            'Modern Input': {
                'html': '<input type="text" class="input-modern" placeholder="{placeholder}">',
                'css': '''.input-modern {
    width: 100%;
    padding: 14px 20px;
    font-size: 16px;
    border: 2px solid #e0e0e0;
    border-radius: 10px;
    transition: all 0.3s ease;
    outline: none;
}
.input-modern:focus {
    border-color: #667eea;
    box-shadow: 0 0 0 4px rgba(102, 126, 234, 0.1);
}''',
                'preview': 'Clean input with focus effect',
                'customizable': ['size', 'color', 'rounded']
            },
            'Floating Label Input': {
                'html': '''<div class="input-floating">
    <input type="text" placeholder=" " required>
    <label>{label}</label>
</div>''',
                'css': '''.input-floating {
    position: relative;
    margin: 20px 0;
}
.input-floating input {
    width: 100%;
    padding: 14px 12px;
    font-size: 16px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    outline: none;
    transition: all 0.3s ease;
}
.input-floating label {
    position: absolute;
    left: 12px;
    top: 14px;
    color: #999;
    transition: all 0.3s ease;
    pointer-events: none;
    background: white;
    padding: 0 5px;
}
.input-floating input:focus,
.input-floating input:not(:placeholder-shown) {
    border-color: #667eea;
}
.input-floating input:focus ~ label,
.input-floating input:not(:placeholder-shown) ~ label {
    top: -10px;
    font-size: 12px;
    color: #667eea;
}''',
                'preview': 'Animated floating label input',
                'customizable': ['size', 'color', 'rounded']
            },
            'Search Bar': {
                'html': '<div class="search-bar"><input type="text" placeholder="{placeholder}"><button>🔍</button></div>',
                'css': '''.search-bar {
    display: flex;
    background: white;
    border-radius: 50px;
    overflow: hidden;
    box-shadow: 0 4px 20px rgba(0, 0, 0, 0.1);
}
.search-bar input {
    flex: 1;
    padding: 14px 24px;
    border: none;
    outline: none;
    font-size: 16px;
}
.search-bar button {
    background: #667eea;
    color: white;
    border: none;
    padding: 14px 28px;
    cursor: pointer;
    font-size: 18px;
    transition: all 0.3s ease;
}
.search-bar button:hover {
    background: #5568d3;
}''',
                'preview': 'Modern search bar with icon',
                'customizable': ['size', 'color', 'rounded']
            }
        }
    
    @staticmethod
    def get_navigation():
        """Pre-designed navigation components"""
        return {
            'Modern Navbar': {
                'html': '''<nav class="navbar-modern">
    <div class="nav-brand">{brand}</div>
    <div class="nav-links">
        <a href="#">Home</a>
        <a href="#">About</a>
        <a href="#">Services</a>
        <a href="#">Contact</a>
    </div>
</nav>''',
                'css': '''.navbar-modern {
    display: flex;
    justify-content: space-between;
    align-items: center;
    padding: 20px 50px;
    background: white;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}
.nav-brand {
    font-size: 24px;
    font-weight: 700;
    color: #667eea;
}
.nav-links {
    display: flex;
    gap: 30px;
}
.nav-links a {
    color: #2c3e50;
    text-decoration: none;
    font-weight: 500;
    transition: all 0.3s ease;
}
.nav-links a:hover {
    color: #667eea;
}''',
                'preview': 'Clean horizontal navbar',
                'customizable': ['size', 'color', 'shadow']
            }
        }
    
    @staticmethod
    def get_headers():
        """Pre-designed header components"""
        return {
            'Hero Section': {
                'html': '''<header class="hero-section">
    <h1>{title}</h1>
    <p>{subtitle}</p>
    <button class="hero-btn">Get Started</button>
</header>''',
                'css': '''.hero-section {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    text-align: center;
    padding: 100px 20px;
}
.hero-section h1 {
    font-size: 56px;
    margin: 0 0 20px 0;
    font-weight: 700;
}
.hero-section p {
    font-size: 22px;
    margin: 0 0 40px 0;
    opacity: 0.9;
}
.hero-btn {
    background: white;
    color: #667eea;
    border: none;
    padding: 16px 40px;
    font-size: 18px;
    font-weight: 600;
    border-radius: 50px;
    cursor: pointer;
    transition: all 0.3s ease;
    box-shadow: 0 5px 20px rgba(0, 0, 0, 0.2);
}
.hero-btn:hover {
    transform: translateY(-3px);
    box-shadow: 0 8px 30px rgba(0, 0, 0, 0.3);
}''',
                'preview': 'Gradient hero with CTA',
                'customizable': ['size', 'color', 'shadow']
            }
        }
    
    @staticmethod
    def get_footers():
        """Pre-designed footer components"""
        return {
            'Simple Footer': {
                'html': '''<footer class="footer-simple">
    <p>{text}</p>
</footer>''',
                'css': '''.footer-simple {
    background: #2c3e50;
    color: white;
    text-align: center;
    padding: 30px 20px;
}
.footer-simple p {
    margin: 0;
    opacity: 0.8;
}''',
                'preview': 'Clean centered footer',
                'customizable': ['size', 'color']
            }
        }
    
    @staticmethod
    def get_widgets():
        """Pre-designed widget components"""
        return {
            'Stat Widget': {
                'html': '''<div class="widget-stat">
    <div class="stat-icon">{icon}</div>
    <div class="stat-number">{number}</div>
    <div class="stat-label">{label}</div>
</div>''',
                'css': '''.widget-stat {
    background: white;
    padding: 30px;
    border-radius: 16px;
    text-align: center;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}
.widget-stat:hover {
    transform: translateY(-5px);
    box-shadow: 0 15px 40px rgba(0, 0, 0, 0.15);
}
.stat-icon {
    font-size: 48px;
    margin-bottom: 15px;
}
.stat-number {
    font-size: 36px;
    font-weight: 700;
    color: #667eea;
    margin-bottom: 10px;
}
.stat-label {
    color: #7f8c8d;
    font-size: 16px;
}''',
                'preview': 'Statistics display widget',
                'customizable': ['size', 'color', 'shadow', 'rounded']
            },
            'Badge': {
                'html': '<span class="badge">{text}</span>',
                'css': '''.badge {
    display: inline-block;
    background: #667eea;
    color: white;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
}''',
                'preview': 'Small badge label',
                'customizable': ['size', 'color', 'rounded']
            }
        }
    
    @staticmethod
    def get_sliders():
        """Pre-designed slider components"""
        return {
            'Modern Range Slider': {
                'html': '<input type="range" class="slider-modern" min="0" max="100" value="50">',
                'css': '''.slider-modern {
    -webkit-appearance: none;
    width: 100%;
    height: 8px;
    border-radius: 5px;
    background: #e0e0e0;
    outline: none;
}
.slider-modern::-webkit-slider-thumb {
    -webkit-appearance: none;
    appearance: none;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #667eea;
    cursor: pointer;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
    transition: all 0.3s ease;
}
.slider-modern::-webkit-slider-thumb:hover {
    transform: scale(1.2);
    box-shadow: 0 4px 15px rgba(102, 126, 234, 0.6);
}
.slider-modern::-moz-range-thumb {
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #667eea;
    cursor: pointer;
    border: none;
    box-shadow: 0 2px 10px rgba(102, 126, 234, 0.4);
}''',
                'preview': 'Styled range slider',
                'customizable': ['size', 'color']
            }
        }
