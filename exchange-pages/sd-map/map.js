(() => {
    const section = document.querySelector('#sd-travel-map');
    const scriptUrl = new URL(document.currentScript.src);
    const assetUrl = (file) => {
        const url = new URL(file, scriptUrl);
        url.search = scriptUrl.search;
        return url;
    };
    const pick = section.querySelector('select');
    const name = section.querySelector('#sd-map-place-name');
    const description = section.querySelector('.sd-map__description');
    const photo = section.querySelector('.sd-map__photo');
    const photoPlaceholder = photo.querySelector('span');
    const directions = section.querySelector('.sd-map__directions');
    const directionsLink = section.querySelector('.sd-map__directions-link');
    const steps = section.querySelector('.sd-map__steps');
    const note = section.querySelector('.sd-map__route-note');
    const message = section.querySelector('.sd-map__map-message');
    const overview = section.querySelector('.sd-map__overview');
    const canvas = section.querySelector('.sd-map__canvas');
    const initialDescription = description.textContent;

    let selected;

    function walkingLine(layer, coordinates) {
        if (L.latLng(coordinates[0]).distanceTo(coordinates.at(-1)) < 22) return;
        L.polyline(coordinates, {
            color: '#424f4a', weight: 3, dashArray: '5 7', opacity: 0.9, interactive: false,
        }).addTo(layer);
    }

    function fit(map, coordinates) {
        map.fitBounds(coordinates, {padding: [32, 39], maxZoom: 15, animate: false});
    }

    function marker(map, place, label) {
        const campus = Boolean(label);
        const size = campus ? [56, 25] : [23, 23];
        const icon = L.divIcon({
            className: `sd-map__pin${campus ? ' sd-map__pin--campus' : ''}`,
            html: label || '',
            iconSize: size,
        });
        const pin = L.marker(place.coordinates, {icon, title: place.name, autoPanOnFocus: false})
            .addTo(map);
        pin.getElement().setAttribute('aria-label', place.name);
        const tooltip = document.createElement('span');
        tooltip.textContent = place.name;
        pin.bindTooltip(tooltip, {direction: 'top', offset: [0, -12]});
        pin.on('keydown', (event) => {
            if (event.originalEvent.key === ' ') {
                event.originalEvent.preventDefault();
                pin.fire('click');
            }
        });
        return pin;
    }

    function showPhoto(place) {
        photo.replaceChildren(photoPlaceholder);
        photo.hidden = !place;
        photoPlaceholder.hidden = false;
        if (!place?.photo) return;

        const image = new Image();
        image.alt = place.photo.alt || place.name;
        image.decoding = 'async';
        image.addEventListener('load', () => {
            if (selected !== place) return;
            photoPlaceholder.hidden = true;
            photo.append(image);
        }, {once: true});
        image.src = assetUrl(place.photo.src).href;
    }

    function addStep(label, detail, color) {
        const item = document.createElement('li');
        const badge = document.createElement('span');
        const text = document.createElement('span');
        badge.className = 'sd-map__line';
        if (color) badge.style.setProperty('--sd-line-color', color);
        else badge.classList.add('sd-map__line--walk');
        badge.textContent = label;
        text.textContent = detail;
        item.append(badge, text);
        steps.append(item);
    }

    function renderDetails(place, data) {
        name.textContent = place?.name ?? data.origin.name;
        description.textContent = place?.description ?? initialDescription;
        showPhoto(place);
        directions.hidden = !place;
        if (!place) return;

        const {rides, walk} = place;
        steps.replaceChildren();
        if (rides.length && rides[0][1] !== 'campus') {
            addStep('步行', `从 Central Campus 到 ${data.stops[rides[0][1]]}。`);
        }
        for (const [line, from, to] of rides) {
            addStep(data.lines[line].name, `${data.stops[from]} → ${data.stops[to]}`, data.lines[line].color);
        }
        if (walk) addStep('步行', walk);
        setNote(place);
        const link = new URL('https://www.google.com/maps/dir/');
        link.search = new URLSearchParams({
            api: '1',
            origin: 'UC San Diego Central Campus Station, San Diego',
            destination: place.coordinates.join(','),
            travelmode: rides.length ? 'transit' : 'walking',
        });
        directionsLink.href = link.href;
        directionsLink.textContent = rides.length ? '在 Google Maps 查班次' : '在 Google Maps 查看步行导航';
    }

    function setNote(place, extra = '') {
        note.textContent = [place.note, extra].filter(Boolean).join(' ');
        note.hidden = !note.textContent;
    }

    function drawRoute(view, place, data, tracks) {
        const {map, routeLayer} = view;
        const origin = data.origin.coordinates;
        const destination = place.coordinates;
        const legs = place.rides.map((ride) => ({
            color: data.lines[ride[0]].color,
            points: tracks[ride.join(':')],
        }));
        const via = place.via ?? [];
        const bounds = [origin, ...via, destination];
        if (legs.some(({points}) => !points)) {
            setNote(place, '暂时无法绘制线路，乘车站点见上方。');
            fit(map, bounds);
            return;
        }
        let previous = origin;
        for (const {points, color} of legs) {
            const start = points[0];
            walkingLine(routeLayer, [previous, start]);
            const style = {interactive: false, lineJoin: 'round', lineCap: 'round'};
            L.polyline(points, {...style, color: '#fff', weight: 8, opacity: 0.9}).addTo(routeLayer);
            L.polyline(points, {...style, color, weight: 4.5}).addTo(routeLayer);
            previous = points.at(-1);
            for (const stop of [start, previous]) {
                L.circleMarker(stop, {radius: 4, color, weight: 2, fillColor: '#fff', fillOpacity: 1, interactive: false})
                    .addTo(routeLayer);
            }
            bounds.push(...points);
        }
        walkingLine(routeLayer, [previous, ...via, destination]);
        fit(map, bounds);
    }

    function addOptions(places) {
        const groups = new Map();
        for (const place of places) {
            if (!groups.has(place.group)) {
                const group = document.createElement('optgroup');
                group.label = place.group;
                groups.set(place.group, group);
                pick.append(group);
            }
            groups.get(place.group).append(new Option(place.name, place.id));
        }
        pick.disabled = false;
    }

    function createMap(data, bounds, selectPlace) {
        if (!window.L) return null;
        const map = L.map(canvas, {scrollWheelZoom: false, zoomSnap: 0.25, maxZoom: 19});
        fit(map, bounds);
        const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        }).addTo(map);
        const routeLayer = L.layerGroup().addTo(map);
        const campus = marker(map, data.origin, 'UCSD');
        campus.setZIndexOffset(550).on('click', () => selectPlace('campus'));
        const pins = data.places.map((place) => {
            const pin = marker(map, place).on('click', () => selectPlace(place.id));
            return {id: place.id, pin};
        });
        tiles.on('load', () => {
            message.hidden = Boolean(canvas.querySelector('.leaflet-tile-loaded'));
            message.textContent = '底图暂时无法加载，仍可选择景点。';
        });
        new ResizeObserver(() => map.invalidateSize({pan: false})).observe(canvas);
        overview.hidden = false;
        return {map, routeLayer, pins};
    }

    async function readJson(file) {
        const response = await fetch(assetUrl(file));
        if (!response.ok) throw new Error(`Could not load ${file}`);
        return response.json();
    }

    async function initialize() {
        const [data, tracks] = await Promise.all([
            readJson('places.json'),
            readJson('transit.json').catch(() => ({})),
        ]);
        const byId = new Map(data.places.map((place) => [place.id, place]));
        const bounds = [data.origin.coordinates, ...data.places.map((place) => place.coordinates)];

        function selectPlace(id) {
            selected = byId.get(id);
            pick.value = selected?.id ?? '';
            renderDetails(selected, data);
            if (id === 'campus') description.textContent = data.origin.description;
            if (!view) return;

            view.map.invalidateSize({pan: false});
            view.routeLayer.clearLayers();
            for (const {id: pinId, pin} of view.pins) {
                const active = pinId === id;
                pin.getElement().classList.toggle('sd-map__pin--selected', active);
                pin.getElement().setAttribute('aria-pressed', String(active));
                pin.setZIndexOffset(active ? 500 : 0);
            }
            if (selected) {
                drawRoute(view, selected, data, tracks);
            } else if (id === 'campus') {
                view.map.setView(data.origin.coordinates, 14, {animate: false});
            } else {
                fit(view.map, bounds);
            }
        }

        addOptions(data.places);
        const view = createMap(data, bounds, selectPlace);
        if (!view) message.textContent = '地图暂时无法加载。可从景点列表查看说明和路线。';
        pick.addEventListener('change', () => selectPlace(pick.value));
        overview.addEventListener('click', () => selectPlace(''));
    }

    initialize().catch(() => {
        message.textContent = '暂时无法加载游记地图。景点介绍仍可以在下方阅读。';
    });
})();
