// PRIME RADIANT 3D VISUALIZATION
// Inspiré de Foundation (Isaac Asimov)
// Fichier : js/prime-radiant-3d.js
// Version corrigée sans boutons RESET/PAUSE

let scene, camera, renderer, sphere, raycaster, mouse;
let eventPoints = [];
let isRotating = true;
let rotationSpeed = 0.001;

function initPrimeRadiant() {
    const container = document.getElementById('prime-radiant-sphere');
    if (!container) {
        console.error('Container prime-radiant-sphere non trouvé');
        return;
    }
    
    // Scene
    scene = new THREE.Scene();
    scene.fog = new THREE.FogExp2(0x000000, 0.001);
    
    // Camera
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    camera = new THREE.PerspectiveCamera(75, width / height, 0.1, 1000);
    camera.position.z = 15;
    
    // Renderer
    renderer = new THREE.WebGLRenderer({
        canvas: container,
        alpha: true,
        antialias: true
    });
    renderer.setSize(width, height);
    renderer.setPixelRatio(window.devicePixelRatio);
    
    // Sphere wireframe (structure du Prime Radiant)
    const geometry = new THREE.SphereGeometry(5, 32, 32);
    const material = new THREE.MeshBasicMaterial({
        color: 0x00f3ff,
        wireframe: true,
        transparent: true,
        opacity: 0.2
    });
    sphere = new THREE.Mesh(geometry, material);
    scene.add(sphere);
    
    // Cercles orbitaux (effet holographique)
    addOrbitalRings();
    
    // Ambient light
    const ambientLight = new THREE.AmbientLight(0x404040);
    scene.add(ambientLight);
    
    // Raycaster pour hover/click
    raycaster = new THREE.Raycaster();
    mouse = new THREE.Vector2();
    
    // Event listeners
    container.addEventListener('mousemove', onMouseMove, false);
    container.addEventListener('click', onMouseClick, false);
    
    window.addEventListener('resize', onWindowResize, false);
    
    // Load historical events
    loadHistoricalEvents();
    
    // Start animation
    animate();
}

function addOrbitalRings() {
    // Ajouter des cercles orbitaux pour l'effet holographique
    for (let i = 0; i < 3; i++) {
        const radius = 5.5 + i * 0.5;
        const segments = 64;
        const curve = new THREE.EllipseCurve(
            0, 0,
            radius, radius,
            0, 2 * Math.PI,
            false,
            0
        );
        
        const points = curve.getPoints(segments);
        const geometry = new THREE.BufferGeometry().setFromPoints(points);
        const material = new THREE.LineBasicMaterial({
            color: 0x00f3ff,
            transparent: true,
            opacity: 0.1
        });
        
        const ellipse = new THREE.Line(geometry, material);
        ellipse.rotation.x = Math.PI / 2;
        scene.add(ellipse);
    }
}

async function loadHistoricalEvents() {
    try {
        const response = await fetch('data/history_full_v3.json?v=' + new Date().getTime());
        if (!response.ok) throw new Error('Fichier history_full_v3.json non trouvé');
        
        const history = await response.json();
        
        // Filtrer les événements majeurs (avec description)
        const majorEvents = history.filter(e => e.description && e.description.length > 0);
        
        // Créer des points pour chaque événement
        majorEvents.forEach((event, index) => {
            createEventPoint(event, index, majorEvents.length);
        });
        
        const countEl = document.getElementById('event-count');
        if (countEl) countEl.textContent = majorEvents.length;
        
    } catch (error) {
        console.error('Erreur chargement historique:', error);
        const countEl = document.getElementById('event-count');
        if (countEl) countEl.textContent = '0';
    }
}

function createEventPoint(event, index, total) {
    // Distribution uniforme sur la sphère (algorithme de Fibonacci)
    const phi = Math.acos(-1 + (2 * index) / total);
    const theta = Math.sqrt(total * Math.PI) * phi;
    
    const radius = 5;
    const x = radius * Math.cos(theta) * Math.sin(phi);
    const y = radius * Math.sin(theta) * Math.sin(phi);
    const z = radius * Math.cos(phi);
    
    // Couleur selon le score
    let color;
    if (event.stability_index >= 60) color = 0x00ff9d; // Vert
    else if (event.stability_index >= 40) color = 0xffee00; // Jaune
    else color = 0xff0055; // Rouge
    
    // Créer le point
    const pointGeometry = new THREE.SphereGeometry(0.15, 16, 16);
    const pointMaterial = new THREE.MeshBasicMaterial({
        color: color,
        transparent: true,
        opacity: 0.8
    });
    const point = new THREE.Mesh(pointGeometry, pointMaterial);
    point.position.set(x, y, z);
    
    // Ajouter des données pour l'interaction
    point.userData = {
        year: event.year,
        score: event.stability_index,
        description: event.description
    };
    
    // Créer un halo lumineux
    const glowGeometry = new THREE.SphereGeometry(0.25, 16, 16);
    const glowMaterial = new THREE.MeshBasicMaterial({
        color: color,
        transparent: true,
        opacity: 0.3
    });
    const glow = new THREE.Mesh(glowGeometry, glowMaterial);
    glow.position.set(x, y, z);
    
    scene.add(glow);
    scene.add(point);
    
    eventPoints.push(point);
    
    // Animation de pulsation
    animatePointPulse(point, glow);
}

function animatePointPulse(point, glow) {
    const initialScale = point.scale.x;
    let time = Math.random() * Math.PI * 2;
    
    function pulse() {
        time += 0.05;
        const scale = initialScale + Math.sin(time) * 0.2;
        point.scale.set(scale, scale, scale);
        if (glow) glow.scale.set(scale * 1.2, scale * 1.2, scale * 1.2);
        requestAnimationFrame(pulse);
    }
    
    pulse();
}

function animate() {
    requestAnimationFrame(animate);
    
    if (isRotating) {
        sphere.rotation.y += rotationSpeed;
        // Les points tournent avec la sphère
        scene.children.forEach(child => {
            if (child.userData.year) {
                child.rotation.y += rotationSpeed;
            }
        });
    }
    
    renderer.render(scene, camera);
}

function onMouseMove(event) {
    const container = document.getElementById('prime-radiant-sphere');
    if (!container) return;
    
    const rect = container.getBoundingClientRect();
    
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(eventPoints);
    
    const tooltip = document.getElementById('event-tooltip');
    if (!tooltip) return;
    
    if (intersects.length > 0) {
        const point = intersects[0].object;
        const data = point.userData;
        
        const yearEl = tooltip.querySelector('.event-year');
        const scoreEl = tooltip.querySelector('.event-score');
        const descEl = tooltip.querySelector('.event-desc');
        
        if (yearEl) yearEl.textContent = data.year;
        if (scoreEl) scoreEl.textContent = `CES: ${data.score}%`;
        if (descEl) descEl.textContent = data.description;
        
        tooltip.style.display = 'block';
        tooltip.style.left = (event.clientX + 15) + 'px';
        tooltip.style.top = (event.clientY + 15) + 'px';
        
        // Highlight
        point.material.opacity = 1;
        point.scale.set(1.5, 1.5, 1.5);
    } else {
        tooltip.style.display = 'none';
        eventPoints.forEach(p => {
            p.material.opacity = 0.8;
            p.scale.set(1, 1, 1);
        });
    }
}

function onMouseClick(event) {
    const container = document.getElementById('prime-radiant-sphere');
    if (!container) return;
    
    const rect = container.getBoundingClientRect();
    
    mouse.x = ((event.clientX - rect.left) / rect.width) * 2 - 1;
    mouse.y = -((event.clientY - rect.top) / rect.height) * 2 + 1;
    
    raycaster.setFromCamera(mouse, camera);
    const intersects = raycaster.intersectObjects(eventPoints);
    
    if (intersects.length > 0) {
        const point = intersects[0].object;
        const data = point.userData;
        
        // Animation de "sélection" (flash)
        const originalColor = point.material.color.clone();
        point.material.color.setHex(0xffffff);
        
        setTimeout(() => {
            point.material.color.copy(originalColor);
        }, 200);
        
        console.log(`Événement sélectionné : ${data.year} - ${data.description}`);
    }
}

function onWindowResize() {
    const container = document.getElementById('prime-radiant-sphere');
    if (!container) return;
    
    const width = container.clientWidth;
    const height = container.clientHeight;
    
    camera.aspect = width / height;
    camera.updateProjectionMatrix();
    renderer.setSize(width, height);
}

// Initialiser au chargement du DOM
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        setTimeout(initPrimeRadiant, 500);
    });
} else {
    setTimeout(initPrimeRadiant, 500);
}
