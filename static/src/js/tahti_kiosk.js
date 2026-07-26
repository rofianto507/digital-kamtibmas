/* Buku Tamu Tahti — Kiosk Web App
   OWL 2 standalone, IIFE pattern
   Route: /tahti/buku-tamu  auth=public */
(function () {
    'use strict';

    const { Component, useState, mount, xml, onMounted, onWillUnmount, useRef, onPatched } = owl;

    // ── RPC helper ────────────────────────────────────────────────────────────

    async function rpc(route, params) {
        const res = await fetch(route, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: params || {} }),
        });
        const json = await res.json();
        if (json.error) {
            const msg = (json.error.data && json.error.data.message) || json.error.message || 'Error';
            throw new Error(msg);
        }
        return json.result;
    }

    // ── Date / time ───────────────────────────────────────────────────────────

    const DAYS   = ['Minggu','Senin','Selasa','Rabu','Kamis','Jumat','Sabtu'];
    const MONTHS = ['Januari','Februari','Maret','April','Mei','Juni','Juli',
                    'Agustus','September','Oktober','November','Desember'];

    function fmtClock(d) {
        return String(d.getHours()).padStart(2,'0') + ':' +
               String(d.getMinutes()).padStart(2,'0') + ':' +
               String(d.getSeconds()).padStart(2,'0');
    }
    function fmtDate(d) {
        return DAYS[d.getDay()] + ', ' + d.getDate() + ' ' +
               MONTHS[d.getMonth()] + ' ' + d.getFullYear();
    }

    // ── Constants ─────────────────────────────────────────────────────────────

    const HUBUNGAN = [
        { v: 'keluarga',  l: 'Keluarga' },
        { v: 'pengacara', l: 'Pengacara / Kuasa Hukum' },
        { v: 'teman',     l: 'Teman / Kenalan' },
        { v: 'lainnya',   l: 'Lainnya' },
    ];

    // ── App ───────────────────────────────────────────────────────────────────

    class TahtiKioskApp extends Component {

        static template = xml/* xml */`
<div class="ok-root">

<!-- ══════════════════ IDLE ══════════════════════════════════════════════════ -->
<div t-if="state.phase === 'idle'" class="ok-idle" t-on-click="startFlow">
    <img class="ok-idle-logo" src="/digital_kamtibmas/static/img/logo_app.png" alt="Logo"/>
    <div class="ok-idle-title">Buku Tamu Tahti</div>
    <div class="ok-idle-org">AMPERA247</div>
    <div class="ok-idle-divider"/>
    <div class="ok-idle-clock" t-esc="state.clock"/>
    <div class="ok-idle-date"  t-esc="state.date"/>
    <div class="ok-idle-cta">
        <span>&#9654;</span>
        <span>Sentuh untuk mulai</span>
    </div>
</div>

<!-- ══════════════════ SUCCESS ═══════════════════════════════════════════════ -->
<div t-elif="state.phase === 'sukses'" class="ok-success" t-on-click="goIdle">
    <div class="ok-success-ring">&#10003;</div>
    <div class="ok-success-title">Kunjungan Berhasil Didaftarkan</div>
    <div class="ok-success-code" t-esc="state.successCode"/>
    <div class="ok-success-msg">
        <b t-esc="state.successTamuNama"/> telah tercatat<br/>
        mengunjungi <b t-esc="state.successTahananNama"/>.
    </div>
    <div class="ok-success-countdown">
        Layar kembali otomatis dalam <b t-esc="state.countdown"/> detik
        &#160;·&#160; sentuh untuk menutup
    </div>
</div>

<!-- ══════════════════ WIZARD ════════════════════════════════════════════════ -->
<div t-elif="true" class="ok-screen">

    <!-- Nav bar -->
    <div class="ok-nav">
        <div class="ok-nav-brand">
            <img class="ok-nav-logo"
                 src="/digital_kamtibmas/static/img/logo_app.png" alt=""/>
            <span class="ok-nav-name">Buku Tamu Tahti</span>
        </div>

        <div class="ok-steps">
            <!-- Step 1 -->
            <div t-att-class="'ok-step ' + stepClass(1)">
                <div class="ok-step-num">
                    <span t-if="stepClass(1) === 'is-done'">&#10003;</span>
                    <span t-else="">1</span>
                </div>
                <span class="ok-step-label">Pilih Tahanan</span>
            </div>
            <span class="ok-step-arrow">&#8250;</span>
            <!-- Step 2: Foto KTP -->
            <div t-att-class="'ok-step ' + stepClass(2)">
                <div class="ok-step-num">
                    <span t-if="stepClass(2) === 'is-done'">&#10003;</span>
                    <span t-else="">2</span>
                </div>
                <span class="ok-step-label">Foto KTP</span>
            </div>
            <span class="ok-step-arrow">&#8250;</span>
            <!-- Step 3: Data Pengunjung -->
            <div t-att-class="'ok-step ' + stepClass(3)">
                <div class="ok-step-num">
                    <span t-if="stepClass(3) === 'is-done'">&#10003;</span>
                    <span t-else="">3</span>
                </div>
                <span class="ok-step-label">Data Pengunjung</span>
            </div>
            <span class="ok-step-arrow">&#8250;</span>
            <!-- Step 4: Konfirmasi -->
            <div t-att-class="'ok-step ' + stepClass(4)">
                <div class="ok-step-num">4</div>
                <span class="ok-step-label">Konfirmasi</span>
            </div>
        </div>

        <button class="ok-nav-cancel" t-on-click="goIdle">
            <span>&#x2715;</span> Batalkan
        </button>
    </div>

    <!-- ── Step 1: Cari Tahanan ──────────────────────────────────────── -->
    <t t-if="state.phase === 'cari_tahanan'">
        <div class="ok-body">
            <div class="ok-card">
                <div class="ok-card-head">
                    <div class="ok-card-head-icon">&#128269;</div>
                    <div class="ok-card-head-title">Pilih Tahanan yang Akan Dikunjungi</div>
                </div>
                <div class="ok-card-body">
                    <div class="ok-field">
                        <div class="ok-search-wrap">
                            <span class="ok-search-icon fa fa-search"/>
                            <input class="ok-search-input"
                                   type="text"
                                   placeholder="Cari nama tahanan..."
                                   autocomplete="off"
                                   t-att-value="state.searchKw"
                                   t-on-input="onSearchInput"/>
                        </div>
                    </div>

                    <div t-if="state.loadingTahanan" class="ok-loading">
                        <div class="ok-spinner"/>
                        <span>Memuat data...</span>
                    </div>

                    <div t-elif="state.tahananList.length === 0" class="ok-empty">
                        <div class="ok-empty-icon">&#128100;</div>
                        <div class="ok-empty-text">
                            <span t-if="state.searchKw">Tidak ada tahanan dengan nama tersebut</span>
                            <span t-else="">Belum ada data tahanan aktif</span>
                        </div>
                    </div>

                    <div t-else="" class="ok-list">
                        <t t-foreach="state.tahananList" t-as="t" t-key="t.id">
                            <div class="ok-list-item" t-on-click="() => this.selectTahanan(t)">
                                <div t-att-class="'ok-avatar' + (t.jenis_kelamin === 'perempuan' ? ' female' : '')">
                                    <span t-if="t.jenis_kelamin === 'perempuan'">&#128105;</span>
                                    <span t-else="">&#128104;</span>
                                </div>
                                <div class="ok-list-body">
                                    <div class="ok-list-name" t-esc="t.nama"/>
                                    <div class="ok-list-meta" t-esc="t.kategori_nama || '—'"/>
                                </div>
                                <span class="ok-badge" t-esc="t.sel_nama"/>
                                <span class="ok-list-arrow">&#8250;</span>
                            </div>
                        </t>
                    </div>
                </div>
            </div>
        </div>
        <div class="ok-footer">
            <div class="ok-footer-left"/>
            <div class="ok-footer-right">
                <button class="ok-btn ok-btn-light" t-on-click="goIdle">Batalkan</button>
            </div>
        </div>
    </t>

    <!-- ── Step 2: Foto KTP ──────────────────────────────────────────── -->
    <t t-if="state.phase === 'foto_ktp'">
        <div class="ok-body">
            <div class="ok-card">
                <div class="ok-card-head">
                    <div class="ok-card-head-icon">&#128247;</div>
                    <div class="ok-card-head-title">Foto KTP Pengunjung</div>
                </div>
                <div class="ok-card-body ok-camera-body">
                    <t t-if="!state.fotoKtp">
                        <!-- Error kamera -->
                        <t t-if="state.cameraError">
                            <div class="ok-camera-error">
                                <div class="ok-camera-error-icon">&#9888;</div>
                                <div class="ok-camera-error-msg" t-esc="state.cameraError"/>
                                <div class="ok-camera-error-hint">
                                    Pastikan izin kamera diaktifkan di browser,<br/>
                                    atau tekan <b>Lewati</b> untuk melanjutkan tanpa foto.
                                </div>
                            </div>
                        </t>
                        <!-- Live camera -->
                        <t t-else="">
                            <div class="ok-camera-hint">
                                <t t-if="state.cameraLoading">
                                    Menghubungkan ke kamera...
                                </t>
                                <t t-else="">
                                    &#128247; Posisikan KTP dalam bingkai lalu tekan <b>Ambil Foto</b>
                                </t>
                            </div>
                            <div class="ok-camera-wrap">
                                <video t-ref="ktpVideo" class="ok-camera-video"
                                       autoplay="true" playsinline="true" muted="true"/>
                                <!-- Loading overlay: visible while camera stream not yet ready -->
                                <t t-if="state.cameraLoading">
                                    <div class="ok-camera-loading-overlay">
                                        <div class="ok-spinner-cam"/>
                                        <span>Memuat kamera...</span>
                                    </div>
                                </t>
                                <div class="ok-ktp-overlay">
                                    <div class="ok-ktp-frame" t-ref="ktpFrame">
                                        <div class="ok-ktp-corner ok-ktp-tl"/>
                                        <div class="ok-ktp-corner ok-ktp-tr"/>
                                        <div class="ok-ktp-corner ok-ktp-bl"/>
                                        <div class="ok-ktp-corner ok-ktp-br"/>
                                        <div class="ok-ktp-label">KTP / Identitas</div>
                                    </div>
                                </div>
                            </div>
                        </t>
                    </t>
                    <!-- Preview setelah capture -->
                    <t t-else="">
                        <div class="ok-camera-hint ok-camera-hint-success">
                            &#10003; Foto berhasil diambil — periksa keterbacaannya
                        </div>
                        <div class="ok-ktp-preview-wrap">
                            <img t-att-src="state.fotoKtp" class="ok-ktp-preview-img"/>
                        </div>
                    </t>
                    <canvas t-ref="ktpCanvas" style="display:none"/>
                </div>
            </div>
        </div>
        <div class="ok-footer">
            <div class="ok-footer-left">
                <button class="ok-btn ok-btn-light" t-on-click="backToStep1Ktp">
                    &#8592; Kembali
                </button>
            </div>
            <div class="ok-footer-right">
                <t t-if="!state.fotoKtp">
                    <button class="ok-btn ok-btn-light" t-on-click="skipFotoKtp">
                        Lewati
                    </button>
                    <button class="ok-btn ok-btn-primary"
                            t-att-disabled="!!state.cameraError || state.cameraLoading"
                            t-on-click="captureKtp">
                        <t t-if="state.cameraLoading">
                            <div class="ok-spinner-sm"/>
                            Memuat kamera...
                        </t>
                        <t t-else="">
                            &#128247; Ambil Foto
                        </t>
                    </button>
                </t>
                <t t-else="">
                    <button class="ok-btn ok-btn-light" t-on-click="retakeFoto">
                        &#128247; Foto Ulang
                    </button>
                    <button class="ok-btn ok-btn-primary ok-btn-lg" t-on-click="goDataTamu">
                        Gunakan Foto &#160;&#8250;
                    </button>
                </t>
            </div>
        </div>
    </t>

    <!-- ── Step 3: Data Tamu ─────────────────────────────────────────── -->
    <t t-if="state.phase === 'data_tamu'">
        <div class="ok-body">

            <!-- Tahanan terpilih (ringkasan singkat) -->
            <div class="ok-card">
                <div class="ok-card-head">
                    <div class="ok-card-head-icon">&#128100;</div>
                    <div class="ok-card-head-title">Tahanan yang Dikunjungi</div>
                </div>
                <div class="ok-card-body">
                    <div class="ok-selected-item">
                        <div t-att-class="'ok-avatar' + (state.selectedTahanan.jenis_kelamin === 'perempuan' ? ' female' : '')">
                            <span t-if="state.selectedTahanan.jenis_kelamin === 'perempuan'">&#128105;</span>
                            <span t-else="">&#128104;</span>
                        </div>
                        <div>
                            <div class="ok-selected-name" t-esc="state.selectedTahanan.nama"/>
                            <div class="ok-selected-meta">
                                Sel / Kamar: <t t-esc="state.selectedTahanan.sel_nama"/>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <!-- Identitas pengunjung -->
            <div class="ok-card">
                <div class="ok-card-head">
                    <div class="ok-card-head-icon">&#128203;</div>
                    <div class="ok-card-head-title">Identitas Pengunjung</div>
                </div>
                <div class="ok-card-body">

                    <div class="ok-field">
                        <label class="ok-label">NIK<span class="ok-req">*</span></label>
                        <input t-att-class="'ok-input' + (state.errors.nik ? ' is-invalid' : '')"
                               type="tel"
                               inputmode="numeric"
                               maxlength="16"
                               placeholder="16 digit NIK sesuai KTP"
                               autocomplete="off"
                               t-att-value="state.nik"
                               t-on-input="onNikInput"/>
                        <div t-if="state.errors.nik" class="ok-errmsg" t-esc="state.errors.nik"/>

                        <div t-if="state.nikStatus === 'checking'" class="ok-loading" style="padding:10px 0">
                            <div class="ok-spinner"/>
                            <span>Memeriksa data...</span>
                        </div>
                        <div t-elif="state.nikStatus === 'found'" class="ok-nik-status ok-nik-found">
                            &#10003;&#160; Data ditemukan: <b t-esc="state.nikData.nama"/>
                        </div>
                        <div t-elif="state.nikStatus === 'not_found'" class="ok-nik-status ok-nik-new">
                            &#8505;&#160; NIK belum terdaftar — isi data di bawah
                        </div>
                    </div>

                    <div class="ok-field">
                        <label class="ok-label">Nama Lengkap<span class="ok-req">*</span></label>
                        <input t-att-class="'ok-input' + (state.errors.nama ? ' is-invalid' : '')"
                               type="text"
                               placeholder="Nama sesuai KTP"
                               t-att-value="state.nama"
                               t-att-readonly="state.nikStatus === 'found'"
                               t-on-input="onNamaInput"/>
                        <div t-if="state.errors.nama" class="ok-errmsg" t-esc="state.errors.nama"/>
                    </div>

                    <div class="ok-field" style="margin-bottom:0">
                        <label class="ok-label">No. HP / WhatsApp</label>
                        <input class="ok-input"
                               type="tel"
                               inputmode="tel"
                               placeholder="Opsional"
                               t-att-value="state.no_hp"
                               t-on-input="onHpInput"/>
                    </div>
                </div>
            </div>

            <!-- Hubungan + keperluan -->
            <div class="ok-card">
                <div class="ok-card-head">
                    <div class="ok-card-head-icon">&#128172;</div>
                    <div class="ok-card-head-title">Detail Kunjungan</div>
                </div>
                <div class="ok-card-body">
                    <div class="ok-field">
                        <label class="ok-label">Hubungan dengan Tahanan<span class="ok-req">*</span></label>
                        <div class="ok-chips">
                            <t t-foreach="hubunganOpts" t-as="h" t-key="h.v">
                                <button t-att-class="'ok-chip' + (state.hubungan === h.v ? ' is-active' : '')"
                                        t-on-click="() => this.setHubungan(h.v)"
                                        t-esc="h.l"/>
                            </t>
                        </div>
                    </div>
                    <div class="ok-field" style="margin-bottom:0">
                        <label class="ok-label">Keperluan / Tujuan Kunjungan</label>
                        <textarea class="ok-textarea"
                                  placeholder="Opsional — jelaskan tujuan kunjungan"
                                  t-att-value="state.keperluan"
                                  t-on-input="onKepInput"/>
                    </div>
                </div>
            </div>

        </div>
        <div class="ok-footer">
            <div class="ok-footer-left">
                <button class="ok-btn ok-btn-light" t-on-click="backToFotoKtp">
                    &#8592; Kembali
                </button>
            </div>
            <div class="ok-footer-right">
                <button class="ok-btn ok-btn-primary ok-btn-lg" t-on-click="goKonfirmasi">
                    Lanjut ke Konfirmasi &#160;&#8250;
                </button>
            </div>
        </div>
    </t>

    <!-- ── Step 4: Konfirmasi ─────────────────────────────────────────── -->
    <t t-if="state.phase === 'konfirmasi'">
        <div class="ok-body">
            <div class="ok-card">
                <div class="ok-card-head">
                    <div class="ok-card-head-icon">&#128203;</div>
                    <div class="ok-card-head-title">Ringkasan Kunjungan</div>
                </div>
                <div class="ok-card-body">
                    <div class="ok-summary">
                        <div class="ok-summary-row">
                            <div class="ok-summary-lbl">Tahanan</div>
                            <div class="ok-summary-val" t-esc="state.selectedTahanan.nama"/>
                        </div>
                        <div class="ok-summary-row">
                            <div class="ok-summary-lbl">Sel / Kamar</div>
                            <div class="ok-summary-val" t-esc="state.selectedTahanan.sel_nama"/>
                        </div>
                        <div class="ok-divider" style="margin:0"/>
                        <div class="ok-summary-row">
                            <div class="ok-summary-lbl">Pengunjung</div>
                            <div class="ok-summary-val" t-esc="state.nama"/>
                        </div>
                        <div class="ok-summary-row">
                            <div class="ok-summary-lbl">NIK</div>
                            <div class="ok-summary-val" t-esc="state.nik"/>
                        </div>
                        <div t-if="state.no_hp" class="ok-summary-row">
                            <div class="ok-summary-lbl">No. HP</div>
                            <div class="ok-summary-val" t-esc="state.no_hp"/>
                        </div>
                        <div class="ok-summary-row">
                            <div class="ok-summary-lbl">Hubungan</div>
                            <div class="ok-summary-val" t-esc="hubunganLabel"/>
                        </div>
                        <div t-if="state.keperluan" class="ok-summary-row">
                            <div class="ok-summary-lbl">Keperluan</div>
                            <div class="ok-summary-val" t-esc="state.keperluan"/>
                        </div>
                        <div class="ok-summary-row">
                            <div class="ok-summary-lbl">Foto KTP</div>
                            <div class="ok-summary-val">
                                <span t-if="state.fotoKtp" style="color:#28a745">&#10003; Tersedia</span>
                                <span t-else="" style="color:#aaa">Tidak ada</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            <div t-if="state.submitError" class="ok-alert ok-alert-danger">
                <span>&#9888;</span>
                <span t-esc="state.submitError"/>
            </div>
        </div>

        <div class="ok-footer">
            <div class="ok-footer-left">
                <button class="ok-btn ok-btn-light"
                        t-att-disabled="state.submitting"
                        t-on-click="backToDataTamu">
                    &#8592; Ubah Data
                </button>
            </div>
            <div class="ok-footer-right">
                <button class="ok-btn ok-btn-success ok-btn-lg"
                        t-att-disabled="state.submitting"
                        t-on-click="submitKunjungan">
                    <t t-if="state.submitting">
                        <div class="ok-spinner-sm"/>
                        Mendaftarkan...
                    </t>
                    <t t-else="">
                        &#10003;&#160; Daftar Kunjungan
                    </t>
                </button>
            </div>
        </div>
    </t>

</div><!-- end wizard -->

</div><!-- end ok-root -->
        `;

        setup() {
            this.hubunganOpts = HUBUNGAN;

            this.videoRef  = useRef('ktpVideo');
            this.canvasRef = useRef('ktpCanvas');
            this.frameRef  = useRef('ktpFrame');
            this._stream   = null;

            this.state = useState({
                phase: 'idle',
                clock: fmtClock(new Date()),
                date:  fmtDate(new Date()),
                // step 1
                searchKw:        '',
                tahananList:     [],
                loadingTahanan:  false,
                selectedTahanan: null,
                // step 2 camera
                fotoKtp:       null,
                cameraError:   '',
                cameraLoading: false,
                // step 3
                nik:       '',
                nikStatus: null,
                nikData:   null,
                nama:      '',
                no_hp:     '',
                hubungan:  'keluarga',
                keperluan: '',
                errors:    {},
                // step 4
                submitting:  false,
                submitError: '',
                // success
                successCode:        '',
                successTahananNama: '',
                successTamuNama:    '',
                countdown: 10,
            });

            this._clockTimer     = null;
            this._countdownTimer = null;
            this._nikTimer       = null;
            this._searchTimer    = null;

            onMounted(() => {
                this._clockTimer = setInterval(() => {
                    const now = new Date();
                    this.state.clock = fmtClock(now);
                    this.state.date  = fmtDate(now);
                }, 1000);
            });

            onPatched(() => {
                if (
                    this.state.phase === 'foto_ktp' &&
                    !this._stream &&
                    !this.state.fotoKtp &&
                    !this.state.cameraError &&
                    !this.state.cameraLoading
                ) {
                    this._startCamera();
                }
            });

            onWillUnmount(() => {
                clearInterval(this._clockTimer);
                clearInterval(this._countdownTimer);
                clearTimeout(this._nikTimer);
                clearTimeout(this._searchTimer);
                this._stopCamera();
            });
        }

        // ── Camera ────────────────────────────────────────────────────────────

        async _startCamera() {
            this.state.cameraLoading = true;
            try {
                const stream = await navigator.mediaDevices.getUserMedia({
                    video: {
                        facingMode: { ideal: 'environment' },
                        width:  { ideal: 1280 },
                        height: { ideal: 720 },
                    },
                });
                this._stream = stream;
                this.state.cameraLoading = false;
                const video = this.videoRef.el;
                if (video) {
                    video.srcObject = stream;
                    video.play().catch(() => {});
                }
            } catch (e) {
                this._stream = null;
                this.state.cameraLoading = false;
                let msg = 'Kamera tidak dapat diakses.';
                if (e.name === 'NotAllowedError')  msg = 'Akses kamera ditolak. Izinkan akses kamera di browser.';
                if (e.name === 'NotFoundError')    msg = 'Kamera tidak ditemukan pada perangkat ini.';
                if (e.name === 'NotReadableError') msg = 'Kamera sedang digunakan oleh aplikasi lain.';
                this.state.cameraError = msg;
            }
        }

        _stopCamera() {
            if (this._stream) {
                this._stream.getTracks().forEach(t => t.stop());
                this._stream = null;
            }
        }

        captureKtp() {
            const video  = this.videoRef.el;
            const canvas = this.canvasRef.el;
            const frame  = this.frameRef.el;
            if (!video || !canvas || !frame || !video.videoWidth) return;

            const vw = video.videoWidth;
            const vh = video.videoHeight;
            const videoRect = video.getBoundingClientRect();
            const frameRect = frame.getBoundingClientRect();

            // Hitung rendering object-fit: cover
            // (salah satu sisi dikrop agar video mengisi elemen)
            const videoAspect   = vw / vh;
            const elementAspect = videoRect.width / videoRect.height;

            let scale, offsetX, offsetY;
            if (videoAspect > elementAspect) {
                // Video lebih lebar → tinggi pas, kiri-kanan terpotong
                scale   = videoRect.height / vh;
                offsetX = (vw * scale - videoRect.width) / 2;
                offsetY = 0;
            } else {
                // Video lebih tinggi → lebar pas, atas-bawah terpotong
                scale   = videoRect.width / vw;
                offsetX = 0;
                offsetY = (vh * scale - videoRect.height) / 2;
            }

            // Posisi frame relatif terhadap sudut kiri-atas video element (CSS px)
            const relLeft = frameRect.left - videoRect.left;
            const relTop  = frameRect.top  - videoRect.top;

            // Konversi ke koordinat pixel source video
            const sx = (relLeft + offsetX) / scale;
            const sy = (relTop  + offsetY) / scale;
            const sw = frameRect.width  / scale;
            const sh = frameRect.height / scale;

            // Gambar hanya area frame ke canvas (resolusi asli crop area)
            canvas.width  = Math.round(sw);
            canvas.height = Math.round(sh);
            canvas.getContext('2d').drawImage(video, sx, sy, sw, sh, 0, 0, canvas.width, canvas.height);

            this.state.fotoKtp = canvas.toDataURL('image/jpeg', 0.90);
            this._stopCamera();
        }

        retakeFoto() {
            this.state.fotoKtp     = null;
            this.state.cameraError = '';
            // onPatched will restart camera automatically
        }

        skipFotoKtp() {
            this._stopCamera();
            this.state.fotoKtp = null;
            this.state.phase   = 'data_tamu';
        }

        goDataTamu() {
            this._stopCamera();
            this.state.phase = 'data_tamu';
        }

        backToStep1Ktp() {
            this._stopCamera();
            this.state.fotoKtp     = null;
            this.state.cameraError = '';
            this.state.phase       = 'cari_tahanan';
        }

        backToFotoKtp() {
            this.state.cameraError = '';
            this.state.phase       = 'foto_ktp';
            // onPatched will start camera if fotoKtp is null
        }

        // ── Navigation ────────────────────────────────────────────────────────

        startFlow() {
            this._resetData();
            this.state.phase = 'cari_tahanan';
            this._loadTahanan('');
        }

        goIdle() {
            clearInterval(this._countdownTimer);
            clearTimeout(this._nikTimer);
            clearTimeout(this._searchTimer);
            this._stopCamera();
            this._resetData();
            this.state.phase = 'idle';
        }

        backToDataTamu() { this.state.submitError = ''; this.state.phase = 'data_tamu'; }

        _resetData() {
            Object.assign(this.state, {
                searchKw: '', tahananList: [], loadingTahanan: false, selectedTahanan: null,
                fotoKtp: null, cameraError: '', cameraLoading: false,
                nik: '', nikStatus: null, nikData: null,
                nama: '', no_hp: '', hubungan: 'keluarga', keperluan: '',
                errors: {}, submitting: false, submitError: '',
                successCode: '', successTahananNama: '', successTamuNama: '', countdown: 10,
            });
        }

        // ── Step 1 ────────────────────────────────────────────────────────────

        onSearchInput(ev) {
            this.state.searchKw = ev.target.value;
            clearTimeout(this._searchTimer);
            this._searchTimer = setTimeout(() => this._loadTahanan(this.state.searchKw), 400);
        }

        async _loadTahanan(kw) {
            this.state.loadingTahanan = true;
            try {
                const list = await rpc('/tahti/api/cari_tahanan', { keyword: kw });
                this.state.tahananList = list || [];
            } catch (_) {
                this.state.tahananList = [];
            } finally {
                this.state.loadingTahanan = false;
            }
        }

        selectTahanan(t) {
            this.state.selectedTahanan = { ...t };
            Object.assign(this.state, {
                fotoKtp: null, cameraError: '', cameraLoading: false,
                nik: '', nikStatus: null, nikData: null,
                nama: '', no_hp: '', errors: {},
            });
            this.state.phase = 'foto_ktp';
        }

        // ── Step 3 ────────────────────────────────────────────────────────────

        onNikInput(ev) {
            this.state.nik       = ev.target.value;
            this.state.nikStatus = null;
            this.state.nikData   = null;
            this.state.errors    = { ...this.state.errors, nik: null };
            clearTimeout(this._nikTimer);
            if (this.state.nik.trim().length === 16) {
                this.state.nikStatus = 'checking';
                this._nikTimer = setTimeout(() => this._cekNik(this.state.nik.trim()), 600);
            }
        }

        async _cekNik(nik) {
            try {
                const res = await rpc('/tahti/api/cek_nik', { nik });
                if (res && res.found) {
                    this.state.nikStatus = 'found';
                    this.state.nikData   = res;
                    this.state.nama      = res.nama  || '';
                    this.state.no_hp     = res.no_hp || '';
                } else {
                    this.state.nikStatus = 'not_found';
                    this.state.nama = '';
                }
            } catch (_) {
                this.state.nikStatus = 'not_found';
            }
        }

        onNamaInput(ev)  { this.state.nama     = ev.target.value; }
        onHpInput(ev)    { this.state.no_hp    = ev.target.value; }
        onKepInput(ev)   { this.state.keperluan = ev.target.value; }
        setHubungan(val) { this.state.hubungan  = val; }

        goKonfirmasi() {
            const errs = {};
            const nik = this.state.nik.trim();
            if (!nik)                   errs.nik  = 'NIK wajib diisi';
            else if (nik.length !== 16) errs.nik  = 'NIK harus 16 digit';
            if (!this.state.nama.trim()) errs.nama = 'Nama wajib diisi';
            this.state.errors = errs;
            if (Object.keys(errs).length > 0) return;
            this.state.submitError = '';
            this.state.phase = 'konfirmasi';
        }

        // ── Step 4 ────────────────────────────────────────────────────────────

        async submitKunjungan() {
            if (this.state.submitting) return;
            this.state.submitting  = true;
            this.state.submitError = '';
            try {
                const res = await rpc('/tahti/api/daftar_kunjungan', {
                    data: {
                        tahanan_id: this.state.selectedTahanan.id,
                        nik:        this.state.nik.trim(),
                        nama:       this.state.nama.trim(),
                        no_hp:      this.state.no_hp.trim(),
                        hubungan:   this.state.hubungan,
                        keperluan:  this.state.keperluan.trim(),
                        foto_ktp:   this.state.fotoKtp || '',
                    },
                });
                if (!res || res.error) {
                    this.state.submitError = (res && res.error) || 'Terjadi kesalahan. Silakan coba lagi.';
                    return;
                }
                this.state.successCode        = res.code         || '-';
                this.state.successTahananNama = res.tahanan_nama || '';
                this.state.successTamuNama    = res.tamu_nama    || '';
                this.state.countdown = 10;
                this.state.phase = 'sukses';
                this._startCountdown();
            } catch (_) {
                this.state.submitError = 'Koneksi gagal. Silakan coba lagi.';
            } finally {
                this.state.submitting = false;
            }
        }

        _startCountdown() {
            clearInterval(this._countdownTimer);
            this._countdownTimer = setInterval(() => {
                this.state.countdown--;
                if (this.state.countdown <= 0) {
                    clearInterval(this._countdownTimer);
                    this.goIdle();
                }
            }, 1000);
        }

        // ── Computed ─────────────────────────────────────────────────────────

        get hubunganLabel() {
            const h = HUBUNGAN.find(x => x.v === this.state.hubungan);
            return h ? h.l : this.state.hubungan;
        }

        stepClass(n) {
            const map = { cari_tahanan: 1, foto_ktp: 2, data_tamu: 3, konfirmasi: 4 };
            const cur = map[this.state.phase] || 1;
            if (n < cur)   return 'is-done';
            if (n === cur) return 'is-active';
            return '';
        }
    }

    // ── Mount ─────────────────────────────────────────────────────────────────

    const el = document.getElementById('tahti-kiosk-app');
    if (el) mount(TahtiKioskApp, el);

})();
