# effects.md — copy-and-adapt snippets (Layer 1, strict-CSP)

All snippets are self-contained: plain CSS/JS, no libraries, no CDN. Adapt colors
via CSS custom properties. Keep motion slow (long durations, small distances).

## Palette scaffold (put at the top)

```css
:root{
  --bg:#0a0b12; --fg:#e8eaf2; --muted:#9aa0b4;
  --accent:#6ea8fe; --accent2:#b088ff; --card:rgba(255,255,255,.04);
  --line:rgba(255,255,255,.10);
}
@media (prefers-color-scheme: light){
  :root{ --bg:#f7f8fc; --fg:#12141c; --muted:#5a6072; --card:rgba(0,0,0,.03); --line:rgba(0,0,0,.10); }
}
*{box-sizing:border-box} html,body{margin:0} body{overflow-x:hidden}
body{background:var(--bg); color:var(--fg);
  font-family:system-ui,-apple-system,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
  line-height:1.5; -webkit-font-smoothing:antialiased}
h1{font-size:clamp(2.2rem,6vw,4.5rem); line-height:1.05; letter-spacing:-.02em}
.container{max-width:1100px; margin:0 auto; padding:0 clamp(16px,4vw,40px)}
```

## Animated aurora hero

```html
<section class="hero"><div class="aurora"></div>
  <div class="container"><h1 class="shimmer">Your headline</h1></div>
</section>
```
```css
.hero{position:relative; overflow:hidden; min-height:82vh; display:grid; place-items:center}
.aurora{position:absolute; inset:-20%; z-index:0; filter:blur(70px); opacity:.7}
.aurora::before,.aurora::after{content:""; position:absolute; width:55vw; height:55vw; border-radius:50%}
.aurora::before{background:radial-gradient(circle,var(--accent),transparent 60%); top:-10%; left:-5%; animation:drift 34s ease-in-out infinite}
.aurora::after{background:radial-gradient(circle,var(--accent2),transparent 60%); bottom:-15%; right:-5%; animation:drift 28s ease-in-out infinite reverse}
.hero .container{position:relative; z-index:1}
@keyframes drift{0%,100%{transform:translate(0,0) scale(1)} 50%{transform:translate(6%,4%) scale(1.12)}}
@media (prefers-reduced-motion:reduce){.aurora::before,.aurora::after{animation:none}}
```

## Gradient-text shimmer

```css
.shimmer{background:linear-gradient(100deg,var(--fg) 30%,var(--accent) 50%,var(--fg) 70%);
  background-size:200% auto; -webkit-background-clip:text; background-clip:text; color:transparent;
  animation:sheen 6s linear infinite}
@keyframes sheen{to{background-position:200% center}}
@media (prefers-reduced-motion:reduce){.shimmer{animation:none}}
```

## Scroll reveal (visible without JS, enhanced with JS)

```css
.reveal{opacity:1; transform:none; transition:opacity .7s ease, transform .7s ease}
.js .reveal{opacity:0; transform:translateY(24px)}
.js .reveal.in{opacity:1; transform:none}
```
```html
<script>
document.documentElement.classList.add('js');
const io=new IntersectionObserver((es)=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.15});
document.querySelectorAll('.reveal').forEach(el=>io.observe(el));
</script>
```
Note: adding `js` class means if JS never runs, `.reveal` stays visible (graceful).

## Glass card with hover lift + glow

```css
.card{background:var(--card); border:1px solid var(--line); border-radius:18px; padding:24px;
  backdrop-filter:blur(12px); transition:transform .3s ease, box-shadow .3s ease}
.card:hover{transform:translateY(-4px); box-shadow:0 18px 50px -12px color-mix(in srgb,var(--accent) 45%,transparent)}
```

## Bento grid

```css
.bento{display:grid; grid-template-columns:repeat(4,1fr); gap:16px}
.bento .b-lg{grid-column:span 2; grid-row:span 2}
.bento .b-wide{grid-column:span 2}
@media (max-width:720px){.bento{grid-template-columns:repeat(2,1fr)} .bento .b-lg{grid-column:span 2}}
```

## Marquee (pause on hover, reduced-motion safe)

```css
.marquee{overflow:hidden; -webkit-mask:linear-gradient(90deg,transparent,#000 8%,#000 92%,transparent)}
.marquee__track{display:flex; gap:48px; width:max-content; animation:scroll 28s linear infinite}
.marquee:hover .marquee__track{animation-play-state:paused}
@keyframes scroll{to{transform:translateX(-50%)}}
@media (prefers-reduced-motion:reduce){.marquee__track{animation:none}}
```
Duplicate the item list twice inside `.marquee__track` so `-50%` loops seamlessly.

## Count-up numbers

```html
<script>
const easeOut=t=>1-Math.pow(1-t,3);
document.querySelectorAll('[data-count]').forEach(el=>{
  const end=+el.dataset.count, dur=1400; let t0=null;
  const io=new IntersectionObserver(([e])=>{ if(!e.isIntersecting) return; io.disconnect();
    requestAnimationFrame(function step(ts){ t0??=ts; const p=Math.min((ts-t0)/dur,1);
      el.textContent=Math.round(end*easeOut(p)).toLocaleString(); if(p<1) requestAnimationFrame(step); });
  },{threshold:.5}); io.observe(el);
});
</script>
```

## Inline SVG ornament (example: soft arc divider)

```html
<svg viewBox="0 0 1200 60" preserveAspectRatio="none" style="display:block;width:100%;height:60px">
  <path d="M0,40 C300,10 900,10 1200,40 L1200,60 L0,60 Z" fill="var(--card)"/>
</svg>
```

## Reduced-motion catch-all

```css
@media (prefers-reduced-motion:reduce){*{animation:none!important; transition-duration:.01ms!important}}
```
