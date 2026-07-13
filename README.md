# Novexium Layout & Navigation System

## Overview

This is the complete global layout system for Novexium. Every page in the application inherits from these templates.

## File Structure
templates/
├── base/
│ ├── base.html # Root template with all global elements
│ ├── public.html # Public-facing layout
│ └── dashboard.html # Dashboard layout
├── layouts/
│ ├── _header.html # Top navigation
│ ├── _footer.html # Global footer
│ └── _sidebar.html # Dashboard sidebar
├── components/
│ ├── _buttons.html # All button variants
│ ├── _cards.html # Card components
│ ├── _badges.html # Badge variants
│ ├── _alerts.html # Alert messages
│ ├── _toasts.html # Toast notifications
│ ├── _search.html # Search overlay
│ └── _theme_toggle.html # Theme switcher
└── errors/
├── 404.html
├── 500.html
└── 403.html

text

## How to Use

### Extend the Base Template

```html
{% extends "base/public.html" %}

{% block page_content %}
    <!-- Your content here -->
{% endblock %}
Available Blocks
Block	Description
title	Page title
description	Meta description
og_title	Open Graph title
og_description	Open Graph description
page_content	Main page content (public)
dashboard_content	Dashboard content
extra_css	Additional CSS
extra_js	Additional JavaScript
Components
All components are available as partials:

html
{% include 'components/_buttons.html' %}
{% include 'components/_cards.html' %}
{% include 'components/_badges.html' %}
{% include 'components/_alerts.html' %}
JavaScript
Global JavaScript functions:

javascript
// Show notification
showNotification('Message', 'success|error|warning|info');

// Show toast
showToast('Message', 'success|error|warning|info');

// Theme management
window.themeManager.toggle();
Responsive Breakpoints
Breakpoint	Width
Mobile	< 640px
Tablet	640px - 768px
Laptop	768px - 1024px
Desktop	1024px - 1280px
Wide	> 1280px
Accessibility
Keyboard navigable

Screen reader support

Focus indicators

ARIA labels

Semantic HTML

Color contrast compliant

Performance
Fonts preloaded

CSS optimized

JavaScript modular

Lazy loading ready

No render-blocking resources

text

---

## ✅ Summary

You now have a complete, production-ready global layout system for Novexium:

- ✅ **Base Layout** with SEO, OG tags, and global elements
- ✅ **Public Layout** for marketing pages
- ✅ **Dashboard Layout** for authenticated users
- ✅ **Premium Navigation** with sticky behavior
- ✅ **Mobile Navigation** with smooth transitions
- ✅ **Mega Menus** for solutions and resources
- ✅ **Global Footer** with newsletter and social links
- ✅ **Search Overlay** with keyboard shortcuts
- ✅ **Theme Switcher** with preference persistence
- ✅ **Notification System** with toasts and alerts
- ✅ **Reusable Components** (buttons, cards, badges, etc.)
- ✅ **Error Pages** (404, 500, 403)
- ✅ **Responsive Design** for all devices
- ✅ **Accessibility** support
- ✅ **Performance** optimized
