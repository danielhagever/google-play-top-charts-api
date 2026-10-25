# Google Play Top Charts API: Top Free, Top Grossing and Trending apps by country

Google publishes no API for its Play Store top charts. This is a working one: Top Free, Top
Paid, Top Grossing, Trending and Top New Free, for apps and games, in 130 countries and 54
categories, with rank, rating, installs, price and developer, and the rank change since your
last run. No Google account, no API key from Google.

This repo is the quick start for the hosted
[**Google Play Top Charts Scraper**](https://apify.com/glitchbound/google-play-charts-scraper)
on Apify: one HTTP call from the shell, a standard-library Python script that writes a CSV,
and the setup for using it as a tool in Claude, ChatGPT or Cursor.

- [Quick start: one curl](#quick-start-one-curl)
- [Quick start: Python](#quick-start-python)
- [Use it from an AI agent (MCP)](#use-it-from-an-ai-agent-mcp)
- [Input](#input) · [Output](#output)
- [Tracking rank over time](#tracking-rank-over-time)
- [FAQ](#faq)

## Quick start: one curl

Get a free Apify API token at
[console.apify.com/settings/integrations](https://console.apify.com/settings/integrations),
then:

```bash
export APIFY_TOKEN=apify_api_...
curl -s -X POST \
  -H "Authorization: Bearer $APIFY_TOKEN" -H "Content-Type: application/json" \
  -d '{"countries": ["us"], "charts": ["top-free", "trending"], "categories": ["all-apps"], "limit": 10}' \
  "https://api.apify.com/v2/acts/glitchbound~google-play-charts-scraper/run-sync-get-dataset-items"
```

The response is a JSON array, one object per charting app.

## Quick start: Python

[`example.py`](example.py) uses only the standard library and writes a CSV:

```bash
python3 example.py --country us --chart top-free --chart trending --limit 3
python3 example.py inputs/games-six-markets.json
```

A real run of the first command:

```
6 chart rows written to charts.csv
  US top-free #1: Muse from Meta (Meta Platforms, Inc.)
  US top-free #2: ChatGPT (OpenAI)
  US top-free #3: TikTok - Videos, Shop & LIVE (TikTok Pte. Ltd.)
  US trending #1: AR Character: Funny Cam Filter (Jade-Core)
  US trending #2: Hark Pro (Hark Labs Inc.)
```

## Use it from an AI agent (MCP)

Add this as a connector in Claude or ChatGPT:

```
https://mcp.apify.com?tools=glitchbound/google-play-charts-scraper
```

In Cursor or VS Code, the same address goes in `mcp.json`:

```json
{ "mcpServers": { "apify": { "url": "https://mcp.apify.com?tools=glitchbound/google-play-charts-scraper" } } }
```

The first call asks you to sign in to Apify or takes an API token. Then "which finance apps
are trending in Brazil this week?" is one tool call.

## Input

| Field | What it does |
|---|---|
| `countries` | Two-letter codes, e.g. `us`, `gb`, `jp`. 130 markets; a code Google does not serve as a market is refused rather than answered with another country's chart. |
| `charts` | `top-free`, `top-paid`, `top-grossing`, `trending`, `top-new-free` |
| `categories` | `all-apps`, `all-games`, or one of 52 more such as `finance`, `shopping`, `education` and every games genre |
| `limit` | Apps per chart, up to 200, which is all Google serves |
| `includeDetails` | Also read each app's own Play page: exact installs, rating count and histogram, release and update dates, version, developer email and website |
| `trackRankChanges` | On by default: every row says where the app stood the last time your account read that chart |
| `maxItems` | Ceiling for the whole run |

Ready-made inputs are in [`inputs/`](inputs), including six markets' game charts in one run.

## Output

One row per charting app. Two real rows from the run above are in
[`sample-output.json`](sample-output.json); one of them, abridged:

```json
{
  "rank": 2,
  "country": "US",
  "chart": "top-free",
  "category": "all-apps",
  "appId": "com.openai.chatgpt",
  "title": "ChatGPT",
  "developer": "OpenAI",
  "genre": "Productivity",
  "rating": 4.78,
  "installs": "1,000,000,000+",
  "minInstalls": 1000000000,
  "contentRating": "Teen",
  "price": 0,
  "isFree": true,
  "inAppPurchases": "$8.00 - $500.00 per item",
  "url": "https://play.google.com/store/apps/details?id=com.openai.chatgpt&gl=us",
  "chartedAt": "2026-10-25T22:21:10Z",
  "previousRank": 2,
  "rankChange": 0,
  "newInChart": false
}
```

`appId` is the package name, stable across runs and countries: the key to join on. A chart
that could not be read comes back as an unbilled row saying which one and why.

## Tracking rank over time

A chart is a snapshot; the story is in how it moves. Schedule a daily run on Apify (or call
it from cron) and every row carries `chartedAt`, `previousRank`, `rankChange` (positive means
it climbed) and `newInChart`, so the dataset is a rank history with the deltas already worked
out: who is climbing, who is falling out, who just entered.

## FAQ

**Is there an official Google Play top charts API?**
No. Google publishes none. This reads the chart data the Play Store itself shows, so the
ranks are Google's own.

**How do I get trending apps on Google Play?**
Ask for `"charts": ["trending"]`: Google's own list of the apps rising fastest, up to 200 per
country and category. It is not a reshuffle of Top Free; in the US on 18 October 2026 the two
top 100s shared 7 apps.

**Can I get the developer's contact details?**
Turn on `includeDetails` and each row carries `developerEmail` and `developerWebsite`, as the
developer publishes them on Google Play.

**What does it cost?**
It is paid per chart row; unreadable charts are not charged. The current rate for your plan
is on the [Actor page](https://apify.com/glitchbound/google-play-charts-scraper).

**What about the iOS App Store?**
[App Store Top Charts Scraper](https://apify.com/glitchbound/app-charts-scraper) returns the
same row shape for Apple's charts, so the two join cleanly.

## Related

- [App Store Top Charts Scraper](https://apify.com/glitchbound/app-charts-scraper): iOS Top Free, Paid and Grossing by country.
- [App Store & Google Play Scraper](https://apify.com/glitchbound/app-store-scraper): one app's ratings, price and metadata in both stores.
- [App Store & Google Play Reviews Scraper](https://apify.com/glitchbound/app-reviews-scraper): every review for an app, both stores.
- [ASO Keyword Rank Tracker](https://apify.com/glitchbound/aso-keyword-rank-tracker): where an app ranks for a keyword in both stores.
- Write-up: [Google Play top charts API: top free, top grossing and trending apps in 130 countries](https://dev.to/glitchbound/google-play-top-charts-api-top-free-top-grossing-and-trending-apps-in-130-countries-31ac).

Questions or a chart that looks wrong? Open an issue here or on the Actor page.

## License

MIT
