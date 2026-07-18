# Flight scraping: Amadeus / Akamai investigation pattern

Session-derived reference for airline scraping flows where a public airline site hands off to Amadeus (`plnext`, `Override.action`, `Preload.action`) and the final Amadeus host returns an anti-bot page such as **Pardon Our Interruption**.

## Pattern observed

- Airline CMS/Drupal form can be accessible and POSTable.
- A valid search POST may generate a dynamic redirect like:
  `https://<airline-amadeus-host>/plnext/<site>/Override.action?...ENC=...`
- The `ENC` generation can be solved while the final Amadeus/Akamai hop remains blocked.
- Treat this as two separate problems:
  1. **Airline front-end form → dynamic ENC**
  2. **Amadeus/Akamai session acceptance → result page/prices**

## Baseline script phases

1. GET airline search page with `curl_cffi` session and browser impersonation.
2. Parse all hidden inputs/selects from the search form.
3. POST the search with realistic headers and `allow_redirects=False`.
4. Save: status, `Location`, Set-Cookie, request headers, response headers, body snippet.
5. Follow the Amadeus URL manually, not with blind redirect following.
6. If blocked, vary one factor at a time.

## Headers/cookies to compare

- `Accept`, `Accept-Language`, `Accept-Encoding`
- `Referer`, `Origin`
- `Sec-Fetch-Dest`, `Sec-Fetch-Mode`, `Sec-Fetch-Site`, `Sec-Fetch-User`
- `Upgrade-Insecure-Requests`
- UA exactly matching the TLS/browser impersonation
- Akamai/Bot Manager cookies if present: `bm_mi`, `bm_sv`, `_abck`, `bm_sz`, `ak_bmsc`

## Experiments before declaring proxy/unlocker required

- Multiple `curl_cffi` impersonations available in the installed version.
- Starting URL variants (`www`, `re`, booking subdomain) and priming the final Amadeus host.
- Session-persistent cookies across GET → POST → Amadeus follow.
- Opening the generated `Override.action?...ENC=...` in a real browser via CDP/nodriver/profile after generating it by HTTP.
- Network comparison between HTTP client and browser for the final hop.

## Evidence required for a hard-block conclusion

Do not conclude “requires residential proxy/mobile/unlocker” without files showing:

- exact final URL and status,
- response title/body snippet,
- cookies present/absent,
- headers used,
- screenshots if browser was used,
- list of tested impersonations/browser approaches.

## Useful search queries

- `Amadeus plnext Override.action ENC scraping`
- `Amadeus FlexPricerAvailability Override.action ENC`
- `Akamai Pardon Our Interruption curl_cffi`
- `curl_cffi Akamai bm_mi bm_sv _abck bm_sz`
- `Akamai Amadeus travel scraping Override.action`
- `nodriver Akamai Pardon Our Interruption`
