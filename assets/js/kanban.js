// kanban.js

document.addEventListener('DOMContentLoaded', () => {
    // Select the filter and sort dropdowns
    const statusFilter = document.getElementById('status-filter');
    const priorityFilter = document.getElementById('priority-filter');
    const sortDropdown = document.getElementById('sort-by');
    const kanbanContainer = document.querySelector('.kanban-container');

    // Add event listeners to the filters and sort dropdown
    statusFilter.addEventListener('change', updateKanbanBoard);
    priorityFilter.addEventListener('change', updateKanbanBoard);
    sortDropdown.addEventListener('change', updateKanbanBoard);

    // Initial board update on page load
    updateKanbanBoard();

    // The main function to filter and sort the tasks
    function updateKanbanBoard() {
        // Get the selected values from the dropdowns
        const selectedStatus = statusFilter.value;
        const selectedPriority = priorityFilter.value;
        const selectedSort = sortDropdown.value;

        // Get all task cards on the page
        const allTaskCards = document.querySelectorAll('.task-card');
        const tasks = Array.from(allTaskCards);

        // Filter the tasks based on the selected status and priority
        const filteredTasks = tasks.filter(task => {
            const taskStatus = task.getAttribute('data-status');
            const taskPriority = task.getAttribute('data-priority');

            const statusMatch = selectedStatus === 'All' || taskStatus === selectedStatus;
            const priorityMatch = selectedPriority === 'All' || taskPriority === selectedPriority;

            return statusMatch && priorityMatch;
        });

        // Sort the filtered tasks
        const sortedTasks = sortTasks(filteredTasks, selectedSort);

        // Clear all existing kanban columns
        document.querySelectorAll('.kanban-column-content').forEach(column => {
            column.innerHTML = '';
        });

        // Re-append the sorted tasks to their correct columns
        sortedTasks.forEach(task => {
            const taskStatus = task.getAttribute('data-status').replace(/\s/g, '-'); // "In Progress" -> "In-Progress"
            const columnContent = document.querySelector(`#column-${taskStatus}`);
            if (columnContent) {
                columnContent.appendChild(task);
            }
        });
    }

    // Function to handle the sorting logic
    function sortTasks(tasks, sortType) {
        return tasks.sort((a, b) => {
            switch (sortType) {
                case 'due_date_asc':
                    const dateA = new Date(a.getAttribute('data-due-date'));
                    const dateB = new Date(b.getAttribute('data-due-date'));
                    return dateA - dateB;
                case 'due_date_desc':
                    const dateADesc = new Date(a.getAttribute('data-due-date'));
                    const dateBDesc = new Date(b.getAttribute('data-due-date'));
                    return dateBDesc - dateADesc;
                case 'priority':
                    const priorityOrder = { 'High': 3, 'Medium': 2, 'Low': 1 };
                    const priorityA = priorityOrder[a.getAttribute('data-priority')];
                    const priorityB = priorityOrder[b.getAttribute('data-priority')];
                    return priorityB - priorityA; // Sort High to Low
                case 'creation_date_asc':
                    const createdA = new Date(a.getAttribute('data-created-at'));
                    const createdB = new Date(b.getAttribute('data-created-at'));
                    return createdA - createdB;
                case 'creation_date_desc':
                    const createdADesc = new Date(a.getAttribute('data-created-at'));
                    const createdBDesc = new Date(b.getAttribute('data-created-at'));
                    return createdBDesc - createdADesc;
                default:
                    return 0;
            }
        });
    }
});
