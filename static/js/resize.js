// Resizable Panels Functionality

let isResizing = false;
let currentResizeHandle = null;
let startY = 0;
let startHeight = 0;
let currentPanel = null;

function initResizablePanels() {
    // Add resize handles and make panels resizable
    const handles = document.querySelectorAll('.resize-handle');
    
    handles.forEach(handle => {
        handle.addEventListener('mousedown', startResize);
    });
    
    // Also enable CSS resize for panels
    document.addEventListener('mousemove', handleResize);
    document.addEventListener('mouseup', stopResize);
    
    // Save panel sizes to localStorage
    loadPanelSizes();
}

function startResize(e) {
    e.preventDefault();
    isResizing = true;
    currentResizeHandle = e.target;
    currentPanel = document.getElementById(currentResizeHandle.dataset.target);
    
    if (!currentPanel) return;
    
    startY = e.clientY;
    startHeight = currentPanel.offsetHeight;
    
    document.body.style.cursor = 'ns-resize';
    document.body.style.userSelect = 'none';
}

function handleResize(e) {
    if (!isResizing || !currentPanel) return;
    
    const deltaY = e.clientY - startY;
    const isBottomHandle = currentResizeHandle.classList.contains('resize-handle-bottom');
    
    let newHeight;
    if (isBottomHandle) {
        newHeight = startHeight + deltaY;
    } else {
        newHeight = startHeight - deltaY;
    }
    
    // Apply min/max constraints
    const minHeight = parseInt(getComputedStyle(currentPanel).minHeight) || 100;
    const maxHeight = parseInt(getComputedStyle(currentPanel).maxHeight) || window.innerHeight;
    
    newHeight = Math.max(minHeight, Math.min(maxHeight, newHeight));
    
    currentPanel.style.height = newHeight + 'px';
    currentPanel.style.flexShrink = '0';
    
    // Update CodeMirror if it's the editor
    if (currentPanel.id === 'editorPanel' && window.editor) {
        window.editor.refresh();
    }
}

function stopResize() {
    if (isResizing && currentPanel) {
        // Save panel size to localStorage
        savePanelSize(currentPanel.id, currentPanel.style.height);
    }
    
    isResizing = false;
    currentResizeHandle = null;
    currentPanel = null;
    document.body.style.cursor = '';
    document.body.style.userSelect = '';
}

function savePanelSize(panelId, height) {
    try {
        const sizes = JSON.parse(localStorage.getItem('panelSizes') || '{}');
        sizes[panelId] = height;
        localStorage.setItem('panelSizes', JSON.stringify(sizes));
    } catch (e) {
        console.error('Error saving panel size:', e);
    }
}

function loadPanelSizes() {
    try {
        const sizes = JSON.parse(localStorage.getItem('panelSizes') || '{}');
        
        Object.keys(sizes).forEach(panelId => {
            const panel = document.getElementById(panelId);
            if (panel && sizes[panelId]) {
                panel.style.height = sizes[panelId];
                panel.style.flexShrink = '0';
            }
        });
        
        // Refresh CodeMirror after loading sizes
        if (window.editor) {
            setTimeout(() => window.editor.refresh(), 100);
        }
    } catch (e) {
        console.error('Error loading panel sizes:', e);
    }
}

// Make sidebar resizable horizontally
function initSidebarResize() {
    const sidebar = document.querySelector('.sidebar');
    if (!sidebar) return;
    
    let isResizingSidebar = false;
    let startX = 0;
    let startWidth = 0;
    
    const handle = document.createElement('div');
    handle.className = 'resize-handle resize-handle-right';
    sidebar.appendChild(handle);
    
    handle.addEventListener('mousedown', (e) => {
        e.preventDefault();
        isResizingSidebar = true;
        startX = e.clientX;
        startWidth = sidebar.offsetWidth;
        document.body.style.cursor = 'ew-resize';
        document.body.style.userSelect = 'none';
    });
    
    document.addEventListener('mousemove', (e) => {
        if (!isResizingSidebar) return;
        
        const deltaX = e.clientX - startX;
        const newWidth = Math.max(200, Math.min(600, startWidth + deltaX));
        sidebar.style.width = newWidth + 'px';
        sidebar.style.flexShrink = '0';
        
        // Save sidebar width
        try {
            localStorage.setItem('sidebarWidth', newWidth + 'px');
        } catch (e) {
            console.error('Error saving sidebar width:', e);
        }
    });
    
    document.addEventListener('mouseup', () => {
        if (isResizingSidebar) {
            isResizingSidebar = false;
            document.body.style.cursor = '';
            document.body.style.userSelect = '';
        }
    });
    
    // Load saved sidebar width
    try {
        const savedWidth = localStorage.getItem('sidebarWidth');
        if (savedWidth) {
            sidebar.style.width = savedWidth;
            sidebar.style.flexShrink = '0';
        }
    } catch (e) {
        console.error('Error loading sidebar width:', e);
    }
}

// Initialize on page load
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initResizablePanels();
        initSidebarResize();
    });
} else {
    initResizablePanels();
    initSidebarResize();
}

