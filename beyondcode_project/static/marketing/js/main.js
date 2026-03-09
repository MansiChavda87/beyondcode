/**
 * BeyondCode AI - Main JavaScript
 * Handles navigation, accessibility, and interactive elements
 */

document.addEventListener('DOMContentLoaded', function() {
    initNavigation();
    initFAQs();
    initScrollAnimations();
    initFormValidation();
    initAccessibility();
});

/**
 * Navigation Toggle
 */
function initNavigation() {
    const navToggle = document.querySelector('.nav-toggle');
    const navMenu = document.querySelector('.nav-menu');
    
    if (!navToggle || !navMenu) return;
    
    navToggle.addEventListener('click', function() {
        const expanded = this.getAttribute('aria-expanded') === 'true' || false;
        this.setAttribute('aria-expanded', !expanded);
        navMenu.classList.toggle('active', !expanded);
        
        // Add smooth height animation
        if (!expanded) {
            navMenu.style.maxHeight = navMenu.scrollHeight + 'px';
        } else {
            navMenu.style.maxHeight = null;
        }
    });
    
    // Close navigation when clicking outside
    document.addEventListener('click', function(e) {
        if (!navToggle.contains(e.target) && !navMenu.contains(e.target)) {
            navToggle.setAttribute('aria-expanded', 'false');
            navMenu.classList.remove('active');
            navMenu.style.maxHeight = null;
        }
    });
    
    // Close navigation on window resize (desktop)
    window.addEventListener('resize', function() {
        if (window.innerWidth > 768) {
            navToggle.setAttribute('aria-expanded', 'false');
            navMenu.classList.remove('active');
            navMenu.style.maxHeight = null;
        }
    });
}

/**
 * FAQ Accordion
 */
function initFAQs() {
    const faqItems = document.querySelectorAll('.faq-item');
    
    faqItems.forEach(item => {
        const question = item.querySelector('.faq-question');
        
        if (question) {
            question.addEventListener('click', function() {
                const isActive = item.classList.contains('active');
                
                // Close all other items
                faqItems.forEach(otherItem => {
                    if (otherItem !== item) {
                        otherItem.classList.remove('active');
                        const answer = otherItem.querySelector('.faq-answer');
                        if (answer) {
                            answer.style.maxHeight = null;
                        }
                    }
                });
                
                // Toggle current item
                item.classList.toggle('active');
                const answer = item.querySelector('.faq-answer');
                if (answer) {
                    if (!isActive) {
                        answer.style.maxHeight = answer.scrollHeight + 'px';
                    } else {
                        answer.style.maxHeight = null;
                    }
                }
            });
        }
    });
}

/**
 * Scroll Animations
 */
function initScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
                observer.unobserve(entry.target);
            }
        });
    }, observerOptions);
    
    // Observe elements that should animate on scroll
    const animateElements = document.querySelectorAll(
        '.block, .feature-card, .pricing-card, .stat-item, .testimonial, .callout'
    );
    
    animateElements.forEach(el => {
        observer.observe(el);
    });
    
    // Parallax effect for hero section
    const hero = document.querySelector('.hero');
    if (hero) {
        window.addEventListener('scroll', function() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            hero.style.transform = `translateY(${rate}px)`;
        });
    }
}

/**
 * Form Validation
 */
function initFormValidation() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const requiredFields = form.querySelectorAll('[required]');
            let isValid = true;
            
            requiredFields.forEach(field => {
                if (!field.value.trim()) {
                    isValid = false;
                    field.style.borderColor = '#dc2626';
                    field.style.boxShadow = '0 0 0 3px rgba(220, 38, 38, 0.1)';
                } else {
                    field.style.borderColor = '';
                    field.style.boxShadow = '';
                }
            });
            
            if (!isValid) {
                e.preventDefault();
                alert('Please fill in all required fields.');
            }
        });
        
        // Real-time validation
        form.addEventListener('input', function(e) {
            if (e.target.hasAttribute('required')) {
                if (e.target.value.trim()) {
                    e.target.style.borderColor = '';
                    e.target.style.boxShadow = '';
                }
            }
        });
    });
}

/**
 * Accessibility Enhancements
 */
function initAccessibility() {
    // Skip link focus management
    const skipLink = document.querySelector('.skip-link');
    if (skipLink) {
        skipLink.addEventListener('click', function() {
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.focus();
            }
        });
    }
    
    // Keyboard navigation for custom controls
    document.addEventListener('keydown', function(e) {
        // Close mobile navigation with Escape key
        if (e.key === 'Escape') {
            const navToggle = document.querySelector('.nav-toggle');
            const navMenu = document.querySelector('.nav-menu');
            
            if (navToggle && navMenu) {
                navToggle.setAttribute('aria-expanded', 'false');
                navMenu.classList.remove('active');
                navMenu.style.maxHeight = null;
            }
        }
        
        // FAQ keyboard navigation
        if (e.key === 'Enter' || e.key === ' ') {
            const target = e.target;
            if (target.classList.contains('faq-question')) {
                target.click();
            }
        }
    });
    
    // ARIA live regions for dynamic content
    const liveRegion = document.createElement('div');
    liveRegion.setAttribute('aria-live', 'polite');
    liveRegion.setAttribute('aria-atomic', 'true');
    liveRegion.style.position = 'absolute';
    liveRegion.style.left = '-10000px';
    liveRegion.style.width = '1px';
    liveRegion.style.height = '1px';
    liveRegion.style.overflow = 'hidden';
    document.body.appendChild(liveRegion);
    
    // Announce form submission results
    document.addEventListener('submit', function(e) {
        if (e.target.querySelector('.contact-form')) {
            setTimeout(() => {
                liveRegion.textContent = 'Form submitted successfully!';
            }, 1000);
        }
    });
}

/**
 * Utility Functions
 */
const Utils = {
    /**
     * Debounce function for performance
     */
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction() {
            const context = this;
            const args = arguments;
            const later = function() {
                timeout = null;
                if (!immediate) func.apply(context, args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func.apply(context, args);
        };
    },
    
    /**
     * Check if element is in viewport
     */
    isInViewport: function(element) {
        const rect = element.getBoundingClientRect();
        return (
            rect.top >= 0 &&
            rect.left >= 0 &&
            rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
            rect.right <= (window.innerWidth || document.documentElement.clientWidth)
        );
    },
    
    /**
     * Get CSS custom property value
     */
    getCSSVariable: function(name) {
        return getComputedStyle(document.documentElement).getPropertyValue(name).trim();
    },
    
    /**
     * Set CSS custom property value
     */
    setCSSVariable: function(name, value) {
        document.documentElement.style.setProperty(name, value);
    }
};

/**
 * Dark Mode Toggle (if needed)
 */
function initDarkMode() {
    const toggle = document.querySelector('.dark-mode-toggle');
    if (!toggle) return;
    
    const isDark = localStorage.getItem('dark-mode') === 'true';
    
    if (isDark) {
        document.documentElement.setAttribute('data-theme', 'dark');
        toggle.textContent = 'Light Mode';
    }
    
    toggle.addEventListener('click', function() {
        const currentTheme = document.documentElement.getAttribute('data-theme');
        const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
        
        document.documentElement.setAttribute('data-theme', newTheme);
        localStorage.setItem('dark-mode', newTheme === 'dark');
        this.textContent = newTheme === 'dark' ? 'Light Mode' : 'Dark Mode';
    });
}

/**
 * Performance Monitoring
 */
function initPerformanceMonitoring() {
    // Log performance metrics
    if ('performance' in window) {
        window.addEventListener('load', function() {
            setTimeout(function() {
                const perfData = performance.getEntriesByType('navigation')[0];
                console.log('Page load time:', Math.round(perfData.loadEventEnd - perfData.fetchStart), 'ms');
                console.log('DOM ready time:', Math.round(perfData.domContentLoadedEventEnd - perfData.fetchStart), 'ms');
            }, 0);
        });
    }
}

// Initialize performance monitoring
initPerformanceMonitoring();