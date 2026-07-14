/* Mobile Chat — standalone page for konseling discuss channel */
/* Variables CHANNEL_ID, MY_PARTNER_ID, CHANNEL_NAME are injected by QWeb */

(function () {
    'use strict';

    // ── DOM refs ──────────────────────────────────────────────────────────────
    const msgList         = document.getElementById('msg-list');
    const msgLoading      = document.getElementById('msg-loading');
    const msgEmpty        = document.getElementById('msg-empty');
    const sendBtn         = document.getElementById('send-btn');
    const msgInput        = document.getElementById('msg-input');
    const scrollBtn       = document.getElementById('scroll-btn');
    const fileInput       = document.getElementById('file-input');
    const attachBtn       = document.getElementById('attach-btn');
    const attachPreview   = document.getElementById('attach-preview');
    const attachThumb     = document.getElementById('attach-thumb');
    const attachName      = document.getElementById('attach-name');
    const attachRemove    = document.getElementById('attach-remove');
    const typingIndicator = document.getElementById('typing-indicator');
    const typingText      = document.getElementById('typing-text');

    // ── State ─────────────────────────────────────────────────────────────────
    let lastMsgId       = 0;
    let firstMsgId      = Infinity;
    let isLoadingMore   = false;
    let hasMoreMessages = true;
    let pendingFile     = null;
    let isTyping        = false;
    let typingTimer     = null;

    // ── JSON-RPC helper ───────────────────────────────────────────────────────
    async function callKw(model, method, args, kwargs) {
        const res = await fetch('/web/dataset/call_kw', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                jsonrpc: '2.0', method: 'call', id: Date.now(),
                params: { model, method, args, kwargs: kwargs || {} },
            }),
        });
        const j = await res.json();
        if (j.error) {
            const msg = (j.error.data && j.error.data.message) || j.error.message || 'Error';
            throw new Error(msg);
        }
        return j.result;
    }

    // ── Fetch pesan baru (afterId > 0) atau awal (afterId = 0) ───────────────
    async function fetchMessages(afterId) {
        const domain = [
            ['res_id', '=', CHANNEL_ID],
            ['model', '=', 'discuss.channel'],
            ['message_type', 'in', ['comment', 'email']],
        ];
        if (afterId > 0) domain.push(['id', '>', afterId]);
        return callKw('mail.message', 'search_read', [domain], {
            fields: ['id', 'body', 'author_id', 'date', 'attachment_ids'],
            order: 'id asc',
            limit: afterId > 0 ? 20 : 50,
        });
    }

    // ── Load pesan lebih lama (scroll ke atas) ────────────────────────────────
    async function loadMoreMessages() {
        if (isLoadingMore || !hasMoreMessages || firstMsgId === Infinity) return;
        isLoadingMore = true;

        const spinner = document.createElement('div');
        spinner.className = 'load-more-spinner';
        msgList.insertBefore(spinner, msgList.firstChild);
        const savedHeight = msgList.scrollHeight;

        try {
            const domain = [
                ['res_id', '=', CHANNEL_ID],
                ['model', '=', 'discuss.channel'],
                ['message_type', 'in', ['comment', 'email']],
                ['id', '<', firstMsgId],
            ];
            const msgs = await callKw('mail.message', 'search_read', [domain], {
                fields: ['id', 'body', 'author_id', 'date', 'attachment_ids'],
                order: 'id desc',
                limit: 20,
            });

            spinner.remove();

            if (msgs.length === 0) {
                hasMoreMessages = false;
                showLoadEnd();
                return;
            }

            msgs.reverse(); // urutan asc (terlama dulu)
            const frag = document.createDocumentFragment();
            msgs.forEach(function (m) {
                if (!document.querySelector('[data-id="' + m.id + '"]')) {
                    frag.appendChild(renderMsg(m));
                    if (m.id < firstMsgId) firstMsgId = m.id;
                }
            });
            msgList.insertBefore(frag, msgList.firstChild);
            rebuildSeparators();
            msgList.scrollTop += msgList.scrollHeight - savedHeight;

            if (msgs.length < 20) { hasMoreMessages = false; showLoadEnd(); }
        } catch (_) {
            spinner.remove();
        } finally {
            isLoadingMore = false;
        }
    }

    function showLoadEnd() {
        const el = document.createElement('div');
        el.className = 'load-more-end';
        el.textContent = 'Awal percakapan';
        msgList.insertBefore(el, msgList.firstChild);
    }

    // ── Send message ──────────────────────────────────────────────────────────
    async function sendMessage(body, attachmentIds) {
        return callKw('discuss.channel', 'message_post', [[CHANNEL_ID]], {
            body: body,
            message_type: 'comment',
            subtype_xmlid: 'mail.mt_comment',
            attachment_ids: attachmentIds && attachmentIds.length ? attachmentIds : [],
        });
    }

    // ── Upload file via base64 ────────────────────────────────────────────────
    function uploadFile(file) {
        return new Promise(function (resolve, reject) {
            const reader = new FileReader();
            reader.onload = async function (e) {
                try {
                    const base64 = e.target.result.split(',')[1];
                    const result = await callKw('ir.attachment', 'create', [{
                        name: file.name,
                        datas: base64,
                        mimetype: file.type || 'application/octet-stream',
                        res_model: 'discuss.channel',
                        res_id: CHANNEL_ID,
                    }], {});
                    // create() bisa return int atau [int] tergantung versi Odoo
                    resolve(Array.isArray(result) ? result[0] : result);
                } catch (err) { reject(err); }
            };
            reader.onerror = reject;
            reader.readAsDataURL(file);
        });
    }

    // ── Kompresi gambar via Canvas ────────────────────────────────────────────
    const MAX_FILE_MB        = 10;
    const COMPRESS_THRESHOLD = 300 * 1024; // 300 KB
    const COMPRESS_MAX_PX    = 1280;
    const COMPRESS_QUALITY   = 0.82;

    function compressImage(file) {
        return new Promise(function (resolve) {
            const img = new Image();
            const url = URL.createObjectURL(file);
            img.onload = function () {
                URL.revokeObjectURL(url);
                let w = img.naturalWidth, h = img.naturalHeight;
                const ratio = Math.min(COMPRESS_MAX_PX / w, COMPRESS_MAX_PX / h);
                if (ratio < 1) { w = Math.round(w * ratio); h = Math.round(h * ratio); }
                const canvas = document.createElement('canvas');
                canvas.width = w; canvas.height = h;
                canvas.getContext('2d').drawImage(img, 0, 0, w, h);
                canvas.toBlob(function (blob) {
                    resolve(new File([blob], file.name.replace(/\.[^.]+$/, '.jpg'), {
                        type: 'image/jpeg',
                    }));
                }, 'image/jpeg', COMPRESS_QUALITY);
            };
            img.onerror = function () { URL.revokeObjectURL(url); resolve(file); };
            img.src = url;
        });
    }

    async function prepareFile(file) {
        if (file.size > MAX_FILE_MB * 1024 * 1024) {
            throw new Error('File terlalu besar. Maksimum ' + MAX_FILE_MB + 'MB.');
        }
        if (file.type.startsWith('image/') && file.type !== 'image/gif'
                && file.size > COMPRESS_THRESHOLD) {
            return compressImage(file);
        }
        return file;
    }

    // ── Preview file yang dipilih ─────────────────────────────────────────────
    async function showAttachPreview(file) {
        try {
            const prepared = await prepareFile(file);
            pendingFile = prepared;
            attachName.textContent = prepared.name;
            attachPreview.style.display = 'flex';
            if (prepared.type.startsWith('image/')) {
                attachThumb.src = URL.createObjectURL(prepared);
                attachThumb.style.display = 'block';
            } else {
                attachThumb.style.display = 'none';
            }
        } catch (e) {
            alert(e.message);
            fileInput.value = '';
        }
    }

    function clearAttachPreview() {
        pendingFile = null;
        fileInput.value = '';
        attachPreview.style.display = 'none';
        attachThumb.src = '';
    }

    // ── HTML escape ───────────────────────────────────────────────────────────
    function esc(s) {
        return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;')
            .replace(/>/g, '&gt;').replace(/"/g, '&quot;');
    }

    // ── Cek body HTML kosong ──────────────────────────────────────────────────
    function isEmptyBody(html) {
        if (!html) return true;
        const tmp = document.createElement('div');
        tmp.innerHTML = html;
        return !tmp.textContent.trim() && !tmp.querySelector('img');
    }

    // ── Date separator helpers ────────────────────────────────────────────────
    function datePart(dateStr) { return dateStr.slice(0, 10); }

    function formatDateLabel(dp) {
        const d = new Date(dp + 'T00:00:00');
        const today     = new Date(); today.setHours(0, 0, 0, 0);
        const yesterday = new Date(today); yesterday.setDate(today.getDate() - 1);
        if (d.getTime() === today.getTime())     return 'Hari ini';
        if (d.getTime() === yesterday.getTime()) return 'Kemarin';
        return d.toLocaleDateString('id-ID', {
            weekday: 'long', day: 'numeric', month: 'long', year: 'numeric',
        });
    }

    function makeDateSeparator(dp) {
        const el = document.createElement('div');
        el.className = 'date-sep';
        el.dataset.date = dp;
        const span = document.createElement('span');
        span.textContent = formatDateLabel(dp);
        el.appendChild(span);
        return el;
    }

    // Rebuild semua separator dari scratch berdasarkan urutan .msg di DOM
    function rebuildSeparators() {
        msgList.querySelectorAll('.date-sep').forEach(function (el) { el.remove(); });
        let prevDp = null;
        msgList.querySelectorAll('.msg').forEach(function (msgEl) {
            const dp = msgEl.dataset.date;
            if (!dp || dp === prevDp) return;
            prevDp = dp;
            msgList.insertBefore(makeDateSeparator(dp), msgEl);
        });
    }

    // ── Render satu message ───────────────────────────────────────────────────
    function renderMsg(msg) {
        const isMine = Array.isArray(msg.author_id) && msg.author_id[0] === MY_PARTNER_ID;
        const name   = Array.isArray(msg.author_id) ? msg.author_id[1] : '?';
        const dt     = new Date(msg.date.replace(' ', 'T') + 'Z');
        const time   = dt.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });

        const div = document.createElement('div');
        div.className    = 'msg ' + (isMine ? 'mine' : 'other');
        div.dataset.id   = msg.id;
        div.dataset.date = datePart(msg.date);

        const hasBody   = !isEmptyBody(msg.body);
        const hasAttach = Array.isArray(msg.attachment_ids) && msg.attachment_ids.length > 0;

        let html = '';
        if (!isMine) html += '<div class="msg-name">' + esc(name) + '</div>';
        if (hasBody)  html += '<div class="msg-bubble">' + msg.body + '</div>';
        html += '<div class="msg-time">' + esc(time) + '</div>';
        div.innerHTML = html;

        if (hasAttach) {
            const timeEl = div.querySelector('.msg-time');
            msg.attachment_ids.forEach(function (attId) {
                const wrap = document.createElement('div');
                wrap.className = 'msg-attachment';

                const img = document.createElement('img');
                img.className = 'msg-img';
                img.loading = 'lazy';
                img.alt = '';
                img.src = '/web/image/' + attId;
                img.addEventListener('click', function () {
                    window.open('/web/image/' + attId, '_blank');
                });
                img.addEventListener('error', function () {
                    wrap.innerHTML = '';
                    const link = document.createElement('a');
                    link.className = 'msg-file';
                    link.href = '/web/content/' + attId + '?download=1';
                    link.target = '_blank'; link.rel = 'noopener';
                    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
                    svg.setAttribute('width', '14'); svg.setAttribute('height', '14');
                    svg.setAttribute('viewBox', '0 0 24 24'); svg.setAttribute('fill', 'currentColor');
                    const path = document.createElementNS('http://www.w3.org/2000/svg', 'path');
                    path.setAttribute('d', 'M16.5 6v11.5A4.5 4.5 0 0 1 7.5 17.5V5a3 3 0 0 1 6 0v10.5a1.5 1.5 0 0 1-3 0V6H9v9.5a3 3 0 0 0 6 0V5a4.5 4.5 0 0 0-9 0v12.5a6 6 0 0 0 12 0V6h-1.5z');
                    svg.appendChild(path);
                    const span = document.createElement('span');
                    span.textContent = 'Unduh Lampiran';
                    link.appendChild(svg); link.appendChild(span);
                    wrap.appendChild(link);
                });
                wrap.appendChild(img);
                div.insertBefore(wrap, timeEl);
            });
        }

        return div;
    }

    // ── Show / hide state panels ──────────────────────────────────────────────
    function showList() {
        msgLoading.style.display = 'none';
        msgEmpty.style.display   = 'none';
        msgList.style.display    = 'flex';
    }
    function showEmpty() {
        msgLoading.style.display = 'none';
        msgList.style.display    = 'none';
        msgEmpty.style.display   = 'flex';
    }

    // ── Append pesan baru ke bawah ────────────────────────────────────────────
    function appendMessages(msgs, scrollToBottom) {
        msgs.forEach(function (m) {
            if (document.querySelector('[data-id="' + m.id + '"]')) return;
            msgList.appendChild(renderMsg(m));
            if (m.id > lastMsgId)  lastMsgId  = m.id;
            if (m.id < firstMsgId) firstMsgId = m.id;
        });
        rebuildSeparators();
        if (scrollToBottom) msgList.scrollTop = msgList.scrollHeight;
    }

    function isNearBottom() {
        return (msgList.scrollHeight - msgList.scrollTop - msgList.clientHeight) < 100;
    }

    // ── Send handler ──────────────────────────────────────────────────────────
    async function doSend() {
        const body = msgInput.value.trim();
        if (!body && !pendingFile) return;

        const fileToSend = pendingFile;
        msgInput.value = '';
        msgInput.style.height = 'auto';
        sendBtn.disabled = true;
        if (fileToSend) clearAttachPreview();

        // Hentikan typing indicator milik kita
        if (isTyping) { isTyping = false; notifyTyping(false); }
        clearTimeout(typingTimer);

        try {
            let attachmentIds = [];
            if (fileToSend) attachmentIds = [await uploadFile(fileToSend)];
            await sendMessage(body, attachmentIds);
            const newMsgs = await fetchMessages(lastMsgId);
            if (newMsgs.length > 0) { showList(); appendMessages(newMsgs, true); }
        } catch (e) {
            if (!fileToSend) msgInput.value = body;
            alert('Gagal mengirim: ' + e.message);
        } finally {
            sendBtn.disabled = false;
            msgInput.focus();
        }
    }

    // ── Typing indicator ──────────────────────────────────────────────────────
    async function notifyTyping(typing) {
        try {
            await callKw('discuss.channel', 'notify_typing', [[CHANNEL_ID]], {
                is_typing: typing,
            });
        } catch (_) {}
    }

    async function checkTypingMembers() {
        try {
            const results = await callKw('discuss.channel', 'read', [[CHANNEL_ID]], {
                fields: ['typing_member_ids'],
            });
            const typingIds = results && results[0] && results[0].typing_member_ids;
            if (!typingIds || typingIds.length === 0) {
                typingIndicator.style.display = 'none';
                return;
            }
            const members = await callKw('discuss.channel.member', 'read', [typingIds], {
                fields: ['partner_id'],
            });
            const names = members
                .filter(function (m) { return m.partner_id && m.partner_id[0] !== MY_PARTNER_ID; })
                .map(function (m) { return m.partner_id[1]; });

            if (names.length > 0) {
                typingText.textContent = names.join(', ') + ' sedang mengetik...';
                typingIndicator.style.display = 'flex';
            } else {
                typingIndicator.style.display = 'none';
            }
        } catch (_) {
            typingIndicator.style.display = 'none';
        }
    }

    // ── Init ──────────────────────────────────────────────────────────────────
    async function init() {
        try {
            const msgs = await fetchMessages(0);
            if (msgs.length === 0) {
                showEmpty();
                hasMoreMessages = false;
            } else {
                showList();
                appendMessages(msgs, true);
                if (msgs.length < 50) hasMoreMessages = false;
            }
        } catch (e) {
            msgLoading.innerHTML = '<span class="err">Gagal memuat pesan. Coba refresh.</span>';
        }

        // Polling: pesan baru + typing status setiap 3 detik
        setInterval(async function () {
            if (lastMsgId > 0) {
                try {
                    const newMsgs = await fetchMessages(lastMsgId);
                    if (newMsgs.length > 0) {
                        const atBottom = isNearBottom();
                        showList();
                        appendMessages(newMsgs, atBottom);
                    }
                } catch (_) {}
            }
            checkTypingMembers();
        }, 3000);
    }

    // ── Video call — navigate ke Odoo discuss (X-Frame-Options blokir iframe) ─
    const videoCallBtn = document.getElementById('videocall-btn');

    videoCallBtn.addEventListener('click', function () {
        // Simpan URL chat agar bisa dipakai tombol back di halaman discuss
        sessionStorage.setItem('returnToChatUrl', window.location.href);
        window.location.href = '/odoo/discuss/channel-' + CHANNEL_ID;
    });

    // ── Event listeners ───────────────────────────────────────────────────────
    sendBtn.addEventListener('click', doSend);

    msgInput.addEventListener('keydown', function (e) {
        if (e.key === 'Enter' && !e.shiftKey) { e.preventDefault(); doSend(); }
    });

    msgInput.addEventListener('input', function () {
        // Auto-grow
        this.style.height = 'auto';
        this.style.height = Math.min(this.scrollHeight, 90) + 'px';
        // Typing signal ke Odoo
        if (!isTyping) { isTyping = true; notifyTyping(true); }
        clearTimeout(typingTimer);
        typingTimer = setTimeout(function () { isTyping = false; notifyTyping(false); }, 2000);
    });

    attachBtn.addEventListener('click', function () { fileInput.click(); });
    fileInput.addEventListener('change', function () {
        const file = this.files && this.files[0];
        if (file) showAttachPreview(file);
    });
    attachRemove.addEventListener('click', clearAttachPreview);

    msgList.addEventListener('scroll', function () {
        scrollBtn.classList.toggle('visible', !isNearBottom());
        if (msgList.scrollTop < 80) loadMoreMessages();
    });

    scrollBtn.addEventListener('click', function () {
        msgList.scrollTo({ top: msgList.scrollHeight, behavior: 'smooth' });
    });

    init();
})();
