var t="post"
/*e={
    "action": {
        "goodsCatalogueId": 6
    }
}*/
HEX_CHARS=[
    "0",
    "1",
    "2",
    "3",
    "4",
    "5",
    "6",
    "7",
    "8",
    "9",
    "a",
    "b",
    "c",
    "d",
    "e",
    "f"
]
EXTRA=[
    128,
    32768,
    8388608,
    -2147483648
]
var buffer = new ArrayBuffer(68);
buffer8 = new Uint8Array(buffer)
blocks = new Uint32Array(buffer)

var ARRAY_BUFFER=true
function Md5(t) {
    if (t)
        blocks[0] = blocks[16] = blocks[1] = blocks[2] = blocks[3] = blocks[4] = blocks[5] = blocks[6] = blocks[7] = blocks[8] = blocks[9] = blocks[10] = blocks[11] = blocks[12] = blocks[13] = blocks[14] = blocks[15] = 0,
            this.blocks = blocks,
            this.buffer8 = buffer8;
    else if (ARRAY_BUFFER) {
        var e = new ArrayBuffer(68);
        this.buffer8 = new Uint8Array(e),
            this.blocks = new Uint32Array(e)
    } else
        this.blocks = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0];
    this.h0 = this.h1 = this.h2 = this.h3 = this.start = this.bytes = this.hBytes = 0,
        this.finalized = this.hashed = !1,
        this.first = !0
}
Md5.prototype.finalize = function() {
    if (!this.finalized) {
        this.finalized = !0;
        var t = this.blocks
            , e = this.lastByteIndex;
        t[e >> 2] |= EXTRA[3 & e],
        e >= 56 && (this.hashed || this.hash(),
            t[0] = t[16],
            t[16] = t[1] = t[2] = t[3] = t[4] = t[5] = t[6] = t[7] = t[8] = t[9] = t[10] = t[11] = t[12] = t[13] = t[14] = t[15] = 0),
            t[14] = this.bytes << 3,
            t[15] = this.hBytes << 3 | this.bytes >>> 29,
            this.hash()
    }
}
Md5.prototype.hex = function() {
    this.finalize();
    var t = this.h0
        , e = this.h1
        , r = this.h2
        , n = this.h3;
    return HEX_CHARS[t >> 4 & 15] + HEX_CHARS[15 & t] + HEX_CHARS[t >> 12 & 15] + HEX_CHARS[t >> 8 & 15] + HEX_CHARS[t >> 20 & 15] + HEX_CHARS[t >> 16 & 15] + HEX_CHARS[t >> 28 & 15] + HEX_CHARS[t >> 24 & 15] + HEX_CHARS[e >> 4 & 15] + HEX_CHARS[15 & e] + HEX_CHARS[e >> 12 & 15] + HEX_CHARS[e >> 8 & 15] + HEX_CHARS[e >> 20 & 15] + HEX_CHARS[e >> 16 & 15] + HEX_CHARS[e >> 28 & 15] + HEX_CHARS[e >> 24 & 15] + HEX_CHARS[r >> 4 & 15] + HEX_CHARS[15 & r] + HEX_CHARS[r >> 12 & 15] + HEX_CHARS[r >> 8 & 15] + HEX_CHARS[r >> 20 & 15] + HEX_CHARS[r >> 16 & 15] + HEX_CHARS[r >> 28 & 15] + HEX_CHARS[r >> 24 & 15] + HEX_CHARS[n >> 4 & 15] + HEX_CHARS[15 & n] + HEX_CHARS[n >> 12 & 15] + HEX_CHARS[n >> 8 & 15] + HEX_CHARS[n >> 20 & 15] + HEX_CHARS[n >> 16 & 15] + HEX_CHARS[n >> 28 & 15] + HEX_CHARS[n >> 24 & 15]
}
Md5.prototype.hash = function() {
    var t, e, r, n, i, o, s = this.blocks;
    this.first ? e = ((e = ((t = ((t = s[0] - 680876937) << 7 | t >>> 25) - 271733879 << 0) ^ (r = ((r = (-271733879 ^ (n = ((n = (-1732584194 ^ 2004318071 & t) + s[1] - 117830708) << 12 | n >>> 20) + t << 0) & (-271733879 ^ t)) + s[2] - 1126478375) << 17 | r >>> 15) + n << 0) & (n ^ t)) + s[3] - 1316259209) << 22 | e >>> 10) + r << 0 : (t = this.h0,
        e = this.h1,
        r = this.h2,
        e = ((e += ((t = ((t += ((n = this.h3) ^ e & (r ^ n)) + s[0] - 680876936) << 7 | t >>> 25) + e << 0) ^ (r = ((r += (e ^ (n = ((n += (r ^ t & (e ^ r)) + s[1] - 389564586) << 12 | n >>> 20) + t << 0) & (t ^ e)) + s[2] + 606105819) << 17 | r >>> 15) + n << 0) & (n ^ t)) + s[3] - 1044525330) << 22 | e >>> 10) + r << 0),
        e = ((e += ((t = ((t += (n ^ e & (r ^ n)) + s[4] - 176418897) << 7 | t >>> 25) + e << 0) ^ (r = ((r += (e ^ (n = ((n += (r ^ t & (e ^ r)) + s[5] + 1200080426) << 12 | n >>> 20) + t << 0) & (t ^ e)) + s[6] - 1473231341) << 17 | r >>> 15) + n << 0) & (n ^ t)) + s[7] - 45705983) << 22 | e >>> 10) + r << 0,
        e = ((e += ((t = ((t += (n ^ e & (r ^ n)) + s[8] + 1770035416) << 7 | t >>> 25) + e << 0) ^ (r = ((r += (e ^ (n = ((n += (r ^ t & (e ^ r)) + s[9] - 1958414417) << 12 | n >>> 20) + t << 0) & (t ^ e)) + s[10] - 42063) << 17 | r >>> 15) + n << 0) & (n ^ t)) + s[11] - 1990404162) << 22 | e >>> 10) + r << 0,
        e = ((e += ((t = ((t += (n ^ e & (r ^ n)) + s[12] + 1804603682) << 7 | t >>> 25) + e << 0) ^ (r = ((r += (e ^ (n = ((n += (r ^ t & (e ^ r)) + s[13] - 40341101) << 12 | n >>> 20) + t << 0) & (t ^ e)) + s[14] - 1502002290) << 17 | r >>> 15) + n << 0) & (n ^ t)) + s[15] + 1236535329) << 22 | e >>> 10) + r << 0,
        e = ((e += ((n = ((n += (e ^ r & ((t = ((t += (r ^ n & (e ^ r)) + s[1] - 165796510) << 5 | t >>> 27) + e << 0) ^ e)) + s[6] - 1069501632) << 9 | n >>> 23) + t << 0) ^ t & ((r = ((r += (t ^ e & (n ^ t)) + s[11] + 643717713) << 14 | r >>> 18) + n << 0) ^ n)) + s[0] - 373897302) << 20 | e >>> 12) + r << 0,
        e = ((e += ((n = ((n += (e ^ r & ((t = ((t += (r ^ n & (e ^ r)) + s[5] - 701558691) << 5 | t >>> 27) + e << 0) ^ e)) + s[10] + 38016083) << 9 | n >>> 23) + t << 0) ^ t & ((r = ((r += (t ^ e & (n ^ t)) + s[15] - 660478335) << 14 | r >>> 18) + n << 0) ^ n)) + s[4] - 405537848) << 20 | e >>> 12) + r << 0,
        e = ((e += ((n = ((n += (e ^ r & ((t = ((t += (r ^ n & (e ^ r)) + s[9] + 568446438) << 5 | t >>> 27) + e << 0) ^ e)) + s[14] - 1019803690) << 9 | n >>> 23) + t << 0) ^ t & ((r = ((r += (t ^ e & (n ^ t)) + s[3] - 187363961) << 14 | r >>> 18) + n << 0) ^ n)) + s[8] + 1163531501) << 20 | e >>> 12) + r << 0,
        e = ((e += ((n = ((n += (e ^ r & ((t = ((t += (r ^ n & (e ^ r)) + s[13] - 1444681467) << 5 | t >>> 27) + e << 0) ^ e)) + s[2] - 51403784) << 9 | n >>> 23) + t << 0) ^ t & ((r = ((r += (t ^ e & (n ^ t)) + s[7] + 1735328473) << 14 | r >>> 18) + n << 0) ^ n)) + s[12] - 1926607734) << 20 | e >>> 12) + r << 0,
        e = ((e += ((o = (n = ((n += ((i = e ^ r) ^ (t = ((t += (i ^ n) + s[5] - 378558) << 4 | t >>> 28) + e << 0)) + s[8] - 2022574463) << 11 | n >>> 21) + t << 0) ^ t) ^ (r = ((r += (o ^ e) + s[11] + 1839030562) << 16 | r >>> 16) + n << 0)) + s[14] - 35309556) << 23 | e >>> 9) + r << 0,
        e = ((e += ((o = (n = ((n += ((i = e ^ r) ^ (t = ((t += (i ^ n) + s[1] - 1530992060) << 4 | t >>> 28) + e << 0)) + s[4] + 1272893353) << 11 | n >>> 21) + t << 0) ^ t) ^ (r = ((r += (o ^ e) + s[7] - 155497632) << 16 | r >>> 16) + n << 0)) + s[10] - 1094730640) << 23 | e >>> 9) + r << 0,
        e = ((e += ((o = (n = ((n += ((i = e ^ r) ^ (t = ((t += (i ^ n) + s[13] + 681279174) << 4 | t >>> 28) + e << 0)) + s[0] - 358537222) << 11 | n >>> 21) + t << 0) ^ t) ^ (r = ((r += (o ^ e) + s[3] - 722521979) << 16 | r >>> 16) + n << 0)) + s[6] + 76029189) << 23 | e >>> 9) + r << 0,
        e = ((e += ((o = (n = ((n += ((i = e ^ r) ^ (t = ((t += (i ^ n) + s[9] - 640364487) << 4 | t >>> 28) + e << 0)) + s[12] - 421815835) << 11 | n >>> 21) + t << 0) ^ t) ^ (r = ((r += (o ^ e) + s[15] + 530742520) << 16 | r >>> 16) + n << 0)) + s[2] - 995338651) << 23 | e >>> 9) + r << 0,
        e = ((e += ((n = ((n += (e ^ ((t = ((t += (r ^ (e | ~n)) + s[0] - 198630844) << 6 | t >>> 26) + e << 0) | ~r)) + s[7] + 1126891415) << 10 | n >>> 22) + t << 0) ^ ((r = ((r += (t ^ (n | ~e)) + s[14] - 1416354905) << 15 | r >>> 17) + n << 0) | ~t)) + s[5] - 57434055) << 21 | e >>> 11) + r << 0,
        e = ((e += ((n = ((n += (e ^ ((t = ((t += (r ^ (e | ~n)) + s[12] + 1700485571) << 6 | t >>> 26) + e << 0) | ~r)) + s[3] - 1894986606) << 10 | n >>> 22) + t << 0) ^ ((r = ((r += (t ^ (n | ~e)) + s[10] - 1051523) << 15 | r >>> 17) + n << 0) | ~t)) + s[1] - 2054922799) << 21 | e >>> 11) + r << 0,
        e = ((e += ((n = ((n += (e ^ ((t = ((t += (r ^ (e | ~n)) + s[8] + 1873313359) << 6 | t >>> 26) + e << 0) | ~r)) + s[15] - 30611744) << 10 | n >>> 22) + t << 0) ^ ((r = ((r += (t ^ (n | ~e)) + s[6] - 1560198380) << 15 | r >>> 17) + n << 0) | ~t)) + s[13] + 1309151649) << 21 | e >>> 11) + r << 0,
        e = ((e += ((n = ((n += (e ^ ((t = ((t += (r ^ (e | ~n)) + s[4] - 145523070) << 6 | t >>> 26) + e << 0) | ~r)) + s[11] - 1120210379) << 10 | n >>> 22) + t << 0) ^ ((r = ((r += (t ^ (n | ~e)) + s[2] + 718787259) << 15 | r >>> 17) + n << 0) | ~t)) + s[9] - 343485551) << 21 | e >>> 11) + r << 0,
        this.first ? (this.h0 = t + 1732584193 << 0,
            this.h1 = e - 271733879 << 0,
            this.h2 = r - 1732584194 << 0,
            this.h3 = n + 271733878 << 0,
            this.first = !1) : (this.h0 = this.h0 + t << 0,
            this.h1 = this.h1 + e << 0,
            this.h2 = this.h2 + r << 0,
            this.h3 = this.h3 + n << 0)
}
Md5.prototype.update = function(t) {
    if (!this.finalized) {
        var e, r = typeof t;
        if ("string" !== r) {
            if ("object" !== r)
                throw ERROR;
            if (null === t)
                throw ERROR;
            if (ARRAY_BUFFER && t.constructor === ArrayBuffer)
                t = new Uint8Array(t);
            else if (!(Array.isArray(t) || ARRAY_BUFFER && ArrayBuffer.isView(t)))
                throw ERROR;
            e = !0
        }
        for (var n, i, o = 0, s = t.length, f = this.blocks, a = this.buffer8; o < s;) {
            if (this.hashed && (this.hashed = !1,
                f[0] = f[16],
                f[16] = f[1] = f[2] = f[3] = f[4] = f[5] = f[6] = f[7] = f[8] = f[9] = f[10] = f[11] = f[12] = f[13] = f[14] = f[15] = 0),
                e)
                if (ARRAY_BUFFER)
                    for (i = this.start; o < s && i < 64; ++o)
                        a[i++] = t[o];
                else
                    for (i = this.start; o < s && i < 64; ++o)
                        f[i >> 2] |= t[o] << SHIFT[3 & i++];
            else if (ARRAY_BUFFER)
                for (i = this.start; o < s && i < 64; ++o)
                    (n = t.charCodeAt(o)) < 128 ? a[i++] = n : n < 2048 ? (a[i++] = 192 | n >> 6,
                        a[i++] = 128 | 63 & n) : n < 55296 || n >= 57344 ? (a[i++] = 224 | n >> 12,
                        a[i++] = 128 | n >> 6 & 63,
                        a[i++] = 128 | 63 & n) : (n = 65536 + ((1023 & n) << 10 | 1023 & t.charCodeAt(++o)),
                        a[i++] = 240 | n >> 18,
                        a[i++] = 128 | n >> 12 & 63,
                        a[i++] = 128 | n >> 6 & 63,
                        a[i++] = 128 | 63 & n);
            else
                for (i = this.start; o < s && i < 64; ++o)
                    (n = t.charCodeAt(o)) < 128 ? f[i >> 2] |= n << SHIFT[3 & i++] : n < 2048 ? (f[i >> 2] |= (192 | n >> 6) << SHIFT[3 & i++],
                        f[i >> 2] |= (128 | 63 & n) << SHIFT[3 & i++]) : n < 55296 || n >= 57344 ? (f[i >> 2] |= (224 | n >> 12) << SHIFT[3 & i++],
                        f[i >> 2] |= (128 | n >> 6 & 63) << SHIFT[3 & i++],
                        f[i >> 2] |= (128 | 63 & n) << SHIFT[3 & i++]) : (n = 65536 + ((1023 & n) << 10 | 1023 & t.charCodeAt(++o)),
                        f[i >> 2] |= (240 | n >> 18) << SHIFT[3 & i++],
                        f[i >> 2] |= (128 | n >> 12 & 63) << SHIFT[3 & i++],
                        f[i >> 2] |= (128 | n >> 6 & 63) << SHIFT[3 & i++],
                        f[i >> 2] |= (128 | 63 & n) << SHIFT[3 & i++]);
            this.lastByteIndex = i,
                this.bytes += i - this.start,
                i >= 64 ? (this.start = i - 64,
                    this.hash(),
                    this.hashed = !0) : this.start = i
        }
        return this.bytes > 4294967295 && (this.hBytes += this.bytes / 4294967296 << 0,
            this.bytes = this.bytes % 4294967296),
            this
    }
}
var l= function(e) {
    return new Md5(!0).update(e)["hex"]()
}
var d = function(e, t) {
    for (var r, n = t ? e : p({}, e), o = (new Date).getTime(), u = "", i = new Array(0,1,2,3,4,5,6,7,8,9), a = 0; a < 6; a++) {
        u += i[Math.floor(9 * Math.random())]
    }
    var n=JSON.parse(e)
    r = Number(u);
    var s = [];
    if (t)
        s.push("PZTimestamp=" + o + "&Random=" + r + "&2147483647=" + encodeURIComponent(JSON.stringify(n)));
    else {
        n.PZTimestamp = o,
            n.Random = r;
        var c = Object.keys(n).sort();
        c = c.sort((function(e, t) {
                return e - t
            }
        ));
        var d = {};
        for (var m in c)
            n[c[m]]instanceof Array && n[c[m]]instanceof Object && (n[c[m]] = JSON.stringify(n[c[m]])),
                d[c[m]] = encodeURIComponent(n[c[m]]);
        for (var b in n = d)
            (t || "null" !== n[b] && "undefined" !== n[b]) && s.push(b + "=" + n[b])
    }
    var f = s.join("&") + "&accessKey=3qXyB7uf";
    return f = f.replace(/[(]/g, "%28").replace(/[)]/g, "%29").replace(/[']/g, "%27").replace(/[*]/g, "%2A").replace(/[~]/g, "%7E").replace(/[!！]/g, "%21"),
        {
            Timestamp: o,
            strMd5: l(f),
            Random: r
        }
};

function myJiaMi(e) {
    t=d(e, "post")
    return t;
}
console.log(myJiaMi('{"action":{"keywords":[],"merchantMark":null,"goodsCatalogueId":6,"gameId":8},"sort":"createTime","order":"DESC","page":1,"pageSize":100}'))