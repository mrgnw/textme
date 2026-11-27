# RCS device eligibility by region

Research cutoff November 27, 2026. [Chart-ready dataset](devices-by-region.json) · [Carrier rollout](adoption.md) · [Messaging app use](messaging.md)

**The share of active phones that can use Rich Communication Services (RCS) is unknown in every region.** Current operating-system data shows that most sampled phones clear the version thresholds on both platforms. Regional handset counts that combine operating system, messaging client and service eligibility are unavailable. That gap matters most where the stock Google Messages path is absent or Apple support varies by carrier.

## What a phone needs

- **iPhone.** Apple requires iOS 18 and a cellular plan from a carrier that supports iPhone RCS. The iPhone XS, XS Max, XR and second-generation SE clear the hardware floor. The iPhone X, 8, 8 Plus, first-generation SE and earlier models cannot run iOS 18. The XS, XS Max and XR can use basic RCS on iOS 18 with an eligible plan. Some carriers require later versions. [Apple RCS setup](https://support.apple.com/en-us/122195) · [iOS 18 compatibility](https://support.apple.com/en-is/104985) · [Apple security releases](https://support.apple.com/en-us/100100)
- **Google Messages.** Google lists Android 5.0 as the RCS troubleshooting floor and Android 7.0 as the floor for supported Google Play services. One November 2026 Google Messages package lists Android 8.0 as its install minimum. The public Play listing gives no universal minimum app build. For the supported route, use a current Google Messages build as the default texting app, current Play services, an eligible verified number and an internet connection. Google or the carrier provides service. [Google troubleshooting](https://support.google.com/messages/answer/9363493?hl=en) · [Play services](https://support.google.com/googleplay/answer/9037938?hl=en) · [Google Play listing](https://play.google.com/store/apps/details?id=com.google.android.apps.messaging) · [Mirrored package metadata](https://www.apkmirror.com/apk/google-inc/messenger-google-inc/google-messages-20261106_00_rc06-release/google-messages-messages-android_20261106_00_rc06-phone_dynamic-3-android-apk-download/) · [Google RCS FAQ](https://support.google.com/messages/answer/9487020?hl=en)
- **Samsung Messages.** Samsung ended support in the United States starting July 6, 2026, on Galaxy devices running Android 12 or later. It exempts Android 11 and earlier from this shutdown. Google documents RCS in Samsung Messages where supported and confirms that Google Messages is the default on selected Galaxy models. [Samsung scope](https://www.samsung.com/us/apps/samsung-messages/) · [Samsung cutoff](https://www.samsung.com/us/support/answer/ANS10001926/) · [Google on Samsung RCS](https://support.google.com/messages/answer/9592174?hl=en) · [Google Messages defaults](https://support.google.com/messages/answer/10324785?hl=en-GB)
- **Huawei, mainland China and low-cost phones.** Huawei says the Mate 30 series and later covered models shipped without Google Mobile Services. Huawei also documents a separate operator-provisioned RCS service in China. Carrier and firmware details matter for locally sourced phones. Android Go supports the Play Store, with app and carrier eligibility still model-specific. KaiOS and basic feature phones fall outside the Apple and Google Messages paths. No KaiOS consumer client was verified in the checked documentation. [Huawei on Google services](https://consumer.huawei.com/cn/support/content/zh-cn15841714/) · [Huawei on its RCS service](https://consumer.huawei.com/cn/support/content/zh-cn15947055/) · [Android Go](https://developer.android.com/guide/topics/androidgo/develop) · [KaiOS](https://developer.kaiostech.com/)

## Operating systems in use

October 2026 is the latest complete month at the research cutoff. The dataset contains **14,206 country and territory version rows** from StatCounter’s mobile CSV exports. Each share uses page views **within the named operating system**. The seven original world and regional charts and the 26-market threshold series use their original snapshots. The separate World Bank ranking multiplies the 2024 adult population by the share whose main phone was a smartphone. [StatCounter Global Stats methodology and CC BY-SA 3.0 terms](https://gs.statcounter.com/faq) · [World Bank Global Findex](https://www.worldbank.org/en/publication/globalfindex/download-data)

|October 2026 coverage|ISO countries and territories|
|-|-|
|Checked|249|
|Published iOS version data|242|
|Published Android version data|243|
|Verified national smartphone base|9|

Both exports were empty for Bouvet Island, Cocos (Keeling) Islands, Christmas Island, Western Sahara, Heard Island and McDonald Islands, and the French Southern Territories. Norfolk Island published Android data only. All 485 populated country and territory exports summed within two percentage points of 100%. The script preserves the source labels and rounded values, including `Other`, and flags any totals outside that range. StatCounter’s country codes are uppercase. Its lowercase codes can identify regions, such as `NA` for Namibia and `na` for North America. [iOS version exports](https://gs.statcounter.com/ios-version-market-share/mobile/worldwide) · [Android version exports](https://gs.statcounter.com/android-version-market-share/mobile/worldwide)

From the repository root, the refresh script uses Python 3.14, waits at least 600 milliseconds between requests, and caches raw exports under `analysis/cache/`. It defaults to the previous complete calendar month. `--offline --check` validates a snapshot against the cached exports.

```sh
uv run analysis/refresh_rcs_devices.py --month 2026-10
```

|Geography|iOS 18+|iOS 26+|iOS below 18|Android 8+|
|-|-|-|-|-|
|Global|94.16%|78.18%|5.67%|99.37%|
|North America|96.64%|81.44%|3.24%|99.35%|
|Europe|96.02%|81.43%|3.85%|99.30%|
|Asia|90.33%|72.37%|9.53%|99.39%|
|South America|96.29%|82.98%|3.64%|99.34%|
|Africa|89.79%|72.58%|10.09%|98.89%|
|Oceania|95.82%|79.80%|4.13%|99.34%|

Apple’s June 7, 2026, App Store sample had 79% on iOS 26, 14% on iOS 18 and 7% on earlier versions. Google’s global Android Studio file, updated October 1, 2026, reports 25.4% on Android 16, 0.9% on Android 17 and a combined 99.0% on listed Android 8+ releases. These samples cover different device populations from the web traffic data. [Apple App Store distribution](https://developer.apple.com/support/app-store/) · [Google Android Studio distribution](https://dl.google.com/android/studio/metadata/distributions.json)

## Device compatibility and version names

The model table covers iOS 16, 17, 18, 26 and 27. Apple moved directly from iOS 18 to iOS 26 for major releases, so versions 19 through 25 have null compatibility entries. The table lists which older iPhones each release excludes and the newest version those devices support. Basic iPhone RCS requires iOS 18 or later and a compatible carrier plan. [Apple compatibility for iOS 16](https://support.apple.com/en-au/103267) · [iOS 17 availability](https://www.apple.com/newsroom/2023/09/ios-17-is-available-today/) · [iOS 18 compatibility](https://support.apple.com/en-is/104985) · [iOS 26 compatibility](https://support.apple.com/en-us/123705) · [iOS 27 compatibility](https://support.apple.com/guide/iphone/iphone-models-compatible-with-ios-27-iphe3fa5df43/27/ios/27) · [Apple RCS requirements](https://support.apple.com/en-us/122195)

The Android table maps platform names to application programming interface (API) levels. Android 7.0 Nougat is API level 24, Google’s support floor for Play services. Google Messages lists Android 5.0, API level 21, as its RCS troubleshooting floor. Google’s public help and Play listing give no universal current app install minimum. [Android version mapping](https://developer.android.com/guide/topics/manifest/uses-sdk-element#ApiLevels) · [Play services minimum](https://support.google.com/googleplay/answer/9037938) · [Google Messages troubleshooting](https://support.google.com/messages/answer/9363493) · [Google Play listing](https://play.google.com/store/apps/details?id=com.google.android.apps.messaging)

## Smartphone base estimates

The nine verified bases cover Brazil, China, India, Kenya, South Korea, Tanzania, Uganda, Vietnam and South Africa. The dataset includes 609 version estimates for these markets and omits estimates for the remaining 240 geographies. The base rows keep the source date and unit. Where a source counts smartphone subscriptions, the estimate has the same subscription denominator.

For each published version, multiply the sourced smartphone base by StatCounter’s share for that platform across sampled mobile page views, then by the version’s share within that platform. The platform share prevents applying the full national base separately to iOS and to Android. The result uses October web traffic as a proxy for the device mix and keeps the base at its published vintage. The formula skips unclassified versions and leaves other operating systems outside the estimate. [StatCounter data methodology](https://gs.statcounter.com/faq)

## Handset mix and age

- In 2024 the GSMA estimated that smartphones accounted for 80% of mobile connections globally, 86% in North America, 82% in Europe, 81% in Latin America, 81% in Asia Pacific excluding Greater China, and 54% in Sub-Saharan Africa. A separate GSMA series counts devices used to access mobile internet. Feature phones made up 7% of this group globally, 2% in North America and 25% in Sub-Saharan Africa. The dataset preserves each denominator and regional boundary, including gaps for South America, all of Asia, all of Africa and Oceania. [GSMA Mobile Economy](https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2025/02/030325-The-Mobile-Economy-2025.pdf) · [GSMA feature-phone series, figure 14](https://www.gsma.com/somic/wp-content/uploads/2025/09/The-State-of-Mobile-Internet-Connectivity-2025-Trends-in-Mobile-Internet-Connectivity.pdf#page=30)
- Counterpoint estimated the global replacement cycle for new smartphones approached four years in 2025. The GSMA’s May 2026 factsheet cites around three and a half years of global phone holding time. A US survey in August 2026 found respondents had owned their current phones for about 24 months and reported upgrading every 32 months. It also found that 9.37% of surveyed iPhone owners reported an iPhone 11 or earlier model. That last measure dates model generations. Comparable regional means and shares of active handsets over four or five years old are unknown. Counterpoint’s newer regional report and the detailed Consumer Intelligence Research Partners chart are paywalled and unverified. [Counterpoint public tracker summary](https://counterpointresearch.com/q1-2026-report.pdf/insights/Active-Installed-Base-8-Smartphone-OEMs-Top-200-mn-Nearly-1-in-4-is-an-iPhone) · [GSMA circularity factsheet](https://www.gsma.com/solutions-and-impact/connectivity-for-good/external-affairs/wp-content/uploads/2026/06/Mobile-Device-Circularity-Factsheet.pdf) · [US phone survey](https://www.reviews.org/mobile/how-long-americans-keep-phones/) · [CIRP public excerpt](https://cirpapple.substack.com/p/the-shrinking-middle-in-iphone-age)

## How to estimate capability

For the two documented smartphone paths, multiply the share of active handsets that are smartphones by the sum, across smartphone platforms, of each platform’s smartphone share times its joint share with a compatible operating system, compatible client and available provider. A separately verified feature-phone path would add its own share. Use probabilities for the same geography, date and active handset denominator. The JSON records the formula, missing inputs and available version proxies.

The GSMA smartphone connection shares above provide historical ceilings for the documented Apple and Google paths on the **connection** denominator. For example, the global 2024 ceiling is 80% because smartphones account for 80% of connections in that source. No matched handset denominator or regional default-app and client availability data supported a current capability percentage. The GSMA’s 2026 global estimate of approximately six billion capable devices omits an auditable all-handset denominator. Google’s older count measures monthly Google Messages users with RCS enabled. The carrier evidence in [adoption.md](adoption.md) and business reach in [messaging.md](messaging.md) answer different questions. [GSMA handset reach disclosure](https://www.gsmaservices.com/service-type/network/how-operators-can-leverage-the-billion-dollar-cross-platform-rcs-opportunity-with-gsma-entitlements/) · [Google enabled-user disclosure](https://blog.google/products-and-platforms/platforms/android/7-new-messages-features/)
