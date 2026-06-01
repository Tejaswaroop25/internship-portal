document.addEventListener('DOMContentLoaded', () => {
    // 1. Auto-Dismiss Flash Alerts
    const alerts = document.querySelectorAll('.alert');
    alerts.forEach(alert => {
        // Automatically slide out and remove alert after 4.5 seconds
        setTimeout(() => {
            alert.style.transition = 'all 0.5s cubic-bezier(0.4, 0, 0.2, 1)';
            alert.style.opacity = '0';
            alert.style.transform = 'translateX(100px)';
            setTimeout(() => {
                alert.remove();
            }, 500);
        }, 4500);

        // Allow closing manually
        const closeBtn = alert.querySelector('.alert-close');
        if (closeBtn) {
            closeBtn.addEventListener('click', () => {
                alert.remove();
            });
        }
    });

    // 2. Interactive Skills Tag Widget for Profile & Registration Pages
    const skillsInput = document.getElementById('skills-input-raw');
    const tagsContainer = document.getElementById('skills-tags-container');
    const hiddenSkillsInput = document.getElementById('hidden-skills-value');

    if (skillsInput && tagsContainer && hiddenSkillsInput) {
        let skillsList = hiddenSkillsInput.value.split(',')
            .map(s => s.strip ? s.strip() : s.trim())
            .filter(s => s.length > 0);

        // Sync visual tags from active list
        const renderTags = () => {
            tagsContainer.innerHTML = '';
            skillsList.forEach((skill, index) => {
                const tagEl = document.createElement('span');
                tagEl.className = 'badge badge-reviewed';
                tagEl.style.display = 'inline-flex';
                tagEl.style.alignItems = 'center';
                tagEl.style.gap = '6px';
                tagEl.style.margin = '4px';
                tagEl.style.cursor = 'pointer';
                tagEl.innerHTML = `${skill} <strong style="font-size: 14px; opacity: 0.6">&times;</strong>`;
                
                // Clicking tag removes it
                tagEl.addEventListener('click', () => {
                    skillsList.splice(index, 1);
                    updateHiddenInput();
                    renderTags();
                });
                tagsContainer.appendChild(tagEl);
            });
        };

        const updateHiddenInput = () => {
            hiddenSkillsInput.value = skillsList.join(', ');
        };

        // Render initial tags on load
        renderTags();

        // Listen to keystrokes on the visible tag input
        skillsInput.addEventListener('keydown', (e) => {
            if (e.key === 'Enter' || e.key === ',') {
                e.preventDefault();
                const newSkill = skillsInput.value.trim();
                
                // Add skill if it's not empty and not already present
                if (newSkill.length > 0 && !skillsList.some(s => s.toLowerCase() === newSkill.toLowerCase())) {
                    skillsList.push(newSkill);
                    updateHiddenInput();
                    renderTags();
                }
                skillsInput.value = '';
            }
        });

        // Also add on blur (when user focus moves away)
        skillsInput.addEventListener('blur', () => {
            const newSkill = skillsInput.value.trim();
            if (newSkill.length > 0 && !skillsList.some(s => s.toLowerCase() === newSkill.toLowerCase())) {
                skillsList.push(newSkill);
                updateHiddenInput();
                renderTags();
            }
            skillsInput.value = '';
        });
    }

    // 3. Elegant Client-Side Confirms for Destructive Actions (Deletions)
    const deleteForms = document.querySelectorAll('.delete-confirm-form');
    deleteForms.forEach(form => {
        form.addEventListener('submit', (e) => {
            const confirmMsg = form.dataset.confirmMessage || 'Are you absolutely sure you want to delete this? This action is permanent.';
            if (!confirm(confirmMsg)) {
                e.preventDefault();
            }
        });
    });

    // 4. Role Selection Custom Card toggling in Registration form
    const roleRadios = document.querySelectorAll('.role-selector input[type="radio"]');
    const studentFormSection = document.getElementById('student-fields-section');
    const companyFormSection = document.getElementById('company-fields-section');

    const updateRegistrationRoleFields = () => {
        let selectedRole = '';
        roleRadios.forEach(radio => {
            const parentLabel = radio.closest('.role-option');
            if (radio.checked) {
                selectedRole = radio.value;
                if (parentLabel) parentLabel.classList.add('selected');
            } else {
                if (parentLabel) parentLabel.classList.remove('selected');
            }
        });

        // Show/Hide relevant profile forms depending on role selected
        if (selectedRole === 'student') {
            if (studentFormSection) studentFormSection.style.display = 'block';
            if (companyFormSection) companyFormSection.style.display = 'none';
        } else if (selectedRole === 'company') {
            if (studentFormSection) studentFormSection.style.display = 'none';
            if (companyFormSection) companyFormSection.style.display = 'block';
        }
    };

    if (roleRadios.length > 0) {
        roleRadios.forEach(radio => {
            radio.addEventListener('change', updateRegistrationRoleFields);
        });
        // Initial sync on load
        updateRegistrationRoleFields();
    }
});
