// Сохраняем выбранную секцию в localStorage
document.querySelectorAll('input[name="tab-control"]').forEach(function(tab) {
    tab.addEventListener('change', function() {
        localStorage.setItem('selectedTab', this.id);
    });
});
// Восстанавливаем выбранную секцию при загрузке страницы
window.addEventListener('load', function() {
    var selectedTabId = localStorage.getItem('selectedTab');
    if (selectedTabId) {
        var selectedTab = document.getElementById(selectedTabId);
        if (selectedTab) {
            selectedTab.checked = true;
        }
    }
});