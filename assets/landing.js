document.addEventListener('DOMContentLoaded', function () {
    var revealElements = document.querySelectorAll('.reveal');
    revealElements.forEach(function (element) {
        element.classList.add('revealed');
    });

    var mapFrame = document.querySelector('.visitor-map-widget');
    if (!mapFrame) return;

    // Scale the provider's fixed-size map without requesting another counted visit.
    function observeVisitorMap() {
        var widget = mapFrame.querySelector('#mapmyvisitors-widget');
        if (!widget) return;

        insertionObserver.disconnect();
        var resizeObserver = new ResizeObserver(function () {
            if (!widget.offsetWidth) return;

            var scale = Math.min(1, mapFrame.clientWidth / widget.offsetWidth);
            mapFrame.style.setProperty('--visitor-map-scale', scale);
            widget.style.transform = 'translateX(-50%) scale(' + scale + ')';
            mapFrame.style.height = widget.offsetHeight * scale + 'px';
        });
        resizeObserver.observe(mapFrame);
        resizeObserver.observe(widget);
    }

    var insertionObserver = new MutationObserver(observeVisitorMap);
    insertionObserver.observe(mapFrame, { childList: true });
    observeVisitorMap();
});
