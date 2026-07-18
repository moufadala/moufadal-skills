# Tailscale + VPS VPN/proxy routing patterns (2026-07-01)

Session learning from a user question about keeping an Android phone connected to Tailscale as a residential/mobile proxy for Hermes/SearXNG while also browsing geo-blocked sites via NordVPN.

## Durable findings

- Android's official VPN model is a hard constraint: Tailscale Android and NordVPN Android both use the Android VPN slot. Running both simultaneously is usually not viable; official Tailscale docs say Android/iOS generally allow only one active VPN at a time.
- Tailscale Android app-based split tunneling can exclude apps from Tailscale, but excluded apps go out through the normal local network, not through a commercial VPN country unless another compatible routing layer exists.
- A VPS can act as a routing hub without changing the VPS global default route: run a VPN client in an isolated container (e.g. Gluetun + NordVPN) and expose only a private HTTP/SOCKS proxy or Tailscale-only service.
- Gluetun supports NordVPN via service credentials/OpenVPN or WireGuard private key and has built-in HTTP/SOCKS proxy options. Do not put NordVPN on the whole VPS unless explicitly accepted; it can break SSH/Docker/Hermes like a global exit-node mistake.
- Community patterns exist for `Tailscale + Gluetun + NordVPN` where Tailscale joins Gluetun's network namespace and advertises an exit node, or where a proxy is bound only to the Tailscale address. Treat GitHub/community repos as patterns to adapt, not turnkey production without testing.
- Chrome Android is a poor fit for per-browser proxy configuration. A dedicated browser/profile that supports proxy settings/extensions (Firefox/Kiwi/other) is more plausible than trying to make Chrome Android use a proxy selectively.
- Remote browser-in-browser is possible (noVNC/Kasm/etc.) but should not be the first recommendation for mobile adult/video browsing: it is less clear to users and may be less fluid than a direct mobile browser using a proxy.

## Recommended architecture for this class of problem

Keep these flows separate:

1. Hermes/SearXNG residential path:
   - `Hermes/VPS service -> existing Tailscale userspace/mobile proxy path -> Android phone/mobile IP -> Internet`
   - Keep watchdog silent-on-success and alert-only-on-failure.

2. User browsing geo-unblocked path:
   - `Android dedicated browser -> Tailscale private address of VPS proxy -> isolated Gluetun/NordVPN container -> USA/other country -> website`
   - Do not install NordVPN Android if the phone must stay connected to Tailscale for Hermes.
   - Do not activate a global VPN/exit-node on the VPS.

## Explanation pitfall

When explaining this to a non-expert user, do not say only “open a remote browser” or “navigate as if in the USA”. State explicitly:

- which app the user opens on the phone;
- whether it is local browsing with a proxy or a remote desktop/browser stream;
- which network hop carries traffic: phone -> Tailscale -> VPS -> VPN container -> Internet;
- what remains unchanged for Hermes/SearXNG;
- what is verified vs what still needs a live test.

## Minimal acceptance test before production

- Direct VPS IP remains unchanged and SSH/Docker/Hermes unaffected.
- Gluetun/NordVPN container reports a non-VPS exit IP in the selected country.
- Proxy bound only to Tailscale/private interface; public VPS IP port scan is closed/filtered.
- Android dedicated browser can reach `https://api.ipify.org` through the proxy and returns the NordVPN country/IP.
- SearXNG/Hermes residential path still returns the phone/mobile exit IP and its watchdog stays silent on OK.
