// @ts-nocheck
/** @odoo-module **/

import { Component, useState, onMounted, onWillDestroy, useRef, useEffect } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

const BULAN            = ['Jan','Feb','Mar','Apr','Mei','Jun','Jul','Agu','Sep','Okt','Nov','Des'];
const PALEMBANG_CENTER = [-2.9761, 104.7754];

const ANTR_STATE_LABEL = {
    menunggu:   'Menunggu',
    konfirmasi: 'Dikonfirmasi',
    dipanggil:  'Dipanggil',
    selesai:    'Selesai',
    batal:      'Batal',
};

const PERIOD_LABEL = {
    this_month: 'Bulan Ini',
    last_month: 'Bulan Lalu',
    this_year:  'Tahun Ini',
    all_time:   'Semua Waktu',
};

class DkmDashboard extends Component {
    static template = "digital_kamtibmas.Dashboard";
    static props    = ["*"];

    setup() {
        this.orm    = useService("orm");
        this.action = useService("action");

        this.state = useState({
            activeSection:    'satlantas',
            sidebarCollapsed: false,
            period:           'this_month',
            loading:      true,
            todayLabel:   '',
            calendarYear: new Date().getFullYear(),
            kpi: {
                antrTotal: 0, antrMenunggu: 0, antrAktif: 0, antrSelesai: 0,
                lakaTotal: 0, lakaBaru: 0, lakaDisproses: 0, lakaSelesai: 0,
            },
            trendData:     [],
            layanData:     [],
            calendarData:  [],
            activeAntrian: [],
            lakaPending:   [],
            lakaPoints:    [],
            // ── Satnarkoba ─────────────────────────────────────────────
            satkoba: {
                loading: false,
                kpi: {
                    konTotal: 0, konMenunggu: 0, konProses: 0, konSelesai: 0,
                    rehTotal: 0, rehMenunggu: 0, rehProses: 0, rehSelesai: 0,
                },
                trendData:  [],
                konJenis:   [],
                jadwalKon:  [],
                jadwalReh:  [],
            },
            // ── Satreskrim ─────────────────────────────────────────────
            satreskrim: {
                loading: false,
                kpi: { total: 0, diterima: 0, aktif: 0, selesai: 0 },
                trendData:    [],
                jenisPerkara: [],
                terbaru:      [],
            },
        });

        this.mapState = useState({
            drillLevel:  'kecamatan',
            activeKecId: null,
            kecName:     '',
        });

        this.trendChartRef    = useRef("trendChart");
        this.statusChartRef   = useRef("statusChart");
        this.calendarChartRef = useRef("calendarChart");
        this.dashMapRef       = useRef("dashMap");
        // Satnarkoba chart refs
        this.skTrendRef = useRef("skTrendChart");
        this.skJenisRef = useRef("skJenisChart");
        // Satreskrim chart refs
        this.srTrendRef = useRef("srTrendChart");
        this.srJenisRef = useRef("srJenisChart");

        this._trendChart     = null;
        this._statusChart    = null;
        this._calendarChart  = null;
        this._leafMap        = null;
        this._kecLayer       = null;
        this._desaLayer      = null;
        this._lakaLayer      = null;
        this._mapInitialized = false;
        // Satnarkoba chart instances
        this._skTrendChart   = null;
        this._skJenisChart   = null;
        // Satreskrim chart instances
        this._srTrendChart   = null;
        this._srJenisChart   = null;

        onMounted(async () => await this.loadData());

        useEffect(
            () => {
                if (!this.state.loading) {
                    if (!this._mapInitialized) {
                        this._mapInitialized = true;
                        this._initDashMap();
                    } else {
                        this._updateLakaMarkers();
                    }
                }
            },
            () => [this.state.loading]
        );

        this._legendControl = null;

        onWillDestroy(() => {
            this._trendChart?.dispose();
            this._statusChart?.dispose();
            this._calendarChart?.dispose();
            this._skTrendChart?.dispose();
            this._skJenisChart?.dispose();
            this._srTrendChart?.dispose();
            this._srJenisChart?.dispose();
            if (this._leafMap) { this._leafMap.remove(); this._leafMap = null; }
        });
    }

    // ── Helpers ─────────────────────────────────────────────────────────────────

    _dateStr(d) {
        return `${d.getFullYear()}-${String(d.getMonth()+1).padStart(2,'0')}-${String(d.getDate()).padStart(2,'0')}`;
    }

    _dt(d) {
        const p = n => String(n).padStart(2, '0');
        return `${d.getFullYear()}-${p(d.getMonth()+1)}-${p(d.getDate())} ` +
               `${p(d.getHours())}:${p(d.getMinutes())}:${p(d.getSeconds())}`;
    }

    _lakaDomain() {
        const now = new Date();
        const p   = this.state.period;
        if (p === 'this_month') {
            return [['tanggal_kejadian', '>=', this._dt(new Date(now.getFullYear(), now.getMonth(), 1))]];
        }
        if (p === 'last_month') {
            const from = new Date(now.getFullYear(), now.getMonth() - 1, 1);
            const to   = new Date(now.getFullYear(), now.getMonth(), 0, 23, 59, 59);
            return [['tanggal_kejadian', '>=', this._dt(from)],
                    ['tanggal_kejadian', '<=', this._dt(to)]];
        }
        if (p === 'this_year') {
            return [['tanggal_kejadian', '>=', this._dt(new Date(now.getFullYear(), 0, 1))]];
        }
        return [];
    }

    periodLabel() { return PERIOD_LABEL[this.state.period] || ''; }

    stateLabel(s) { return ANTR_STATE_LABEL[s] || s; }

    fmtTgl(s) {
        if (!s) return '-';
        // Date field: 'YYYY-MM-DD' — no timezone conversion needed
        if (s.length === 10) {
            const [y, m, d] = s.split('-');
            return `${parseInt(d)} ${BULAN[parseInt(m)-1]} ${y}`;
        }
        // Datetime field: 'YYYY-MM-DD HH:MM:SS'
        const d = new Date(s.replace(' ', 'T') + 'Z');
        if (isNaN(d)) return s;
        return `${d.getDate()} ${BULAN[d.getMonth()]} ${d.getFullYear()}`;
    }

    // ── Load data ──────────────────────────────────────────────────────────────

    async loadData() {
        this.state.loading = true;

        const now        = new Date();
        const todayStr   = this._dateStr(now);
        const lakaDom    = this._lakaDomain();
        const domToday   = [['tanggal_booking', '=', todayStr]];

        const monthStart    = new Date(now.getFullYear(), now.getMonth(), 1);
        const monthStartStr = this._dateStr(monthStart);

        const sixMonthsAgo = new Date();
        sixMonthsAgo.setMonth(sixMonthsAgo.getMonth() - 5);
        sixMonthsAgo.setDate(1);

        this.state.todayLabel =
            `${now.getDate()} ${BULAN[now.getMonth()]} ${now.getFullYear()}`;

        const [
            antrTotal, antrMenunggu, antrAktif, antrSelesai,
            lakaTotal, lakaBaru, lakaDisproses, lakaSelesai,
            activeAntrian,
            lakaPending,
            trendRaw,
            layanRaw,
            lakaPoints,
            calendarRaw,
        ] = await Promise.all([
            // ── Antrian KPI (hari ini) ────────────────────────────────
            this.orm.searchCount('digital_kamtibmas.antrian',
                [...domToday, ['state', '!=', 'batal']]),
            this.orm.searchCount('digital_kamtibmas.antrian',
                [...domToday, ['state', '=', 'menunggu']]),
            this.orm.searchCount('digital_kamtibmas.antrian',
                [...domToday, ['state', 'in', ['konfirmasi', 'dipanggil']]]),
            this.orm.searchCount('digital_kamtibmas.antrian',
                [...domToday, ['state', '=', 'selesai']]),

            // ── Laka KPI (per periode) ────────────────────────────────
            this.orm.searchCount('digital_kamtibmas.eform_laka', [...lakaDom]),
            this.orm.searchCount('digital_kamtibmas.eform_laka',
                [['state', '=', 'BARU'],     ...lakaDom]),
            this.orm.searchCount('digital_kamtibmas.eform_laka',
                [['state', '=', 'DIPROSES'], ...lakaDom]),
            this.orm.searchCount('digital_kamtibmas.eform_laka',
                [['state', '=', 'SELESAI'],  ...lakaDom]),

            // ── Antrian aktif hari ini (konfirmasi + dipanggil) ───────
            this.orm.searchRead(
                'digital_kamtibmas.antrian',
                [...domToday, ['state', 'in', ['konfirmasi', 'dipanggil']]],
                ['nomor_antrian', 'atas_nama', 'layanan_id', 'state'],
                { order: 'nomor_urut asc', limit: 20 }
            ),

            // ── Laka perlu tindakan (BARU + DIPROSES) ─────────────────
            this.orm.searchRead(
                'digital_kamtibmas.eform_laka',
                [['state', 'in', ['BARU', 'DIPROSES']]],
                ['code', 'kejadian', 'tanggal_kejadian', 'state'],
                { order: 'tanggal_kejadian desc', limit: 10 }
            ),

            // ── Trend laka 6 bulan ────────────────────────────────────
            this.orm.searchRead(
                'digital_kamtibmas.eform_laka',
                [['tanggal_kejadian', '>=', this._dt(sixMonthsAgo)]],
                ['tanggal_kejadian'],
                { limit: 5000 }
            ),

            // ── Antrian per jenis layanan (bulan ini) ─────────────────
            this.orm.searchRead(
                'digital_kamtibmas.antrian',
                [['tanggal_booking', '>=', monthStartStr], ['state', '!=', 'batal']],
                ['layanan_id'],
                { limit: 5000 }
            ),

            // ── Laka points untuk peta ────────────────────────────────
            this.orm.searchRead(
                'digital_kamtibmas.eform_laka',
                [['lat', '!=', 0], ['lng', '!=', 0]],
                ['id', 'code', 'kejadian', 'tanggal_kejadian', 'state', 'lat', 'lng'],
                { limit: 500 }
            ),

            // ── Antrian per hari (tahun ini) untuk kalender ───────────
            this.orm.searchRead(
                'digital_kamtibmas.antrian',
                [['tanggal_booking', '>=', `${now.getFullYear()}-01-01`],
                 ['state', '!=', 'batal']],
                ['tanggal_booking'],
                { limit: 50000 }
            ),
        ]);

        this.state.kpi = {
            antrTotal, antrMenunggu, antrAktif, antrSelesai,
            lakaTotal, lakaBaru, lakaDisproses, lakaSelesai,
        };
        this.state.activeAntrian = activeAntrian;
        this.state.lakaPending   = lakaPending;
        this.state.trendData     = this._buildTrendLaka(trendRaw);
        this.state.layanData     = this._buildLayanan(layanRaw);
        this.state.calendarData  = this._buildCalendarData(calendarRaw);
        this.state.calendarYear  = now.getFullYear();
        this.state.lakaPoints    = lakaPoints;
        this.state.loading       = false;

        setTimeout(() => this._renderCharts(), 60);
    }

    _buildTrendLaka(records) {
        const now    = new Date();
        const months = [];
        for (let i = 5; i >= 0; i--) {
            const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
            months.push({
                year: d.getFullYear(), month: d.getMonth() + 1,
                label: `${BULAN[d.getMonth()]} ${d.getFullYear()}`,
            });
        }
        const map = {};
        for (const r of records) {
            if (!r.tanggal_kejadian) continue;
            const d   = new Date(r.tanggal_kejadian.replace(' ', 'T') + 'Z');
            const key = `${d.getFullYear()}-${d.getMonth()+1}`;
            map[key]  = (map[key] || 0) + 1;
        }
        return months.map(m => ({
            label: m.label,
            count: map[`${m.year}-${m.month}`] || 0,
        }));
    }

    _buildCalendarData(records) {
        const map = {};
        for (const r of records) {
            if (!r.tanggal_booking) continue;
            map[r.tanggal_booking] = (map[r.tanggal_booking] || 0) + 1;
        }
        return Object.entries(map).map(([date, count]) => [date, count]);
    }

    _buildLayanan(records) {
        const map = {};
        for (const r of records) {
            const name = r.layanan_id ? r.layanan_id[1] : 'Lainnya';
            map[name]  = (map[name] || 0) + 1;
        }
        return Object.entries(map)
            .map(([name, count]) => ({ name, count }))
            .sort((a, b) => b.count - a.count);
    }

    // ── Charts ─────────────────────────────────────────────────────────────────

    _renderCharts() {
        if (typeof echarts === 'undefined') return;
        this._renderTrend();
        this._renderLayanan();
        this._renderCalendar();
    }

    _renderCalendar() {
        const el = this.calendarChartRef?.el;
        if (!el) return;
        if (this._calendarChart) this._calendarChart.dispose();
        this._calendarChart = echarts.init(el);

        const year = this.state.calendarYear;
        const data = this.state.calendarData;
        const maxVal = data.length ? Math.max(...data.map(d => d[1])) : 5;

        this._calendarChart.setOption({
            tooltip: {
                formatter: p => {
                    if (!p.data) return '';
                    const [date, count] = p.data;
                    return `<b>${date}</b><br/>${count} antrian`;
                },
            },
            visualMap: {
                show: false,
                min: 0,
                max: maxVal || 5,
                inRange: {
                    color: ['#ebedf0', '#c6e48b', '#7bc96f', '#239a3b', '#196127'],
                },
            },
            calendar: [{
                range: String(year),
                left:  70,
                right: 20,
                top:   30,
                bottom: 10,
                cellSize: ['auto', 14],
                splitLine: { show: false },
                yearLabel: { show: false },
                monthLabel: {
                    nameMap: ['Jan','Feb','Mar','Apr','Mei','Jun',
                              'Jul','Agu','Sep','Okt','Nov','Des'],
                    fontSize: 11,
                    color: '#6b7280',
                },
                dayLabel: {
                    firstDay: 1,
                    nameMap: ['Min','Sen','Sel','Rab','Kam','Jum','Sab'],
                    fontSize: 11,
                    color: '#6b7280',
                },
                itemStyle: {
                    borderColor: '#fff',
                    borderWidth: 3,
                    color: '#ebedf0',
                },
            }],
            series: [{
                type: 'heatmap',
                coordinateSystem: 'calendar',
                calendarIndex: 0,
                data: data,
            }],
        });
    }

    _renderTrend() {
        const el = this.trendChartRef?.el;
        if (!el) return;
        if (this._trendChart) this._trendChart.dispose();
        this._trendChart = echarts.init(el);
        this._trendChart.setOption({
            tooltip: {
                trigger: 'axis',
                backgroundColor: '#fff', borderColor: '#e5e7eb', borderWidth: 1,
                textStyle: { color: '#374151', fontSize: 12 },
                formatter: p => `${p[0].name}<br/><b>Laka: ${p[0].value}</b>`,
            },
            grid: { left: 10, right: 16, top: 16, bottom: 55, containLabel: true },
            xAxis: {
                type: 'category', data: this.state.trendData.map(d => d.label),
                axisLabel: { rotate: 30, fontSize: 11, color: '#6b7280' },
                axisLine: { lineStyle: { color: '#e5e7eb' } }, axisTick: { show: false },
            },
            yAxis: {
                type: 'value', minInterval: 1,
                axisLabel: { fontSize: 11, color: '#9ca3af' },
                splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } },
            },
            series: [{
                type: 'line', data: this.state.trendData.map(d => d.count),
                smooth: true, symbol: 'circle', symbolSize: 7,
                lineStyle: { color: '#7c3aed', width: 2.5 },
                itemStyle: { color: '#7c3aed', borderColor: '#fff', borderWidth: 2 },
                areaStyle: {
                    color: {
                        type: 'linear', x: 0, y: 0, x2: 0, y2: 1,
                        colorStops: [
                            { offset: 0, color: 'rgba(124,58,237,0.22)' },
                            { offset: 1, color: 'rgba(124,58,237,0.02)' },
                        ],
                    },
                },
            }],
        });
    }

    _renderLayanan() {
        const el = this.statusChartRef?.el;
        if (!el) return;
        if (this._statusChart) this._statusChart.dispose();
        this._statusChart = echarts.init(el);

        const data = this.state.layanData;
        if (!data.length) {
            this._statusChart.setOption({
                graphic: [{
                    type: 'text', left: 'center', top: 'middle',
                    style: { text: 'Belum ada antrian bulan ini', fill: '#9ca3af', fontSize: 13 },
                }],
            });
            return;
        }

        const COLORS = ['#71639e', '#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6'];
        this._statusChart.setOption({
            tooltip: { trigger: 'item', formatter: '{b}: {c} ({d}%)' },
            legend: { bottom: 4, textStyle: { fontSize: 11, color: '#6b7280' } },
            series: [{
                type: 'pie', radius: ['40%', '66%'], center: ['50%', '44%'],
                label: { show: false }, labelLine: { show: false },
                data: data.map((d, i) => ({
                    value: d.count, name: d.name,
                    itemStyle: { color: COLORS[i % COLORS.length] },
                })),
            }],
        });
    }

    // ── Choropleth helpers ─────────────────────────────────────────────────────

    _choroplethColor(count) {
        if (!count) return '#dceefb';
        if (count <= 5)  return '#fee08b';
        if (count <= 10) return '#fdae61';
        if (count <= 20) return '#f46d43';
        if (count <= 50) return '#d73027';
        return '#7f0000';
    }

    _extractPolygons(geometry) {
        if (geometry.type === 'Polygon')      return [geometry.coordinates[0]];
        if (geometry.type === 'MultiPolygon') return geometry.coordinates.map(p => p[0]);
        return [];
    }

    _pointInPolygon(lat, lng, ring) {
        // ring: [[lng, lat], ...] (GeoJSON order)
        let inside = false;
        for (let i = 0, j = ring.length - 1; i < ring.length; j = i++) {
            const [xi, yi] = ring[i];   // xi = lng, yi = lat
            const [xj, yj] = ring[j];
            const cross = ((yi > lat) !== (yj > lat)) &&
                (lng < (xj - xi) * (lat - yi) / (yj - yi) + xi);
            if (cross) inside = !inside;
        }
        return inside;
    }

    _buildLakaCountByKec(features) {
        const counts = {};
        for (const feat of features) {
            const id = feat.properties.id;
            counts[id] = 0;
            const rings = this._extractPolygons(feat.geometry);
            for (const p of (this.state.lakaPoints || [])) {
                if (!p.lat || !p.lng) continue;
                for (const ring of rings) {
                    if (this._pointInPolygon(p.lat, p.lng, ring)) {
                        counts[id]++;
                        break;
                    }
                }
            }
        }
        return counts;
    }

    _addMapLegend() {
        if (!this._leafMap) return;
        if (this._legendControl) {
            this._leafMap.removeControl(this._legendControl);
            this._legendControl = null;
        }
        const self = this;
        const legend = L.control({ position: 'bottomright' });
        legend.onAdd = function () {
            const div = L.DomUtil.create('div', 'dkm-choropleth-legend');
            div.innerHTML =
                '<div class="dkm-cleg-title"><i class="fa fa-map"></i> Sebaran Laka</div>' +
                '<div class="dkm-cleg-row"><span class="dkm-cleg-box" style="background:#7f0000"></span>&gt; 50 Kasus</div>' +
                '<div class="dkm-cleg-row"><span class="dkm-cleg-box" style="background:#d73027"></span>21 – 50 Kasus</div>' +
                '<div class="dkm-cleg-row"><span class="dkm-cleg-box" style="background:#f46d43"></span>11 – 20 Kasus</div>' +
                '<div class="dkm-cleg-row"><span class="dkm-cleg-box" style="background:#fdae61"></span>6 – 10 Kasus</div>' +
                '<div class="dkm-cleg-row"><span class="dkm-cleg-box" style="background:#fee08b"></span>1 – 5 Kasus</div>' +
                '<div class="dkm-cleg-row"><span class="dkm-cleg-box" style="background:#dceefb;border:1px solid #bcd"></span>Tidak Ada</div>';
            return div;
        };
        legend.addTo(this._leafMap);
        this._legendControl = legend;
    }

    // ── Dashboard Map ──────────────────────────────────────────────────────────

    _initDashMap() {
        const el = this.dashMapRef?.el;
        if (!el || typeof L === 'undefined') return;

        this._leafMap = L.map(el, { zoomControl: true }).setView(PALEMBANG_CENTER, 11);
        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            attribution: '© <a href="https://www.openstreetmap.org">OpenStreetMap</a>',
            maxZoom: 19,
        }).addTo(this._leafMap);

        setTimeout(() => this._leafMap && this._leafMap.invalidateSize(), 200);
        this._loadKecamatanLayer();
    }

    async _loadKecamatanLayer() {
        if (!this._leafMap) return;

        const kecList = await this.orm.searchRead(
            'digital_kamtibmas.kecamatan',
            [['geometry', '!=', false]],
            ['id', 'name', 'geometry'],
            { order: 'name asc', limit: 200 }
        );

        if (this._kecLayer) { this._kecLayer.remove(); this._kecLayer = null; }

        const features = this._toFeatures(kecList);
        if (!features.length) return;

        // Count laka per kecamatan via point-in-polygon
        const lakaCount = this._buildLakaCountByKec(features);

        this._kecLayer = L.geoJSON({ type: 'FeatureCollection', features }, {
            style: (feat) => {
                const count = lakaCount[feat.properties.id] || 0;
                const fill  = this._choroplethColor(count);
                return {
                    color: '#4b5563', weight: 1,
                    fillColor: fill,
                    fillOpacity: count > 0 ? 0.75 : 0.35,
                };
            },
            onEachFeature: (feat, layer) => {
                const count = lakaCount[feat.properties.id] || 0;
                const tip   = `<b>${feat.properties.name}</b><br/>${count} kasus laka`;
                layer.bindTooltip(tip, { sticky: true });
                layer.on('click', () =>
                    this._drillToKecamatan(feat.properties.id, feat.properties.name)
                );
                layer.on('mouseover', e => {
                    const orig = lakaCount[feat.properties.id] || 0;
                    e.target.setStyle({ weight: 2.5, fillOpacity: Math.min((orig > 0 ? 0.75 : 0.35) + 0.2, 1) });
                });
                layer.on('mouseout', e => this._kecLayer.resetStyle(e.target));
            },
        }).addTo(this._leafMap);

        this._leafMap.fitBounds(this._kecLayer.getBounds(), { padding: [20, 20] });
        this._updateLakaMarkers();
        this._addMapLegend();
    }

    async _drillToKecamatan(kecId, kecName) {
        if (!this._leafMap) return;

        const desaList = await this.orm.searchRead(
            'digital_kamtibmas.desa',
            [['kecamatan_id', '=', kecId], ['geometry', '!=', false]],
            ['id', 'name', 'type', 'geometry'],
            { order: 'name asc', limit: 300 }
        );

        if (this._kecLayer)  this._kecLayer.remove();
        if (this._desaLayer) { this._desaLayer.remove(); this._desaLayer = null; }
        if (this._lakaLayer) { this._lakaLayer.remove(); this._lakaLayer = null; }

        const features = this._toFeatures(desaList, d => ({
            id: d.id, name: d.name, tipe: d.type,
        }));

        if (features.length) {
            // Count laka per desa via point-in-polygon
            const lakaCount = this._buildLakaCountByKec(features);

            this._desaLayer = L.geoJSON({ type: 'FeatureCollection', features }, {
                style: (feat) => {
                    const count = lakaCount[feat.properties.id] || 0;
                    const fill  = this._choroplethColor(count);
                    return {
                        color: '#4b5563', weight: 1,
                        fillColor: fill,
                        fillOpacity: count > 0 ? 0.75 : 0.35,
                    };
                },
                onEachFeature: (feat, layer) => {
                    const count = lakaCount[feat.properties.id] || 0;
                    const tipe  = feat.properties.tipe ? ` (${feat.properties.tipe})` : '';
                    const tip   = `<b>${feat.properties.name}</b>${tipe}<br/>${count} kasus laka`;
                    layer.bindTooltip(tip, { sticky: true });
                    layer.on('mouseover', e => {
                        const orig = lakaCount[feat.properties.id] || 0;
                        e.target.setStyle({ weight: 2.5, fillOpacity: Math.min((orig > 0 ? 0.75 : 0.35) + 0.2, 1) });
                    });
                    layer.on('mouseout', e => this._desaLayer.resetStyle(e.target));
                },
            }).addTo(this._leafMap);

            this._leafMap.fitBounds(this._desaLayer.getBounds(), { padding: [20, 20] });
        }

        this.mapState.drillLevel  = 'desa';
        this.mapState.activeKecId = kecId;
        this.mapState.kecName     = kecName;

        this._updateLakaMarkers();
    }

    resetMapToKecamatan() {
        if (!this._leafMap) return;
        if (this._desaLayer) { this._desaLayer.remove(); this._desaLayer = null; }
        if (this._lakaLayer) { this._lakaLayer.remove(); this._lakaLayer = null; }
        if (this._kecLayer)  {
            this._kecLayer.addTo(this._leafMap);
            this._leafMap.fitBounds(this._kecLayer.getBounds(), { padding: [20, 20] });
        }
        this.mapState.drillLevel  = 'kecamatan';
        this.mapState.activeKecId = null;
        this.mapState.kecName     = '';
        this._updateLakaMarkers();
    }

    _updateLakaMarkers() {
        if (!this._leafMap) return;
        if (this._lakaLayer) { this._lakaLayer.remove(); this._lakaLayer = null; }

        const COLOR = { BARU: '#3b82f6', DIPROSES: '#f59e0b', SELESAI: '#10b981' };
        const markers = (this.state.lakaPoints || [])
            .filter(p => p.lat && p.lng)
            .map(p => {
                const c   = COLOR[p.state] || '#6b7280';
                const tgl = p.tanggal_kejadian ? this.fmtTgl(p.tanggal_kejadian) : '-';
                const popup = `
<div class="dkm-laka-popup">
    <div class="dkm-laka-popup-header">
        <i class="fa fa-car"></i> ${p.code}
    </div>
    <div class="dkm-laka-popup-body">
        <div class="dkm-laka-popup-row">
            <span class="dkm-laka-popup-lbl">Kejadian</span>
            <span class="dkm-laka-popup-val">${p.kejadian || '-'}</span>
        </div>
        <div class="dkm-laka-popup-row">
            <span class="dkm-laka-popup-lbl">Tanggal</span>
            <span class="dkm-laka-popup-val">${tgl}</span>
        </div>
        <div class="dkm-laka-popup-row">
            <span class="dkm-laka-popup-lbl">Status</span>
            <span class="dkm-laka-popup-val" style="color:${c};font-weight:700">${p.state}</span>
        </div>
    </div>
    <button class="dkm-laka-popup-detail-btn">
        <i class="fa fa-external-link"></i> Lihat Detail
    </button>
</div>`;
                const marker = L.circleMarker([p.lat, p.lng], {
                    radius: 7, color: '#fff', weight: 2,
                    fillColor: c, fillOpacity: 0.92,
                }).bindPopup(popup, { maxWidth: 260 });

                marker.on('popupopen', (ev) => {
                    const btn = ev.popup.getElement()
                        ?.querySelector('.dkm-laka-popup-detail-btn');
                    if (btn) btn.onclick = () => this.openLakaRecord(p.id);
                });

                return marker;
            });

        if (markers.length) {
            this._lakaLayer = L.layerGroup(markers).addTo(this._leafMap);
        }
    }

    _toFeatures(list, propsMapper) {
        const out = [];
        for (const item of list) {
            if (!item.geometry) continue;
            try {
                const geo = typeof item.geometry === 'string'
                    ? JSON.parse(item.geometry) : item.geometry;
                out.push({
                    type: 'Feature',
                    properties: propsMapper
                        ? propsMapper(item)
                        : { id: item.id, name: item.name },
                    geometry: geo,
                });
            } catch (e) { /* skip */ }
        }
        return out;
    }

    // ── Satnarkoba Dashboard ───────────────────────────────────────────────────

    async loadSatnarkoba() {
        this.state.satkoba.loading = true;

        const now        = new Date();
        const sixAgo     = new Date(now.getFullYear(), now.getMonth() - 5, 1);
        const sixAgoStr  = this._dateStr(sixAgo);

        const [
            konTotal, konMenunggu, konProses, konSelesai,
            rehTotal, rehMenunggu, rehProses, rehSelesai,
            konTrendRaw, rehTrendRaw, konJenisRaw,
            jadwalKon, jadwalReh,
        ] = await Promise.all([
            this.orm.searchCount('digital_kamtibmas.konseling', []),
            this.orm.searchCount('digital_kamtibmas.konseling', [['state','=','menunggu']]),
            this.orm.searchCount('digital_kamtibmas.konseling', [['state','in',['konfirmasi','proses']]]),
            this.orm.searchCount('digital_kamtibmas.konseling', [['state','=','selesai']]),

            this.orm.searchCount('digital_kamtibmas.rehab', []),
            this.orm.searchCount('digital_kamtibmas.rehab', [['state','=','menunggu']]),
            this.orm.searchCount('digital_kamtibmas.rehab', [['state','in',['konfirmasi','proses']]]),
            this.orm.searchCount('digital_kamtibmas.rehab', [['state','=','selesai']]),

            this.orm.searchRead('digital_kamtibmas.konseling',
                [['tanggal_pengajuan','>=', sixAgoStr]],
                ['tanggal_pengajuan'], { limit: 5000 }),

            this.orm.searchRead('digital_kamtibmas.rehab',
                [['tanggal_pengajuan','>=', sixAgoStr]],
                ['tanggal_pengajuan'], { limit: 5000 }),

            this.orm.searchRead('digital_kamtibmas.konseling',
                [], ['jenis_masalah'], { limit: 5000 }),

            this.orm.searchRead('digital_kamtibmas.konseling',
                [['tanggal_jadwal','!=',false], ['state','!=','selesai']],
                ['code','nama','tanggal_jadwal','jenis_masalah','state'],
                { order: 'tanggal_jadwal asc', limit: 10 }),

            this.orm.searchRead('digital_kamtibmas.rehab',
                [['tanggal_jadwal','!=',false], ['state','!=','selesai']],
                ['code','nama','tanggal_jadwal','state'],
                { order: 'tanggal_jadwal asc', limit: 10 }),
        ]);

        this.state.satkoba.kpi = {
            konTotal, konMenunggu, konProses, konSelesai,
            rehTotal, rehMenunggu, rehProses, rehSelesai,
        };
        this.state.satkoba.trendData = this._buildSatkobaTrend(konTrendRaw, rehTrendRaw);
        this.state.satkoba.konJenis  = this._buildSelectionCount(konJenisRaw, 'jenis_masalah', {
            penyalahgunaan: 'Penyalahgunaan',
            ketergantungan: 'Ketergantungan',
            pencegahan:     'Pencegahan',
            pasca_rehab:    'Pasca Rehab',
            konsultasi:     'Konsultasi',
            lainnya:        'Lainnya',
        });
        this.state.satkoba.jadwalKon = jadwalKon;
        this.state.satkoba.jadwalReh = jadwalReh;
        this.state.satkoba.loading   = false;

        setTimeout(() => this._renderSatnarkobaCharts(), 60);
    }

    _buildSatkobaTrend(konRaw, rehRaw) {
        const now    = new Date();
        const months = [];
        for (let i = 5; i >= 0; i--) {
            const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
            months.push({ year: d.getFullYear(), month: d.getMonth() + 1,
                          label: `${BULAN[d.getMonth()]} ${d.getFullYear()}` });
        }
        const buildMap = (raw) => {
            const m = {};
            for (const r of raw) {
                if (!r.tanggal_pengajuan) continue;
                const [y, mo] = r.tanggal_pengajuan.split('-');
                const k = `${y}-${parseInt(mo)}`;
                m[k] = (m[k] || 0) + 1;
            }
            return m;
        };
        const konMap = buildMap(konRaw);
        const rehMap = buildMap(rehRaw);
        return months.map(m => ({
            label: m.label,
            kon:   konMap[`${m.year}-${m.month}`] || 0,
            reh:   rehMap[`${m.year}-${m.month}`] || 0,
        }));
    }

    _buildSelectionCount(raw, field, labelMap) {
        const map = {};
        for (const r of raw) {
            const v = r[field] || 'lainnya';
            map[v] = (map[v] || 0) + 1;
        }
        return Object.entries(map).map(([k, count]) => ({
            name: labelMap[k] || k, count,
        })).sort((a, b) => b.count - a.count);
    }

    _renderSatnarkobaCharts() {
        if (typeof echarts === 'undefined') return;
        this._renderSkTrend();
        this._renderSkJenis();
    }

    _renderSkTrend() {
        const el = this.skTrendRef?.el;
        if (!el) return;
        this._skTrendChart?.dispose();
        this._skTrendChart = echarts.init(el);
        const data = this.state.satkoba.trendData;
        this._skTrendChart.setOption({
            tooltip: { trigger: 'axis',
                formatter: p => `${p[0].name}<br/>`+
                    `<b>Konseling: ${p[0].value}</b><br/>`+
                    `<b>Rehab: ${p[1]?.value ?? 0}</b>` },
            legend: { bottom: 4, textStyle: { fontSize: 11, color: '#6b7280' } },
            grid: { left: 10, right: 16, top: 20, bottom: 48, containLabel: true },
            xAxis: { type: 'category', data: data.map(d => d.label),
                axisLabel: { rotate: 30, fontSize: 11, color: '#6b7280' },
                axisLine: { lineStyle: { color: '#e5e7eb' } }, axisTick: { show: false } },
            yAxis: { type: 'value', minInterval: 1,
                axisLabel: { fontSize: 11, color: '#9ca3af' },
                splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } } },
            series: [
                { name: 'Konseling', type: 'line', data: data.map(d => d.kon),
                  smooth: true, symbol: 'circle', symbolSize: 7,
                  lineStyle: { color: '#71639e', width: 2.5 },
                  itemStyle: { color: '#71639e', borderColor: '#fff', borderWidth: 2 },
                  areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,
                    colorStops:[{offset:0,color:'rgba(113,99,158,0.2)'},{offset:1,color:'rgba(113,99,158,0.02)'}] } } },
                { name: 'Rehab', type: 'line', data: data.map(d => d.reh),
                  smooth: true, symbol: 'circle', symbolSize: 7,
                  lineStyle: { color: '#10b981', width: 2.5 },
                  itemStyle: { color: '#10b981', borderColor: '#fff', borderWidth: 2 },
                  areaStyle: { color: { type:'linear',x:0,y:0,x2:0,y2:1,
                    colorStops:[{offset:0,color:'rgba(16,185,129,0.18)'},{offset:1,color:'rgba(16,185,129,0.02)'}] } } },
            ],
        });
    }

    _renderSkJenis() {
        const el = this.skJenisRef?.el;
        if (!el) return;
        this._skJenisChart?.dispose();
        this._skJenisChart = echarts.init(el);
        const data = this.state.satkoba.konJenis;
        if (!data.length) {
            this._skJenisChart.setOption({ graphic: [{ type:'text', left:'center', top:'middle',
                style:{ text:'Belum ada data konseling', fill:'#9ca3af', fontSize:13 } }] });
            return;
        }
        const COLORS = ['#71639e','#10b981','#f59e0b','#3b82f6','#ef4444','#8b5cf6'];
        this._skJenisChart.setOption({
            tooltip: { trigger:'item', formatter:'{b}: {c} ({d}%)' },
            legend: { bottom: 4, textStyle: { fontSize: 11, color: '#6b7280' } },
            series: [{ type:'pie', radius:['40%','66%'], center:['50%','44%'],
                label:{ show:false }, labelLine:{ show:false },
                data: data.map((d,i) => ({ value:d.count, name:d.name,
                    itemStyle:{ color: COLORS[i % COLORS.length] } })) }],
        });
    }

    // ── Satnarkoba navigation ──────────────────────────────────────────────────

    openKonselingList(extraDomain) {
        this.action.doAction({ type:'ir.actions.act_window', name:'Konseling Online',
            res_model:'digital_kamtibmas.konseling', view_mode:'list,form',
            domain: extraDomain || [] });
    }

    openKonselingRecord(id) {
        this.action.doAction({ type:'ir.actions.act_window',
            res_model:'digital_kamtibmas.konseling', res_id: id,
            views: [[false,'form']] });
    }

    openRehabList(extraDomain) {
        this.action.doAction({ type:'ir.actions.act_window', name:'Permohonan Rehabilitasi',
            res_model:'digital_kamtibmas.rehab', view_mode:'list,form',
            domain: extraDomain || [] });
    }

    openRehabRecord(id) {
        this.action.doAction({ type:'ir.actions.act_window',
            res_model:'digital_kamtibmas.rehab', res_id: id,
            views: [[false,'form']] });
    }

    skStateLabel(s) {
        return { menunggu:'Menunggu', konfirmasi:'Dikonfirmasi',
                 proses:'Diproses', selesai:'Selesai' }[s] || s;
    }

    skJenisMasalah(key) {
        return { penyalahgunaan:'Penyalahgunaan', ketergantungan:'Ketergantungan',
                 pencegahan:'Pencegahan', pasca_rehab:'Pasca Rehab',
                 konsultasi:'Konsultasi', lainnya:'Lainnya' }[key] || '-';
    }

    skFormatJadwal(dt) {
        if (!dt) return '-';
        return String(dt).replace('T', ' ').slice(0, 16);
    }

    // ── Satreskrim Dashboard ──────────────────────────────────────────────────

    async loadSatreskrim() {
        this.state.satreskrim.loading = true;

        const now       = new Date();
        const sixAgo    = new Date(now.getFullYear(), now.getMonth() - 5, 1);
        const sixAgoStr = this._dateStr(sixAgo);

        const [
            total, diterima, aktif, selesai,
            trendRaw, jenisRaw, terbaru,
        ] = await Promise.all([
            this.orm.searchCount('digital_kamtibmas.barang_bukti', []),
            this.orm.searchCount('digital_kamtibmas.barang_bukti', [['state','=','diterima']]),
            this.orm.searchCount('digital_kamtibmas.barang_bukti',
                [['state','in',['disimpan','diproses']]]),
            this.orm.searchCount('digital_kamtibmas.barang_bukti',
                [['state','in',['dikembalikan','dimusnahkan']]]),

            this.orm.searchRead('digital_kamtibmas.barang_bukti',
                [['tanggal_penerimaan','>=', sixAgoStr]],
                ['tanggal_penerimaan'], { limit: 5000 }),

            this.orm.searchRead('digital_kamtibmas.barang_bukti',
                [], ['jenis_perkara'], { limit: 5000 }),

            this.orm.searchRead('digital_kamtibmas.barang_bukti',
                [],
                ['code','nama_pelapor','jenis_perkara','tanggal_penerimaan','state'],
                { order: 'id desc', limit: 10 }),
        ]);

        this.state.satreskrim.kpi          = { total, diterima, aktif, selesai };
        this.state.satreskrim.trendData    = this._buildTrend6BulanDate(trendRaw, 'tanggal_penerimaan');
        this.state.satreskrim.jenisPerkara = this._buildSelectionCount(jenisRaw, 'jenis_perkara', {
            pencurian:    'Pencurian',
            penipuan:     'Penipuan',
            penganiayaan: 'Penganiayaan',
            narkoba:      'Narkoba',
            korupsi:      'Korupsi',
            cybercrime:   'Cyber Crime',
            pemerkosaan:  'Kesusilaan',
            pembunuhan:   'Pembunuhan',
            lainnya:      'Lainnya',
        });
        this.state.satreskrim.terbaru      = terbaru;
        this.state.satreskrim.loading      = false;

        setTimeout(() => this._renderSatreskrimCharts(), 60);
    }

    _buildTrend6BulanDate(raw, dateField) {
        const now    = new Date();
        const months = [];
        for (let i = 5; i >= 0; i--) {
            const d = new Date(now.getFullYear(), now.getMonth() - i, 1);
            months.push({ year: d.getFullYear(), month: d.getMonth() + 1,
                          label: `${BULAN[d.getMonth()]} ${d.getFullYear()}` });
        }
        const map = {};
        for (const r of raw) {
            if (!r[dateField]) continue;
            const [y, mo] = r[dateField].split('-');
            const k = `${y}-${parseInt(mo)}`;
            map[k] = (map[k] || 0) + 1;
        }
        return months.map(m => ({
            label: m.label,
            count: map[`${m.year}-${m.month}`] || 0,
        }));
    }

    _renderSatreskrimCharts() {
        if (typeof echarts === 'undefined') return;
        this._renderSrTrend();
        this._renderSrJenis();
    }

    _renderSrTrend() {
        const el = this.srTrendRef?.el;
        if (!el) return;
        this._srTrendChart?.dispose();
        this._srTrendChart = echarts.init(el);
        const data = this.state.satreskrim.trendData;
        this._srTrendChart.setOption({
            tooltip: { trigger: 'axis',
                formatter: p => `${p[0].name}<br/><b>Barang Bukti: ${p[0].value}</b>` },
            grid: { left: 10, right: 16, top: 20, bottom: 48, containLabel: true },
            xAxis: { type: 'category', data: data.map(d => d.label),
                axisLabel: { rotate: 30, fontSize: 11, color: '#6b7280' },
                axisLine: { lineStyle: { color: '#e5e7eb' } }, axisTick: { show: false } },
            yAxis: { type: 'value', minInterval: 1,
                axisLabel: { fontSize: 11, color: '#9ca3af' },
                splitLine: { lineStyle: { color: '#f3f4f6', type: 'dashed' } } },
            series: [{
                type: 'bar', data: data.map(d => d.count),
                itemStyle: { color: '#71639e', borderRadius: [4, 4, 0, 0] },
                label: { show: true, position: 'top', fontSize: 11, color: '#6b7280',
                    formatter: p => p.value > 0 ? p.value : '' },
            }],
        });
    }

    _renderSrJenis() {
        const el = this.srJenisRef?.el;
        if (!el) return;
        this._srJenisChart?.dispose();
        this._srJenisChart = echarts.init(el);
        const data = this.state.satreskrim.jenisPerkara;
        if (!data.length) {
            this._srJenisChart.setOption({ graphic: [{ type:'text', left:'center', top:'middle',
                style:{ text:'Belum ada data', fill:'#9ca3af', fontSize:13 } }] });
            return;
        }
        const COLORS = ['#71639e','#3b82f6','#f59e0b','#ef4444','#10b981','#8b5cf6','#ec4899','#06b6d4','#84cc16'];
        this._srJenisChart.setOption({
            tooltip: { trigger:'item', formatter:'{b}: {c} ({d}%)' },
            legend: { bottom: 4, textStyle: { fontSize: 11, color: '#6b7280' } },
            series: [{ type:'pie', radius:['40%','66%'], center:['50%','44%'],
                label:{ show:false }, labelLine:{ show:false },
                data: data.map((d,i) => ({ value:d.count, name:d.name,
                    itemStyle:{ color: COLORS[i % COLORS.length] } })) }],
        });
    }

    // ── Satreskrim navigation ──────────────────────────────────────────────────

    openBBList(domain) {
        this.action.doAction({ type:'ir.actions.act_window', name:'Barang Bukti',
            res_model:'digital_kamtibmas.barang_bukti', view_mode:'list,form',
            domain: domain || [] });
    }

    openBBRecord(id) {
        this.action.doAction({ type:'ir.actions.act_window',
            res_model:'digital_kamtibmas.barang_bukti', res_id: id,
            views: [[false,'form']] });
    }

    srStateLabel(s) {
        return { diterima:'Diterima', disimpan:'Disimpan', diproses:'Diproses',
                 dikembalikan:'Dikembalikan', dimusnahkan:'Dimusnahkan' }[s] || s;
    }

    srJenisPerkara(key) {
        return { pencurian:'Pencurian', penipuan:'Penipuan', penganiayaan:'Penganiayaan',
                 narkoba:'Narkoba', korupsi:'Korupsi', cybercrime:'Cyber Crime',
                 pemerkosaan:'Kesusilaan', pembunuhan:'Pembunuhan', lainnya:'Lainnya' }[key] || '-';
    }

    // ── Sidebar navigation ─────────────────────────────────────────────────────

    toggleSidebar() {
        this.state.sidebarCollapsed = !this.state.sidebarCollapsed;
        // Resize map after sidebar transition ends (220ms)
        if (this.state.activeSection === 'satlantas' && this._leafMap) {
            setTimeout(() => this._leafMap && this._leafMap.invalidateSize(), 250);
        }
    }

    setSection(section) {
        const prev = this.state.activeSection;
        if (prev === section) return;

        if (prev === 'satlantas') {
            this._trendChart?.dispose();    this._trendChart    = null;
            this._statusChart?.dispose();   this._statusChart   = null;
            this._calendarChart?.dispose(); this._calendarChart = null;
            if (this._leafMap) { this._leafMap.remove(); this._leafMap = null; }
            this._mapInitialized = false;
        }
        if (prev === 'satnarkoba') {
            this._skTrendChart?.dispose(); this._skTrendChart = null;
            this._skJenisChart?.dispose(); this._skJenisChart = null;
        }
        if (prev === 'satreskrim') {
            this._srTrendChart?.dispose(); this._srTrendChart = null;
            this._srJenisChart?.dispose(); this._srJenisChart = null;
        }

        this.state.activeSection = section;

        if (section === 'satlantas') {
            setTimeout(() => {
                if (!this.state.loading) {
                    this._renderCharts();
                    this._initDashMap();
                }
            }, 100);
        }
        if (section === 'satnarkoba') {
            this.loadSatnarkoba();
        }
        if (section === 'satreskrim') {
            this.loadSatreskrim();
        }
    }

    ucSectionName() {
        const names = {
            satnarkoba: 'Satnarkoba',
            satreskrim: 'Satreskrim',
            sabhara:    'Sabhara',
        };
        return names[this.state.activeSection] || '';
    }

    ucSectionIcon() {
        const icons = {
            satnarkoba: 'fa-medkit',
            satreskrim: 'fa-search',
            sabhara:    'fa-binoculars',
        };
        return icons[this.state.activeSection] || 'fa-shield';
    }

    // ── Event handlers ─────────────────────────────────────────────────────────

    async onPeriodChange(ev) {
        this.state.period = ev.target.value;
        await this.loadData();
    }

    // ── Navigation ─────────────────────────────────────────────────────────────

    openAntrianRecord(id) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'digital_kamtibmas.antrian',
            res_id: id,
            views: [[false, 'form']],
        });
    }

    openAntrianList(extraDomain) {
        const todayStr = this._dateStr(new Date());
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'Antrian Satlantas',
            res_model: 'digital_kamtibmas.antrian',
            view_mode: 'list,form',
            domain: [['tanggal_booking', '=', todayStr], ...(extraDomain || [])],
        });
    }

    openLakaRecord(id) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            res_model: 'digital_kamtibmas.eform_laka',
            res_id: id,
            views: [[false, 'form']],
        });
    }

    openLakaList(extraDomain) {
        this.action.doAction({
            type: 'ir.actions.act_window',
            name: 'e-Form Laka',
            res_model: 'digital_kamtibmas.eform_laka',
            view_mode: 'list,form',
            domain: [...this._lakaDomain(), ...(extraDomain || [])],
        });
    }
}

registry.category("actions").add("digital_kamtibmas.dashboard", DkmDashboard);
