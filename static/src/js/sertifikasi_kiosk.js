/* Sertifikasi Narkoba — Kiosk Web App
   OWL 2 standalone, IIFE pattern
   Route: /sertifikasi/<token>  auth=public */
(function () {
    'use strict';

    const { Component, useState, mount, xml, onMounted, onWillUnmount } = owl;

    // ── Token dari URL ────────────────────────────────────────────────────────

    const TOKEN = (function () {
        const parts = window.location.pathname.split('/');
        return parts[parts.length - 1] || '';
    })();

    // Logo company dibaca sebelum OWL mount (div sudah ada di DOM)
    const LOGO_URL = (document.getElementById('sertifikasi-kiosk-app') || {}).dataset?.logo
        || '/digital_kamtibmas/static/img/logo_polda.png';

    // ── RPC helper ────────────────────────────────────────────────────────────

    async function rpc(route, params) {
        const res = await fetch(route, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ jsonrpc: '2.0', method: 'call', params: params || {} }),
        });
        const json = await res.json();
        if (json.error) {
            const msg = (json.error.data && json.error.data.message) || json.error.message || 'Server error';
            throw new Error(msg);
        }
        return json.result;
    }

    // ── Format timer mm:ss ─────────────────────────────────────────────────

    function fmtTimer(secs) {
        const m = Math.floor(secs / 60);
        const s = secs % 60;
        return String(m).padStart(2, '0') + ':' + String(s).padStart(2, '0');
    }

    // ── App ───────────────────────────────────────────────────────────────────

    class SertifikasiKioskApp extends Component {

        static template = xml/* xml */`
<div id="sertifikasi-kiosk-app">

<!-- ══════════════════ LOADING ══════════════════════════════════════════════ -->
<div t-if="state.phase === 'loading'" class="sk-screen" style="background:var(--navy)">
    <div class="sk-spinner"/>
    <div class="sk-loading-text">Memuat...</div>
</div>

<!-- ══════════════════ ERROR ════════════════════════════════════════════════ -->
<div t-elif="state.phase === 'error'" class="sk-screen sk-error">
    <div class="sk-error-icon">&#9888;</div>
    <div class="sk-title" style="color:#FC8181">Tidak Dapat Memuat Ujian</div>
    <div class="sk-error-msg" t-esc="state.errorMsg"/>
</div>

<!-- ══════════════════ IDLE ═════════════════════════════════════════════════ -->
<div t-elif="state.phase === 'idle'" class="sk-screen sk-idle">
    <img class="sk-logo" t-att-src="logoUrl" alt="Logo"/>
    <div class="sk-idle-badge">Sertifikasi Anti Narkoba</div>
    <div class="sk-idle-title" t-esc="state.info.name"/>
    <div class="sk-idle-org">AMPERA247</div>

    <div class="sk-idle-meta">
        <div class="sk-idle-meta-item">
            <div class="sk-idle-meta-num" t-esc="state.info.jumlah_soal"/>
            <div class="sk-idle-meta-label">Soal</div>
        </div>
        <div class="sk-idle-meta-item">
            <div class="sk-idle-meta-num" t-esc="state.info.waktu_menit"/>
            <div class="sk-idle-meta-label">Menit</div>
        </div>
        <div class="sk-idle-meta-item">
            <div class="sk-idle-meta-num" t-esc="state.info.nilai_kelulusan + '%'"/>
            <div class="sk-idle-meta-label">Kelulusan</div>
        </div>
    </div>

    <t t-if="state.info.tanggal_expired">
        <div class="sk-idle-expired">Berlaku hingga: <b t-esc="state.info.tanggal_expired"/></div>
    </t>

    <button class="sk-idle-cta" t-on-click="goIdentitas">
        <span>&#9654;</span>
        <span>Mulai Ujian</span>
    </button>
</div>

<!-- ══════════════════ IDENTITAS ════════════════════════════════════════════ -->
<div t-elif="state.phase === 'identitas'" class="sk-screen" style="background:#F0F4F8">
    <div class="sk-card">
        <div class="sk-title">Data Peserta</div>
        <div class="sk-subtitle">Isi identitas Anda sebelum memulai ujian</div>
        <div class="sk-divider"/>

        <div class="sk-form-group">
            <label class="sk-label">NIK <span class="sk-req">*</span></label>
            <input class="sk-input"
                   type="tel"
                   inputmode="numeric"
                   maxlength="16"
                   placeholder="16 digit NIK"
                   t-att-value="state.form.nik"
                   t-on-input="onNikInput"/>
            <!-- NIK status indicator -->
            <div t-if="state.nikChecking"
                 style="font-size:12px;color:var(--muted);margin-top:4px">
                &#9203; Memeriksa data...
            </div>
            <div t-elif="state.nikStatus === 'found'"
                 style="font-size:12px;color:var(--green);margin-top:4px;font-weight:600">
                &#10003; Data ditemukan — formulir telah diisi otomatis
            </div>
            <div t-elif="state.nikStatus === 'new'"
                 style="font-size:12px;color:var(--muted);margin-top:4px">
                NIK baru — lengkapi formulir di bawah
            </div>
        </div>

        <div class="sk-form-group">
            <label class="sk-label">Nama Lengkap <span class="sk-req">*</span></label>
            <input class="sk-input"
                   type="text"
                   placeholder="Nama sesuai KTP"
                   t-att-value="state.form.nama"
                   t-on-input="ev => state.form.nama = ev.target.value"/>
        </div>

        <div class="sk-form-row">
            <div class="sk-form-group">
                <label class="sk-label">Tempat Lahir</label>
                <input class="sk-input"
                       type="text"
                       placeholder="Kota lahir"
                       t-att-value="state.form.tempat_lahir"
                       t-on-input="ev => state.form.tempat_lahir = ev.target.value"/>
            </div>
            <div class="sk-form-group">
                <label class="sk-label">Tanggal Lahir</label>
                <input class="sk-input"
                       type="date"
                       t-att-value="state.form.tanggal_lahir"
                       t-on-input="ev => state.form.tanggal_lahir = ev.target.value"/>
            </div>
        </div>

        <div class="sk-form-row">
            <div class="sk-form-group">
                <label class="sk-label">Jenis Kelamin</label>
                <select class="sk-select"
                        t-att-value="state.form.jenis_kelamin"
                        t-on-change="ev => state.form.jenis_kelamin = ev.target.value">
                    <option value="">-- Pilih --</option>
                    <option value="laki">Laki-laki</option>
                    <option value="perempuan">Perempuan</option>
                </select>
            </div>
            <div class="sk-form-group">
                <label class="sk-label">No. HP</label>
                <input class="sk-input"
                       type="tel"
                       placeholder="08xx"
                       t-att-value="state.form.no_hp"
                       t-on-input="ev => state.form.no_hp = ev.target.value"/>
            </div>
        </div>

        <div class="sk-form-group">
            <label class="sk-label">Alamat</label>
            <input class="sk-input"
                   type="text"
                   placeholder="Alamat lengkap"
                   t-att-value="state.form.alamat"
                   t-on-input="ev => state.form.alamat = ev.target.value"/>
        </div>

        <t t-if="state.formError">
            <div style="color:var(--red);font-size:13px;margin-bottom:10px;text-align:center"
                 t-esc="state.formError"/>
        </t>

        <button class="sk-btn sk-btn-primary"
                t-on-click="submitIdentitas"
                t-att-disabled="state.loading">
            <t t-if="state.loading">Memuat soal...</t>
            <t t-else="">Lanjut ke Soal &#8594;</t>
        </button>

        <button class="sk-btn sk-btn-outline" style="margin-top:8px" t-on-click="goIdle">
            Kembali
        </button>
    </div>
</div>

<!-- ══════════════════ SOAL ══════════════════════════════════════════════════ -->
<div t-elif="state.phase === 'soal'"
     class="sk-screen sk-soal-screen"
     style="display:flex;flex-direction:column">

    <!-- Header -->
    <div class="sk-soal-header">
        <div class="sk-soal-progress-text">
            Soal <t t-esc="state.soalIdx + 1"/> / <t t-esc="state.soalList.length"/>
        </div>
        <div t-att-class="'sk-timer' + (state.timerSecs &lt;= 60 ? ' sk-timer-warn' : '')">
            &#9200; <span t-esc="fmtTimer(state.timerSecs)"/>
        </div>
    </div>

    <!-- Progress bar -->
    <div class="sk-progress-bar-wrap">
        <div class="sk-progress-bar">
            <div class="sk-progress-fill"
                 t-att-style="'width:' + ((state.soalIdx + 1) / state.soalList.length * 100) + '%'"/>
        </div>
    </div>

    <!-- Body: soal saat ini -->
    <div class="sk-soal-body">
        <t t-set="soal" t-value="state.soalList[state.soalIdx]"/>
        <div class="sk-soal-card">
            <div class="sk-soal-no">Soal <t t-esc="soal.no"/></div>
            <div class="sk-soal-text" t-esc="soal.name"/>
            <div class="sk-pilihan-list">
                <t t-foreach="soal.pilihan" t-as="p" t-key="p.id">
                    <t t-set="chosen" t-value="state.jawaban[soal.id]"/>
                    <div t-att-class="'sk-pilihan-item' + (chosen === p.id ? ' selected' : '')"
                         t-on-click="() => this.pilihJawaban(soal.id, p.id)">
                        <div class="sk-pilihan-marker" t-esc="p.letter"/>
                        <div class="sk-pilihan-text" t-esc="p.name"/>
                    </div>
                </t>
            </div>
        </div>
        <div class="sk-answered-count">
            Terjawab: <t t-esc="Object.keys(state.jawaban).length"/> / <t t-esc="state.soalList.length"/>
        </div>
    </div>

    <!-- Footer nav -->
    <div class="sk-soal-footer">
        <button class="sk-btn-nav"
                t-att-disabled="state.soalIdx === 0"
                t-on-click="prevSoal">
            &#8592; Sebelumnya
        </button>

        <t t-if="state.soalIdx &lt; state.soalList.length - 1">
            <button class="sk-btn-nav" style="flex:2;background:var(--blue);color:#fff;border-color:var(--blue)"
                    t-on-click="nextSoal">
                Berikutnya &#8594;
            </button>
        </t>
        <t t-else="">
            <button class="sk-btn-submit"
                    t-on-click="confirmSubmit"
                    t-att-disabled="state.submitting">
                <t t-if="state.submitting">Mengirim...</t>
                <t t-else="">Kumpulkan Jawaban</t>
            </button>
        </t>
    </div>
</div>

<!-- ══════════════════ KONFIRMASI SUBMIT ═════════════════════════════════════ -->
<div t-elif="state.phase === 'konfirmasi'" class="sk-screen" style="background:#F0F4F8">
    <div class="sk-card" style="text-align:center">
        <div style="font-size:48px;margin-bottom:12px">&#10067;</div>
        <div class="sk-title">Yakin Ingin Mengumpulkan?</div>
        <div class="sk-subtitle">
            Anda menjawab <b><t t-esc="Object.keys(state.jawaban).length"/></b>
            dari <b><t t-esc="state.soalList.length"/></b> soal.
            <t t-if="Object.keys(state.jawaban).length &lt; state.soalList.length">
                <br/><span style="color:var(--red)">
                    Masih ada <t t-esc="state.soalList.length - Object.keys(state.jawaban).length"/> soal belum dijawab.
                </span>
            </t>
        </div>
        <div class="sk-divider"/>
        <button class="sk-btn sk-btn-success" t-on-click="doSubmit" t-att-disabled="state.submitting">
            <t t-if="state.submitting">Mengirim...</t>
            <t t-else="">Ya, Kumpulkan Sekarang</t>
        </button>
        <button class="sk-btn sk-btn-outline" style="margin-top:8px" t-on-click="backToSoal">
            Kembali Periksa Jawaban
        </button>
    </div>
</div>

<!-- ══════════════════ HASIL ══════════════════════════════════════════════════ -->
<div t-elif="state.phase === 'hasil'" class="sk-screen sk-hasil-screen">
    <t t-set="r" t-value="state.hasil"/>

    <div t-att-class="'sk-hasil-ring ' + (r.lulus ? 'lulus' : 'gagal')">
        <t t-if="r.lulus">&#10003;</t>
        <t t-else="">&#10007;</t>
    </div>

    <div t-att-class="'sk-hasil-status ' + (r.lulus ? 'lulus' : 'gagal')">
        <t t-if="r.lulus">LULUS</t>
        <t t-else="">TIDAK LULUS</t>
    </div>
    <div class="sk-hasil-nama" t-esc="r.nama"/>

    <div class="sk-nilai-besar" t-esc="r.nilai.toFixed(1)"/>
    <div class="sk-nilai-label">Nilai (Min. lulus: <t t-esc="r.nilai_lulus"/>%)</div>

    <div class="sk-hasil-detail">
        <div class="sk-hasil-detail-item">
            <div class="sk-hasil-detail-num" t-esc="r.total_benar"/>
            <div class="sk-hasil-detail-label">Benar</div>
        </div>
        <div class="sk-hasil-detail-item">
            <div class="sk-hasil-detail-num" t-esc="r.total_soal - r.total_benar"/>
            <div class="sk-hasil-detail-label">Salah</div>
        </div>
        <div class="sk-hasil-detail-item">
            <div class="sk-hasil-detail-num" t-esc="r.total_soal"/>
            <div class="sk-hasil-detail-label">Total Soal</div>
        </div>
    </div>

    <button class="sk-idle-cta" t-on-click="goIdle">
        Selesai
    </button>
</div>

</div>
        `;

        setup() {
            this.logoUrl = LOGO_URL;
            this.state = useState({
                phase: 'loading',
                errorMsg: '',
                info: {},

                // form identitas
                form: {
                    nik: '', nama: '', tempat_lahir: '',
                    tanggal_lahir: '', jenis_kelamin: '', no_hp: '', alamat: '',
                },
                formError: '',
                nikStatus: '',    // '' | 'found' | 'new'
                nikChecking: false,
                loading: false,

                // soal
                soalList: [],
                soalIdx: 0,
                jawaban: {},          // { soal_id: pilihan_id }
                pesertaId: null,
                timerSecs: 0,
                submitting: false,

                // hasil
                hasil: null,
            });

            this._timerInterval = null;
            onMounted(() => this._loadInfo());
            onWillUnmount(() => this._clearTimer());
        }

        // ── Timer ─────────────────────────────────────────────────────────────

        _startTimer(menit) {
            this._clearTimer();
            this.state.timerSecs = menit * 60;
            this._timerInterval = setInterval(() => {
                if (this.state.timerSecs <= 0) {
                    this._clearTimer();
                    this.doSubmit(true);
                    return;
                }
                this.state.timerSecs -= 1;
            }, 1000);
        }

        _clearTimer() {
            if (this._timerInterval) {
                clearInterval(this._timerInterval);
                this._timerInterval = null;
            }
        }

        // ── Input handlers ────────────────────────────────────────────────────

        onNikInput(ev) {
            const val = ev.target.value.replace(/[^0-9]/g, '');
            this.state.form.nik = val;
            if (val.length === 16) {
                this._cekNik(val);
            } else {
                this.state.nikStatus = '';
            }
        }

        async _cekNik(nik) {
            this.state.nikChecking = true;
            try {
                const result = await rpc('/sertifikasi/api/cek_nik', { token: TOKEN, nik });
                if (result.found) {
                    this.state.nikStatus       = 'found';
                    this.state.form.nama        = result.nama;
                    this.state.form.tempat_lahir = result.tempat_lahir;
                    this.state.form.tanggal_lahir = result.tanggal_lahir;
                    this.state.form.jenis_kelamin = result.jenis_kelamin;
                    this.state.form.no_hp       = result.no_hp;
                    this.state.form.alamat      = result.alamat;
                } else {
                    this.state.nikStatus = 'new';
                }
            } catch (_e) {
                this.state.nikStatus = '';
            } finally {
                this.state.nikChecking = false;
            }
        }

        // ── Load info ─────────────────────────────────────────────────────────

        async _loadInfo() {
            try {
                const result = await rpc('/sertifikasi/api/info', { token: TOKEN });
                if (result.error) {
                    this.state.phase    = 'error';
                    this.state.errorMsg = result.error;
                    return;
                }
                this.state.info  = result;
                this.state.phase = 'idle';
            } catch (e) {
                this.state.phase    = 'error';
                this.state.errorMsg = e.message || 'Gagal memuat data ujian.';
            }
        }

        // ── Navigation ────────────────────────────────────────────────────────

        goIdle() {
            this._clearTimer();
            this.state.phase       = 'idle';
            this.state.form        = { nik: '', nama: '', tempat_lahir: '', tanggal_lahir: '', jenis_kelamin: '', no_hp: '', alamat: '' };
            this.state.formError   = '';
            this.state.nikStatus   = '';
            this.state.nikChecking = false;
            this.state.jawaban     = {};
            this.state.soalList    = [];
            this.state.soalIdx     = 0;
            this.state.pesertaId   = null;
            this.state.hasil       = null;
        }

        goIdentitas() {
            this.state.phase     = 'identitas';
            this.state.formError = '';
        }

        async submitIdentitas() {
            const f = this.state.form;
            if (!f.nik || f.nik.length < 16) {
                this.state.formError = 'NIK harus 16 digit.';
                return;
            }
            if (!f.nama.trim()) {
                this.state.formError = 'Nama lengkap wajib diisi.';
                return;
            }
            this.state.formError = '';
            this.state.loading   = true;
            try {
                const result = await rpc('/sertifikasi/api/mulai', {
                    token: TOKEN,
                    data:  {
                        nik:           f.nik,
                        nama:          f.nama.trim(),
                        tempat_lahir:  f.tempat_lahir.trim(),
                        tanggal_lahir: f.tanggal_lahir || false,
                        jenis_kelamin: f.jenis_kelamin || false,
                        no_hp:         f.no_hp.trim(),
                        alamat:        f.alamat.trim(),
                    },
                });
                if (result.error) {
                    this.state.formError = result.error;
                    return;
                }
                this.state.pesertaId = result.peserta_id;
                const LETTERS = ['A','B','C','D','E','F'];
                this.state.soalList = result.soal.map(soal => ({
                    ...soal,
                    pilihan: soal.pilihan.map((p, i) => ({ ...p, letter: LETTERS[i] || (i + 1).toString() })),
                }));
                this.state.soalIdx   = 0;
                this.state.jawaban   = {};
                this.state.phase     = 'soal';
                this._startTimer(result.waktu_menit);
            } catch (e) {
                this.state.formError = e.message || 'Gagal memuat soal.';
            } finally {
                this.state.loading = false;
            }
        }

        pilihJawaban(soalId, pilihanId) {
            this.state.jawaban = { ...this.state.jawaban, [soalId]: pilihanId };
        }

        nextSoal() {
            if (this.state.soalIdx < this.state.soalList.length - 1) {
                this.state.soalIdx++;
            }
        }

        prevSoal() {
            if (this.state.soalIdx > 0) {
                this.state.soalIdx--;
            }
        }

        confirmSubmit() {
            this.state.phase = 'konfirmasi';
        }

        backToSoal() {
            this.state.phase = 'soal';
        }

        async doSubmit() {
            if (this.state.submitting) return;
            this._clearTimer();
            this.state.submitting = true;
            this.state.phase      = 'konfirmasi';

            try {
                const jawabanArr = this.state.soalList.map(soal => ({
                    soal_id:    soal.id,
                    pilihan_id: this.state.jawaban[soal.id] || 0,
                }));

                const result = await rpc('/sertifikasi/api/submit', {
                    token: TOKEN,
                    data: {
                        peserta_id: this.state.pesertaId,
                        jawaban:    jawabanArr,
                    },
                });

                if (result.error) {
                    this.state.submitting = false;
                    this.state.phase      = 'soal';
                    alert(result.error);
                    return;
                }

                this.state.hasil     = result;
                this.state.phase     = 'hasil';
                this.state.submitting = false;
            } catch (e) {
                this.state.submitting = false;
                this.state.phase      = 'soal';
                alert(e.message || 'Gagal mengirim jawaban.');
            }
        }

        // ── Template helper ───────────────────────────────────────────────────

        fmtTimer(secs) { return fmtTimer(secs); }
    }

    // ── Mount ─────────────────────────────────────────────────────────────────

    const container = document.getElementById('sertifikasi-kiosk-app');
    if (container) {
        mount(SertifikasiKioskApp, container);
    }

})();
