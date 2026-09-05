document.addEventListener('DOMContentLoaded', function () {
    var revealElements = document.querySelectorAll('.reveal');
    revealElements.forEach(function (element) {
        element.classList.add('revealed');
    });
});
