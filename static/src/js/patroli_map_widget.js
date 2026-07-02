// @ts-nocheck
/** @odoo-module **/

import { Component, onMounted, onWillDestroy, useEffect, useRef } from "@odoo/owl";
import { registry } from "@web/core/registry";

class PatroliRouteMap extends Component {
    static template = "digital_kamtibmas.PatroliRouteMap";
    static props    = { "*": { optional: true } };

    setup() {
        this.mapRef       = useRef("patroliRouteMap");
        this._map         = null;
        this._routeLayers = [];

        onMounted(() => {
            this._initMap();
        });

        // Re-render rute setiap kali isi titik_ids berubah
        useEffect(
            () => {
                const timer = setTimeout(() => this._renderRoute(), 150);
                return () => clearTimeout(timer);
            },
            () => {
                const recs = this.props.record?.data?.titik_ids?.records || [];
                const key  = recs.map(r => {
                    const d = r.data;
                    const t = d.waktu_rekam
                        ? (d.waktu_rekam.toMillis ? d.waktu_rekam.toMillis() : String(d.waktu_rekam))
                        : '';
                    return `${d.latitude}|${d.longitude}|${t}`;
                }).join(';');
                return [recs.length, key];
            }
        );

        onWillDestroy(() => {
            if (this._map) { this._map.remove(); this._map = null; }
        });
    }

    _initMap() {
        const el = this.mapRef.el;
        if (!el || typeof L === 'undefined') return;

        this._map = L.map(el, { zoomControl: true }).setView([-2.9761, 104.7754], 13);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org">OpenStreetMap</a>',
            maxZoom: 19,
        }).addTo(this._map);

        setTimeout(() => {
            this._map && this._map.invalidateSize();
            this._renderRoute();
        }, 250);
    }

    _clearRoute() {
        for (const layer of this._routeLayers) {
            try { this._map && this._map.removeLayer(layer); } catch (e) {}
        }
        this._routeLayers = [];
    }

    _renderRoute() {
        if (!this._map) return;
        this._clearRoute();

        const recs = this.props.record?.data?.titik_ids?.records || [];

        const points = recs
            .map(r => ({
                lat:   r.data.latitude  || 0,
                lng:   r.data.longitude || 0,
                waktu: r.data.waktu_rekam,
            }))
            .filter(p => p.lat && p.lng)
            .sort((a, b) => {
                const ta = this._waktuMs(a.waktu);
                const tb = this._waktuMs(b.waktu);
                return ta - tb;
            });

        if (!points.length) return;

        // Polyline rute — garis putus-putus
        const latlngs = points.map(p => [p.lat, p.lng]);
        const polyline = L.polyline(latlngs, {
            color: '#71639e', weight: 3, opacity: 0.85,
            dashArray: '10, 7',
        }).addTo(this._map);
        this._routeLayers.push(polyline);

        // Marker bernomor (semua pakai nomor, warna beda untuk titik pertama/terakhir)
        points.forEach((p, i) => {
            const isFirst = i === 0;
            const isLast  = i === points.length - 1;
            const bg      = isFirst ? '#10b981' : isLast ? '#ef4444' : '#71639e';
            const label   = `${i + 1}`;

            const icon = L.divIcon({
                className: '',
                html: `<div style="
                    background:${bg};color:#fff;border-radius:50%;
                    width:28px;height:28px;display:flex;
                    align-items:center;justify-content:center;
                    font-weight:700;font-size:13px;
                    border:2px solid #fff;
                    box-shadow:0 2px 6px rgba(0,0,0,.35);
                ">${label}</div>`,
                iconSize:   [28, 28],
                iconAnchor: [14, 14],
            });

            const waktuStr = this._fmtWaktu(p.waktu);
            const popup = `
<div style="font-family:inherit;min-width:160px">
  <div style="background:${bg};color:#fff;padding:6px 10px;margin:-14px -20px 8px;font-weight:700;font-size:12px;border-radius:3px 3px 0 0">
    ${isFirst ? '🚀 Titik Mulai' : isLast ? '🏁 Titik Akhir' : `📍 Titik ${i + 1}`}
  </div>
  <div style="font-size:12px;padding:0 2px 4px">
    <div style="margin-bottom:4px">🕐 ${waktuStr}</div>
    <div style="color:#9ca3af;font-size:11px">${p.lat.toFixed(6)}, ${p.lng.toFixed(6)}</div>
  </div>
</div>`;

            const marker = L.marker([p.lat, p.lng], { icon }).addTo(this._map);
            marker.bindPopup(popup, { maxWidth: 220 });
            this._routeLayers.push(marker);
        });

        // Fit ke semua titik
        try {
            this._map.fitBounds(polyline.getBounds(), { padding: [40, 40] });
        } catch (e) {}
    }

    _waktuMs(waktu) {
        if (!waktu) return 0;
        if (typeof waktu === 'object' && waktu.toMillis) return waktu.toMillis();
        try { return new Date(String(waktu).replace(' ', 'T') + 'Z').getTime(); }
        catch (e) { return 0; }
    }

    _fmtWaktu(waktu) {
        if (!waktu) return '-';
        // luxon DateTime (dari form OWL — sudah dalam timezone lokal user)
        if (typeof waktu === 'object' && waktu.toFormat) {
            return waktu.toFormat('yyyy-MM-dd HH:mm');
        }
        // string UTC dari server — convert ke WIB
        try {
            const d = new Date(String(waktu).replace(' ', 'T') + 'Z');
            const w = new Date(d.getTime() + 7 * 3600 * 1000);
            const p = n => String(n).padStart(2, '0');
            return `${w.getUTCFullYear()}-${p(w.getUTCMonth()+1)}-${p(w.getUTCDate())} ` +
                   `${p(w.getUTCHours())}:${p(w.getUTCMinutes())}`;
        } catch (e) { return String(waktu).slice(0, 16); }
    }

    get titikCount() {
        const recs = this.props.record?.data?.titik_ids?.records || [];
        return recs.filter(r => r.data.latitude && r.data.longitude).length;
    }

    _bearing(from, to) {
        const toRad = d => d * Math.PI / 180;
        const toDeg = r => r * 180 / Math.PI;
        const dLng  = toRad(to[1] - from[1]);
        const lat1  = toRad(from[0]);
        const lat2  = toRad(to[0]);
        const y     = Math.sin(dLng) * Math.cos(lat2);
        const x     = Math.cos(lat1) * Math.sin(lat2) - Math.sin(lat1) * Math.cos(lat2) * Math.cos(dLng);
        return (toDeg(Math.atan2(y, x)) + 360) % 360;
    }
}

registry.category("view_widgets").add("dkm_patroli_route_map", {
    component: PatroliRouteMap,
});
