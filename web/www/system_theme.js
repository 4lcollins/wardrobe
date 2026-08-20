document.addEventListener("DOMContentLoaded", function() {
    const isDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const targetTheme = isDark ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', targetTheme);
    
    // Use the namespaced ID passed from Python
    const toggle = document.getElementById('{{ toggle_id }}');
    if (toggle) { toggle.value = targetTheme; }
});
window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
    const newTheme = e.matches ? 'dark' : 'light';
    document.documentElement.setAttribute('data-bs-theme', newTheme);
});