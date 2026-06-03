/* ==========================
   CODE QUEST JS - COMPLETE
========================== */

// ==========================
// ASTRO CAT CURSOR (Single declaration)
// ==========================

// Create custom cursor - ONLY ONCE
const customCursor = document.createElement("div");
customCursor.className = "cursor";
customCursor.innerHTML = "🐱‍🚀";
document.body.appendChild(customCursor);

// Custom cursor movement
document.addEventListener("mousemove", (e) => {
    customCursor.style.left = `${e.clientX}px`;
    customCursor.style.top = `${e.clientY}px`;
});

// Hide cursor when leaving window
document.addEventListener("mouseleave", () => {
    customCursor.style.opacity = "0";
});

document.addEventListener("mouseenter", () => {
    customCursor.style.opacity = "1";
});

// ==========================
// FLOATING ASTRO CAT (Fixed)
// ==========================

const astroCat = document.createElement("div");
astroCat.innerHTML = "🐱‍🚀";
astroCat.style.position = "fixed";
astroCat.style.left = "40px";
astroCat.style.bottom = "100px";
astroCat.style.fontSize = "70px";
astroCat.style.pointerEvents = "none";
astroCat.style.zIndex = "5";
astroCat.style.animation = "floatCat 4s ease-in-out infinite";
document.body.appendChild(astroCat);

// Add floating animation styles
const floatCatStyle = document.createElement("style");
floatCatStyle.innerHTML = `
    @keyframes floatCat {
        0%, 100% {
            transform: translateY(0);
        }
        50% {
            transform: translateY(-20px);
        }
    }
`;
document.head.appendChild(floatCatStyle);

// ==========================
// STAR PARTICLE EFFECT
// ==========================

// Star particle effect on click
document.addEventListener("click", (e) => {
    createStarParticle(e.clientX, e.clientY);
});

function createStarParticle(x, y) {
    const star = document.createElement("div");
    star.innerHTML = "⭐";
    star.style.position = "fixed";
    star.style.left = x + "px";
    star.style.top = y + "px";
    star.style.fontSize = "20px";
    star.style.pointerEvents = "none";
    star.style.zIndex = "99999";
    star.style.animation = "starExplode 0.8s ease-out forwards";
    document.body.appendChild(star);
    
    setTimeout(() => star.remove(), 800);
}

// Add star explosion animation
const starStyle = document.createElement("style");
starStyle.textContent = `
    @keyframes starExplode {
        0% {
            transform: scale(0) rotate(0deg);
            opacity: 1;
        }
        100% {
            transform: scale(1.5) rotate(180deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(starStyle);

// ==========================
// XP POPUP ANIMATION
// ==========================

function showXPPopup(element, xpAmount) {
    const popup = document.createElement("div");
    popup.textContent = `+${xpAmount} XP`;
    popup.style.position = "absolute";
    popup.style.color = "#ffd93d";
    popup.style.fontWeight = "bold";
    popup.style.fontSize = "20px";
    popup.style.fontFamily = "'Orbitron', monospace";
    popup.style.textShadow = "0 0 10px #00e5ff";
    popup.style.pointerEvents = "none";
    popup.style.zIndex = "10000";
    popup.style.animation = "floatUp 1s ease-out forwards";
    
    const rect = element.getBoundingClientRect();
    popup.style.left = rect.left + rect.width / 2 + "px";
    popup.style.top = rect.top + "px";
    
    document.body.appendChild(popup);
    setTimeout(() => popup.remove(), 1000);
}

// Add float animation
const floatStyle = document.createElement("style");
floatStyle.textContent = `
    @keyframes floatUp {
        0% {
            transform: translateY(0) scale(0.5);
            opacity: 1;
        }
        100% {
            transform: translateY(-50px) scale(1.5);
            opacity: 0;
        }
    }
`;
document.head.appendChild(floatStyle);

// ==========================
// CONFETTI EFFECT
// ==========================

function showConfetti() {
    const colors = ["#00e5ff", "#b026ff", "#ffd93d", "#4ade80", "#ff6b6b"];
    
    for (let i = 0; i < 100; i++) {
        const confetti = document.createElement("div");
        confetti.style.position = "fixed";
        confetti.style.width = Math.random() * 10 + 5 + "px";
        confetti.style.height = Math.random() * 10 + 5 + "px";
        confetti.style.backgroundColor = colors[Math.floor(Math.random() * colors.length)];
        confetti.style.left = Math.random() * 100 + "%";
        confetti.style.top = "-10px";
        confetti.style.borderRadius = "2px";
        confetti.style.pointerEvents = "none";
        confetti.style.zIndex = "99999";
        confetti.style.animation = `confettiFall ${Math.random() * 2 + 2}s linear forwards`;
        document.body.appendChild(confetti);
        
        setTimeout(() => confetti.remove(), 3000);
    }
}

// Confetti animation
const confettiStyle = document.createElement("style");
confettiStyle.textContent = `
    @keyframes confettiFall {
        to {
            transform: translateY(100vh) rotate(360deg);
            opacity: 0;
        }
    }
`;
document.head.appendChild(confettiStyle);

// ==========================
// LEVEL UP ANIMATION
// ==========================

function showLevelUp(level) {
    const levelUpDiv = document.createElement("div");
    levelUpDiv.innerHTML = `
        <div style="position: fixed; top: 50%; left: 50%; transform: translate(-50%, -50%);
                    background: linear-gradient(135deg, #b026ff, #00e5ff);
                    padding: 30px 50px;
                    border-radius: 30px;
                    text-align: center;
                    z-index: 100000;
                    animation: levelUpPop 0.5s ease-out forwards;
                    box-shadow: 0 0 50px rgba(0,229,255,0.8);">
            <div style="font-size: 60px;">🎉</div>
            <h2 style="color: white; margin: 10px 0; font-family: 'Orbitron', sans-serif;">LEVEL UP!</h2>
            <p style="color: white; margin: 0;">You reached Level ${level}!</p>
        </div>
    `;
    document.body.appendChild(levelUpDiv);
    
    showConfetti();
    
    setTimeout(() => levelUpDiv.remove(), 3000);
}

// Add level up animation
const levelUpStyle = document.createElement("style");
levelUpStyle.textContent = `
    @keyframes levelUpPop {
        0% {
            transform: translate(-50%, -50%) scale(0);
            opacity: 0;
        }
        50% {
            transform: translate(-50%, -50%) scale(1.1);
        }
        100% {
            transform: translate(-50%, -50%) scale(1);
            opacity: 1;
        }
    }
`;
document.head.appendChild(levelUpStyle);

// ==========================
// ACHIEVEMENT UNLOCK TOAST
// ==========================

function showAchievement(badgeName) {
    const toast = document.createElement("div");
    toast.innerHTML = `
        <div style="background: linear-gradient(135deg, #b026ff, #00e5ff);
                    padding: 15px 25px;
                    border-radius: 15px;
                    margin-bottom: 10px;
                    animation: slideIn 0.3s ease;
                    box-shadow: 0 0 20px rgba(0,229,255,0.5);">
            🏆 <strong style="font-family: 'Orbitron', sans-serif;">${badgeName}</strong> Unlocked!
        </div>
    `;
    toast.style.position = "fixed";
    toast.style.bottom = "20px";
    toast.style.right = "20px";
    toast.style.zIndex = "10000";
    document.body.appendChild(toast);
    
    setTimeout(() => toast.remove(), 4000);
}

// ==========================
// FORM SUBMISSION LOADING STATE
// ==========================

document.querySelectorAll("form").forEach(form => {
    form.addEventListener("submit", function(e) {
        const submitBtn = this.querySelector('button[type="submit"], input[type="submit"]');
        if (submitBtn && !submitBtn.disabled) {
            const originalText = submitBtn.innerHTML;
            submitBtn.innerHTML = '<span class="loading-spinner"></span> Loading...';
            submitBtn.disabled = true;
            
            // Reset after form submission (fallback)
            setTimeout(() => {
                if (submitBtn.disabled) {
                    submitBtn.innerHTML = originalText;
                    submitBtn.disabled = false;
                }
            }, 10000);
        }
    });
});

// ==========================
// TOOLTIP SYSTEM
// ==========================

document.querySelectorAll("[data-tooltip]").forEach(el => {
    let tooltip;
    
    el.addEventListener("mouseenter", () => {
        tooltip = document.createElement("div");
        tooltip.textContent = el.dataset.tooltip;
        tooltip.style.position = "fixed";
        tooltip.style.background = "#1f2937";
        tooltip.style.color = "white";
        tooltip.style.padding = "8px 12px";
        tooltip.style.borderRadius = "8px";
        tooltip.style.fontSize = "12px";
        tooltip.style.fontFamily = "'Poppins', sans-serif";
        tooltip.style.zIndex = "10000";
        tooltip.style.whiteSpace = "nowrap";
        tooltip.style.boxShadow = "0 0 10px rgba(0,229,255,0.5)";
        tooltip.style.border = "1px solid #00e5ff";
        
        const rect = el.getBoundingClientRect();
        tooltip.style.left = rect.left + rect.width / 2 - 20 + "px";
        tooltip.style.top = rect.top - 35 + "px";
        
        document.body.appendChild(tooltip);
    });
    
    el.addEventListener("mouseleave", () => {
        if (tooltip) tooltip.remove();
    });
});

// ==========================
// KEYBOARD SHORTCUTS
// ==========================

document.addEventListener("keydown", (e) => {
    // Ctrl + K for search focus
    if (e.ctrlKey && e.key === "k") {
        e.preventDefault();
        const searchInput = document.querySelector('input[type="search"], .search-input');
        if (searchInput) {
            searchInput.focus();
            searchInput.style.boxShadow = "0 0 15px #00e5ff";
            setTimeout(() => {
                searchInput.style.boxShadow = "";
            }, 1000);
        }
    }
    
    // Ctrl + H for home
    if (e.ctrlKey && e.key === "h") {
        e.preventDefault();
        window.location.href = "/";
    }
    
    // Ctrl + L for leaderboard
    if (e.ctrlKey && e.key === "l") {
        e.preventDefault();
        window.location.href = "/leaderboard/";
    }
    
    // Escape key to blur focused elements
    if (e.key === "Escape") {
        document.activeElement.blur();
    }
});

// ==========================
// GALAXY BACKGROUND EFFECT
// ==========================

const galaxyDiv = document.createElement("div");
galaxyDiv.className = "galaxy";
document.body.insertBefore(galaxyDiv, document.body.firstChild);

// Parallax effect on mouse move
document.addEventListener("mousemove", (e) => {
    const x = e.clientX / window.innerWidth;
    const y = e.clientY / window.innerHeight;
    
    const galaxy = document.querySelector(".galaxy");
    if (galaxy) {
        galaxy.style.transform = `translate(${x * 20}px, ${y * 20}px)`;
    }
});

// ==========================
// SMOOTH SCROLL FOR ANCHOR LINKS
// ==========================

document.querySelectorAll('a[href^="#"]').forEach(anchor => {
    anchor.addEventListener("click", function(e) {
        const href = this.getAttribute("href");
        if (href && href !== "#") {
            e.preventDefault();
            const target = document.querySelector(href);
            if (target) {
                target.scrollIntoView({ behavior: "smooth" });
            }
        }
    });
});

// ==========================
// LOADING SCREEN HIDE
// ==========================

window.addEventListener("load", () => {
    const loadingScreen = document.querySelector(".loading-screen");
    if (loadingScreen) {
        setTimeout(() => {
            loadingScreen.style.opacity = "0";
            setTimeout(() => {
                loadingScreen.style.display = "none";
            }, 500);
        }, 500);
    }
});

// ==========================
// ADD LOADING SPINNER STYLES
// ==========================

const spinnerStyle = document.createElement("style");
spinnerStyle.textContent = `
    .loading-spinner {
        display: inline-block;
        width: 16px;
        height: 16px;
        border: 2px solid rgba(255, 255, 255, 0.3);
        border-top-color: #00e5ff;
        border-radius: 50%;
        animation: spin 0.8s linear infinite;
        margin-right: 8px;
        vertical-align: middle;
    }
    
    @keyframes spin {
        to {
            transform: rotate(360deg);
        }
    }
`;
document.head.appendChild(spinnerStyle);

// ==========================
// PAGE TRANSITION EFFECT
// ==========================

document.querySelectorAll("a").forEach(link => {
    // Only apply to internal links
    if (link.href && link.hostname === window.location.hostname && !link.target) {
        link.addEventListener("click", (e) => {
            // Don't add transition for anchor links
            if (link.getAttribute("href").startsWith("#")) return;
            
            e.preventDefault();
            const destination = link.href;
            
            // Add fade out effect
            document.body.style.transition = "opacity 0.3s";
            document.body.style.opacity = "0";
            
            setTimeout(() => {
                window.location.href = destination;
            }, 300);
        });
    }
});

// ==========================
// EXPORT FUNCTIONS FOR GLOBAL USE
// ==========================

window.showXPPopup = showXPPopup;
window.showConfetti = showConfetti;
window.showLevelUp = showLevelUp;
window.showAchievement = showAchievement;
window.createStarParticle = createStarParticle;

// ==========================
// CONSOLE WELCOME MESSAGE
// ==========================

console.log("%c🚀 Welcome to CodeQuest Space Academy! 🚀", "color: #00e5ff; font-size: 16px; font-weight: bold; font-family: 'Orbitron', monospace;");
console.log("%c🌌 Your coding journey through the galaxy begins here! 🌌", "color: #b026ff; font-size: 14px; font-family: 'Orbitron', monospace;");
console.log("%c✨ Use Ctrl+K to search | Ctrl+H for home | Esc to blur ✨", "color: #ffd93d; font-size: 12px;");

// ==========================
// INITIALIZE ON DOM READY
// ==========================

document.addEventListener("DOMContentLoaded", () => {
    console.log("✅ CodeQuest Space Theme Fully Loaded! 🚀✨");
    
    // Add floating animation to cards on scroll
    const cards = document.querySelectorAll(".card, .learning-path-card");
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.style.opacity = "1";
                entry.target.style.transform = "translateY(0)";
            }
        });
    }, { threshold: 0.1 });
    
    cards.forEach(card => {
        card.style.opacity = "0";
        card.style.transform = "translateY(20px)";
        card.style.transition = "opacity 0.5s ease, transform 0.5s ease";
        observer.observe(card);
    });
});