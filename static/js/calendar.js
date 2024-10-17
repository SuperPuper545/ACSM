let currentYear = new Date().getFullYear();
let currentMonth = new Date().getMonth();
let selectedDates = JSON.parse(localStorage.getItem('selectedDates')) || {};
function createCalendar(year, month) {
    const daysInMonth = new Date(year, month + 1, 0).getDate();
    const firstDayOfWeek = new Date(year, month, 1).getDay();
    const offset = (firstDayOfWeek === 0) ? 6 : firstDayOfWeek - 1; // Коррекция начального дня недели
    const calendarTable = document.getElementById('calendar');
    calendarTable.innerHTML = '';
    // Set month and year
    document.getElementById('monthYear').innerText = `${getMonthName(month)} ${year}`;
    // Create table header
    const headerRow = document.createElement('tr');
    ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс'].forEach(day => {
        const th = document.createElement('th');
        th.textContent = day;
        headerRow.appendChild(th);
    });
    calendarTable.appendChild(headerRow);
    // Fill the calendar with dates
    let date = 1;
    for (let i = 0; i < 6; i++) {
        const row = document.createElement('tr');
        for (let j = 0; j < 7; j++) {
            if ((i === 0 && j < offset) || date > daysInMonth) {
                const emptyCell = document.createElement('td');
                row.appendChild(emptyCell);
            } else {
                const cell = document.createElement('td');
                cell.textContent = date;
                cell.dataset.date = `${year}-${month + 1}-${date}`;
                if (selectedDates[cell.dataset.date]) {
                    cell.classList.add('selected');
                }
                if (j === 5 || j === 6) { // Check if it's Saturday or Sunday
                    cell.classList.add('weekend');
                }
                cell.addEventListener('click', toggleSelect);
                row.appendChild(cell);
                date++;
            }
        }
        calendarTable.appendChild(row);
    }
}
function getMonthName(month) {
    const monthNames = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь', 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь'];
    return monthNames[month];
}
function prevMonth() {
    currentMonth--;
    if (currentMonth < 0) {
        currentMonth = 11;
        currentYear--;
    }
    createCalendar(currentYear, currentMonth);
}
function nextMonth() {
    currentMonth++;
    if (currentMonth > 11) {
        currentMonth = 0;
        currentYear++;
    }
    createCalendar(currentYear, currentMonth);
}
function toggleSelect() {
    const date = this.dataset.date;
    if (selectedDates[date]) {
        delete selectedDates[date];
    } else {
        selectedDates[date] = true;
    }
    localStorage.setItem('selectedDates', JSON.stringify(selectedDates));
    this.classList.toggle('selected');
}
// Create the calendar for the current year and month
createCalendar(currentYear, currentMonth);