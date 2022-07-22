const btnMenuOpen = document.getElementById('btn-open')
const btnMenuOpen2 = document.getElementById('btn-open-2')
const btnMenuClose = document.getElementById('btn-close')
const menu = document.querySelector(".comment-nav");

const toggleMenu = function () {
    menu.classList.toggle("open");
}

btnMenuOpen.addEventListener("click", function (e) {
    e.stopPropagation();
    toggleMenu();
});

btnMenuOpen2.addEventListener("click", function (e) {
    e.stopPropagation();
    toggleMenu();
});

btnMenuClose.addEventListener("click", function (e) {
    e.stopPropagation();
    toggleMenu();
});

document.addEventListener("click", function (e) {
    const target = e.target;
    const its_menu = target == menu || menu.contains(target);
    const its_btnMenu = target == btnMenuOpen;
    const menu_is_active = menu.classList.contains("open");

    if (!its_menu && !its_btnMenu && menu_is_active) {
        toggleMenu();
    }
});