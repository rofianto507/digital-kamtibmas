// @ts-nocheck
/** @odoo-module **/

import { Component, onMounted, onWillDestroy, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

// Pusat default: Palembang
const DEFAULT_CENTER = [-2.9761, 104.7754];
const DEFAULT_ZOOM   = 13;

class DkmMapPicker extends Component {
    static template = "digital_kamtibmas.MapPicker";
    static props    = { ...standardFieldProps };

    setup() {
        this.mapRef  = useRef("mapContainer");
        this._map    = null;
        this._marker = null;

        onMounted(() => this._initMap());
        onWillDestroy(() => {
            if (this._map) { this._map.remove(); this._map = null; }
        });
    }

    get lat() { return this.props.record.data.lat || 0; }
    get lng() { return this.props.record.data.lng || 0; }
    get readonly() { return this.props.readonly; }

    _initMap() {
        const el = this.mapRef.el;
        if (!el || typeof L === 'undefined') return;

        const hasCoord = this.lat && this.lng;
        const center   = hasCoord ? [this.lat, this.lng] : DEFAULT_CENTER;

        this._map = L.map(el, { zoomControl: true }).setView(center, DEFAULT_ZOOM);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org">OpenStreetMap</a>',
            maxZoom: 19,
        }).addTo(this._map);

        if (hasCoord) this._placeMarker(this.lat, this.lng);

        if (!this.readonly) {
            this._map.on('click', (e) => {
                this._placeMarker(e.latlng.lat, e.latlng.lng);
                this._save(e.latlng.lat, e.latlng.lng);
            });
        }

        // Fix tile rendering setelah DOM settle
        setTimeout(() => this._map && this._map.invalidateSize(), 200);
    }

    _placeMarker(lat, lng) {
        if (this._marker) {
            this._marker.setLatLng([lat, lng]);
        } else {
            this._marker = L.marker([lat, lng], {
                draggable: !this.readonly,
                icon: L.icon({
                    iconUrl:       '/digital_kamtibmas/static/lib/leaflet/images/marker-icon.png',
                    shadowUrl:     '/digital_kamtibmas/static/lib/leaflet/images/marker-shadow.png',
                    iconSize:      [25, 41],
                    iconAnchor:    [12, 41],
                    popupAnchor:   [1, -34],
                    shadowSize:    [41, 41],
                }),
            }).addTo(this._map);

            if (!this.readonly) {
                this._marker.on('dragend', (e) => {
                    const ll = e.target.getLatLng();
                    this._save(ll.lat, ll.lng);
                });
            }
        }
        this._map.panTo([lat, lng]);
    }

    _save(lat, lng) {
        this.props.record.update({ lat, lng });
    }
}

registry.category("fields").add("dkm_map_picker", {
    component: DkmMapPicker,
    supportedTypes: ["float"],
});
