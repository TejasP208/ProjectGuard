document.addEventListener('DOMContentLoaded', () => {
    fetchProjects();
});

async function fetchProjects() {
    const container = document.getElementById('projects-container');
    container.innerHTML = `
        <div style="color: var(--text-secondary); text-align: center; width: 100%; grid-column: 1 / -1; padding: 4rem 0;">
            <i class="ph ph-folder-dashed" style="font-size: 4rem; margin-bottom: 1rem; opacity: 0.5;"></i>
            <h3 style="color: var(--text-primary); margin-bottom: 0.5rem; font-size: 1.5rem;">No Projects Yet</h3>
            <p style="color: var(--text-muted);">When you submit a project, you'll be able to see it here.</p>
        </div>
    `;
}
