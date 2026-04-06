/**
 * Cartoonizer Pro - Main JavaScript
 * Handles theme toggle, navigation, animations, and interactions
 */

(function() {
    'use strict';

    // ===== Get Current Page =====
    function getCurrentPage() {
        const path = window.location.pathname;
        if (path.includes('cartoonize')) return 'cartoonize';
        if (path.includes('developer')) return 'developer';
        return 'index';
    }

    // ===== Set Active Nav Link =====
    function setActiveNavLink() {
        const currentPage = getCurrentPage();
        const navLinks = document.querySelectorAll('.navbar-nav .nav-link');
        
        navLinks.forEach(link => {
            link.classList.remove('active');
            
            const href = link.getAttribute('href');
            if (currentPage === 'index' && (href === '/' || href.includes('index'))) {
                link.classList.add('active');
            } else if (currentPage === 'cartoonize' && href.includes('cartoonize')) {
                link.classList.add('active');
            } else if (currentPage === 'developer' && href.includes('developer')) {
                link.classList.add('active');
            }
        });
    }

    // ===== Theme Management =====
    const themeToggle = document.getElementById('themeToggle');
    const html = document.documentElement;
    const themeIcon = themeToggle ? themeToggle.querySelector('i') : null;

    // Check for saved theme preference or default to dark for cyber theme
    const savedTheme = localStorage.getItem('theme') || 'dark';
    html.setAttribute('data-theme', savedTheme);
    updateThemeIcon(savedTheme);

    // Theme toggle handler
    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const currentTheme = html.getAttribute('data-theme');
            const newTheme = currentTheme === 'dark' ? 'light' : 'dark';
            
            html.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
            updateThemeIcon(newTheme);
            
            // Dispatch event for other components
            document.dispatchEvent(new CustomEvent('themechange', { detail: { theme: newTheme } }));
        });
    }

    function updateThemeIcon(theme) {
        if (!themeIcon) return;
        
        if (theme === 'dark') {
            themeIcon.className = 'bi bi-sun';
        } else {
            themeIcon.className = 'bi bi-moon-stars';
        }
    }

    // ===== Back to Top Button =====
    const backToTopBtn = document.getElementById('backToTop');
    
    if (backToTopBtn) {
        // Show/hide button based on scroll position
        window.addEventListener('scroll', () => {
            if (window.scrollY > 300) {
                backToTopBtn.classList.add('visible');
            } else {
                backToTopBtn.classList.remove('visible');
            }
        });

        // Scroll to top on click
        backToTopBtn.addEventListener('click', () => {
            window.scrollTo({
                top: 0,
                behavior: 'smooth'
            });
        });
    }

    // ===== Section Reveal Animation =====
    function initRevealAnimations() {
        const revealElements = document.querySelectorAll('.reveal');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    // Add stagger delay based on index
                    const index = Array.from(revealElements).indexOf(entry.target);
                    entry.target.style.transitionDelay = `${index * 0.1}s`;
                    entry.target.classList.add('active');
                    observer.unobserve(entry.target);
                }
            });
        }, { 
            threshold: 0.1,
            rootMargin: '0px 0px -50px 0px'
        });

        revealElements.forEach(el => observer.observe(el));
    }

    // ===== Counter Animation =====
    function animateCounter(element, target, duration = 2000) {
        let startTimestamp = null;
        
        const step = (timestamp) => {
            if (!startTimestamp) startTimestamp = timestamp;
            const progress = Math.min((timestamp - startTimestamp) / duration, 1);
            const current = Math.floor(progress * target);
            element.textContent = current.toLocaleString();
            
            if (progress < 1) {
                window.requestAnimationFrame(step);
            }
        };
        
        window.requestAnimationFrame(step);
    }

    // ===== Initialize Counter Animations =====
    function initCounters() {
        const counters = document.querySelectorAll('.counter[data-target]');
        
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const target = parseInt(entry.target.getAttribute('data-target'));
                    animateCounter(entry.target, target);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });

        counters.forEach(counter => observer.observe(counter));
    }

    // ===== Smooth Scroll =====
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            if (href !== '#') {
                e.preventDefault();
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({
                        behavior: 'smooth',
                        block: 'start'
                    });
                }
            }
        });
    });

    // ===== Navbar Scroll Effect =====
    const navbar = document.getElementById('mainNav');
    
    if (navbar) {
        window.addEventListener('scroll', () => {
            const currentScroll = window.pageYOffset;
            
            if (currentScroll > 50) {
                navbar.style.padding = '8px 0';
                navbar.style.boxShadow = '0 4px 30px rgba(0, 212, 255, 0.15)';
            } else {
                navbar.style.padding = '12px 0';
                navbar.style.boxShadow = '0 4px 30px rgba(0, 212, 255, 0.1)';
            }
        });
    }

    // ===== Utility Functions =====
    
    // Debounce function
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    // Throttle function
    function throttle(func, limit) {
        let inThrottle;
        return function(...args) {
            if (!inThrottle) {
                func.apply(this, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    }

    // ===== Tooltip Initialization =====
    function initTooltips() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(tooltipTriggerEl => {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }

    // ===== Lazy Loading for Images =====
    function initLazyLoading() {
        const lazyImages = document.querySelectorAll('img[data-src]');
        
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.getAttribute('data-src');
                    img.removeAttribute('data-src');
                    imageObserver.unobserve(img);
                }
            });
        });

        lazyImages.forEach(img => imageObserver.observe(img));
    }

    // ===== Form Validation =====
    function validateEmail(email) {
        const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return re.test(email);
    }

    function showFormError(input, message) {
        const parent = input.parentElement;
        let errorElement = parent.querySelector('.error-message');
        
        if (!errorElement) {
            errorElement = document.createElement('div');
            errorElement.className = 'error-message';
            parent.appendChild(errorElement);
        }
        
        errorElement.textContent = message;
        input.classList.add('is-invalid');
    }

    function clearFormError(input) {
        const parent = input.parentElement;
        const errorElement = parent.querySelector('.error-message');
        
        if (errorElement) {
            errorElement.remove();
        }
        
        input.classList.remove('is-invalid');
    }

    // ===== Copy to Clipboard =====
    async function copyToClipboard(text) {
        try {
            await navigator.clipboard.writeText(text);
            return true;
        } catch (err) {
            console.error('Failed to copy:', err);
            return false;
        }
    }

    // ===== Format File Size =====
    function formatFileSize(bytes) {
        if (bytes === 0) return '0 Bytes';
        
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    }

    // ===== Image Preloader =====
    function preloadImages(urls) {
        urls.forEach(url => {
            const img = new Image();
            img.src = url;
        });
    }

    // ===== Loading Spinner =====
    function showLoading(element) {
        if (!element) return;
        
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        spinner.innerHTML = '<div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div>';
        
        element.style.position = 'relative';
        element.appendChild(spinner);
        
        return spinner;
    }

    function hideLoading(spinner) {
        if (spinner && spinner.parentElement) {
            spinner.parentElement.style.position = '';
            spinner.remove();
        }
    }

    // ===== Page Transition =====
    function initPageTransition() {
        const main = document.querySelector('main');
        if (main) {
            // Add fade-in effect on page load
            main.style.animation = 'none';
            main.offsetHeight; // Trigger reflow
            main.style.animation = 'fadeIn 0.4s ease';
        }
    }

    // ===== Hover Micro-interactions =====
    function initHoverEffects() {
        // Button scale on hover
        document.querySelectorAll('.btn-primary, .hero-cta').forEach(btn => {
            btn.addEventListener('mouseenter', () => {
                btn.style.transform = 'translateY(-3px) scale(1.02)';
            });
            btn.addEventListener('mouseleave', () => {
                btn.style.transform = '';
            });
        });

        // Card float on hover
        document.querySelectorAll('.card').forEach(card => {
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'translateY(-8px)';
            });
            card.addEventListener('mouseleave', () => {
                card.style.transform = '';
            });
        });
    }

    // ===== Keyboard Navigation =====
    document.addEventListener('keydown', (e) => {
        // Escape key to close modals
        if (e.key === 'Escape') {
            const activeModal = document.querySelector('.modal.show');
            if (activeModal) {
                bootstrap.Modal.getInstance(activeModal)?.hide();
            }
        }
    });

    // ===== Save/Load State =====
    const stateStorage = {
        save: function(key, value) {
            try {
                localStorage.setItem(`cartoonizer_${key}`, JSON.stringify(value));
            } catch (e) {
                console.warn('Could not save state:', e);
            }
        },
        
        load: function(key) {
            try {
                const value = localStorage.getItem(`cartoonizer_${key}`);
                return value ? JSON.parse(value) : null;
            } catch (e) {
                console.warn('Could not load state:', e);
                return null;
            }
        },
        
        remove: function(key) {
            try {
                localStorage.removeItem(`cartoonizer_${key}`);
            } catch (e) {
                console.warn('Could not remove state:', e);
            }
        }
    };

    // ===== Export to Global =====
    window.CartoonizerPro = {
        utils: {
            debounce,
            throttle,
            validateEmail,
            copyToClipboard,
            formatFileSize,
            preloadImages,
            showFormError,
            clearFormError,
            showLoading,
            hideLoading
        },
        storage: stateStorage,
        theme: {
            get: () => html.getAttribute('data-theme'),
            set: (theme) => {
                html.setAttribute('data-theme', theme);
                localStorage.setItem('theme', theme);
                updateThemeIcon(theme);
            },
            toggle: () => themeToggle?.click()
        },
        animations: {
            reveal: initRevealAnimations,
            counters: initCounters,
            hover: initHoverEffects
        }
    };

    // ===== Initialize on DOM Ready =====
    document.addEventListener('DOMContentLoaded', () => {
        console.log('Cartoonizer Pro initialized');
        
        // Set active nav link
        setActiveNavLink();
        
        // Initialize animations
        initRevealAnimations();
        initCounters();
        initHoverEffects();
        initPageTransition();
        
        initTooltips();
        initLazyLoading();
        
        // Preload critical images
        preloadImages([
            '/static/uploads/.gitkeep',
            '/static/outputs/.gitkeep'
        ]);
    });

    // ===== Handle Page Visibility =====
    document.addEventListener('visibilitychange', () => {
        if (document.hidden) {
            document.body.style.animationPlayState = 'paused';
        } else {
            document.body.style.animationPlayState = 'running';
        }
    });

})();