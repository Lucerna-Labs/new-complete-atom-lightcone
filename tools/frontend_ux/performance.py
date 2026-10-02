"""Front-end performance: loading, layout stability, responsiveness (Core Web Vitals)."""

DOMAIN = "frontend-web-development"
SUBJECT = "frontend-web-development.performance"
SOURCES = ["web-dev-vitals", "mdn-web-docs"]

CONCEPTS = [
    ("lcp-slow", "Slow Largest Contentful Paint", "The largest visible image or text block appears later than 2.5 seconds after navigation starts.", ["slow lcp"]),
    ("cls-high", "High Cumulative Layout Shift", "Visible content moves unexpectedly while the page loads or updates, giving a layout shift score above 0.1.", ["layout shift"]),
    ("inp-slow", "Slow Interaction to Next Paint", "The page takes longer than 200 milliseconds to show visual feedback after a click, tap or key press.", ["slow inp"]),
    ("render-blocking-resources", "Render-blocking CSS and scripts", "Stylesheets and synchronous scripts in the document head that the browser must load before first rendering.", []),
    ("large-hero-image", "Large unoptimised hero image", "A high-resolution image in the first screen served without compression, modern formats or responsive sizes.", []),
    ("lazy-loaded-hero", "Lazy loading the main hero image", "Applying loading=lazy to the image that is the largest element in the first viewport.", []),
    ("preloading-key-resource", "Preloading the key resource", "Using fetchpriority=high or a preload hint for the LCP image or critical font.", []),
    ("slow-server-response", "Slow server response time", "A high time to first byte before any HTML arrives.", ["slow ttfb"]),
    ("images-without-dimensions", "Images without width and height", "Image or video elements without width/height attributes or an aspect-ratio rule.", []),
    ("reserved-space", "Reserved layout space", "Space held in advance for images, ads and embeds via dimensions, aspect-ratio or min-height.", []),
    ("late-injected-content", "Late-injected banners and ads", "Banners, ads or embeds inserted above existing content after it has rendered.", []),
    ("web-font-swap", "Web font swapping in", "A fallback font is replaced by a web font with different metrics after the text has rendered.", []),
    ("font-metric-override", "Font fallback metric matching", "Adjusting fallback fonts with size-adjust and ascent overrides to match the web font's metrics.", []),
    ("long-tasks", "Long main-thread tasks", "JavaScript tasks that run for more than 50 milliseconds without yielding the main thread.", []),
    ("large-js-bundle", "Large JavaScript bundle", "Hundreds of kilobytes of JavaScript downloaded, parsed and executed before the page becomes interactive.", []),
    ("code-splitting", "Code splitting and deferred loading", "Loading JavaScript per route or on demand instead of in one bundle.", []),
    ("yielding-main-thread", "Yielding the main thread", "Breaking work into small chunks with scheduling so input can be handled between them.", []),
    ("layout-thrashing", "Forced synchronous layout thrashing", "Reading layout properties right after writing styles in a loop, forcing repeated layout calculations.", []),
    ("dropped-frames", "Dropped animation frames", "Rendering misses the frame deadline, so scrolling and animations stutter.", ["jank"]),
    ("animating-layout-properties", "Animating layout properties", "Animating width, height, top or left, which forces layout on every frame.", []),
    ("compositor-animation", "Compositor-only animation", "Animating transform and opacity, which the compositor can do without layout or paint.", []),
    ("misclick-from-shift", "Mis-click caused by layout shift", "A user taps the wrong control because content moved just before the tap.", []),
    ("perceived-unresponsive", "Interface perceived as unresponsive", "Users believe the click did not register and click again or leave.", []),
    ("excessive-dom-size", "Excessively large DOM", "Pages with many thousands of DOM nodes, such as unvirtualised long lists.", []),
    ("list-virtualisation", "List virtualisation", "Rendering only the visible rows of a long list.", ["windowing"]),
]

RELATIONS = [
    ("blocking-lcp", "render-blocking-resources", "lcp-slow", "causes", "Render-blocking CSS and scripts cause slow Largest Contentful Paint by delaying first render.", "the resources are large or slow to fetch", ""),
    ("hero-lcp", "large-hero-image", "lcp-slow", "causes", "A large unoptimised hero image causes slow Largest Contentful Paint.", "the image is the largest element in the first viewport", ""),
    ("lazyhero-lcp", "lazy-loaded-hero", "lcp-slow", "causes", "Lazy loading the main hero image causes slow Largest Contentful Paint because the browser deprioritises it.", "the hero is visible on first load", ""),
    ("preload-lcp", "preloading-key-resource", "lcp-slow", "inhibits", "Preloading the key resource inhibits slow Largest Contentful Paint.", "the preloaded resource is actually the LCP element", "preloading the wrong resource competes for bandwidth"),
    ("ttfb-lcp", "slow-server-response", "lcp-slow", "causes", "Slow server response time causes slow Largest Contentful Paint, since nothing renders before HTML arrives.", "the page is server-rendered or needs the HTML first", ""),
    ("nodims-cls", "images-without-dimensions", "cls-high", "causes", "Images without width and height cause high Cumulative Layout Shift when they load and push content down.", "the image loads after surrounding text has rendered", ""),
    ("reserved-prevents-cls", "reserved-space", "cls-high", "prevents", "Reserved layout space prevents high Cumulative Layout Shift from late-loading media.", "the reserved size matches the final size", ""),
    ("injected-cls", "late-injected-content", "cls-high", "causes", "Late-injected banners and ads cause high Cumulative Layout Shift.", "they are inserted above content the user is viewing", "shifts within 500 ms of user input are excluded"),
    ("fontswap-cls", "web-font-swap", "cls-high", "causes", "Web font swapping in causes high Cumulative Layout Shift when metrics differ.", "the fallback and web font have different sizes", ""),
    ("metric-prevents", "font-metric-override", "web-font-swap", "inhibits", "Font fallback metric matching inhibits the layout effect of web font swapping in.", "the overrides are tuned to the web font", ""),
    ("cls-misclick", "cls-high", "misclick-from-shift", "causes", "High Cumulative Layout Shift causes a mis-click caused by layout shift.", "the shift happens while the user is about to tap", ""),
    ("longtasks-inp", "long-tasks", "inp-slow", "causes", "Long main-thread tasks cause slow Interaction to Next Paint by delaying input handling.", "the task is running when the user interacts", ""),
    ("bundle-longtasks", "large-js-bundle", "long-tasks", "causes", "A large JavaScript bundle causes long main-thread tasks during parse and execution.", "the bundle is evaluated on the main thread", ""),
    ("splitting-prevents", "code-splitting", "large-js-bundle", "prevents", "Code splitting and deferred loading prevent a large JavaScript bundle on initial load.", "routes and features are split at sensible boundaries", ""),
    ("yield-inp", "yielding-main-thread", "inp-slow", "inhibits", "Yielding the main thread inhibits slow Interaction to Next Paint.", "work is broken into chunks under about 50 ms", ""),
    ("thrash-longtasks", "layout-thrashing", "long-tasks", "causes", "Forced synchronous layout thrashing causes long main-thread tasks.", "reads and writes interleave in a loop", ""),
    ("thrash-frames", "layout-thrashing", "dropped-frames", "causes", "Forced synchronous layout thrashing causes dropped animation frames.", "it happens during scrolling or animation", ""),
    ("animlayout-frames", "animating-layout-properties", "dropped-frames", "causes", "Animating layout properties causes dropped animation frames.", "the animated element affects the layout of many others", ""),
    ("compositor-prevents", "compositor-animation", "dropped-frames", "inhibits", "Compositor-only animation inhibits dropped animation frames.", "the animation uses only transform and opacity", ""),
    ("inp-unresponsive", "inp-slow", "perceived-unresponsive", "causes", "Slow Interaction to Next Paint causes the interface to be perceived as unresponsive.", "no visual feedback appears within about 100 to 200 ms", ""),
    ("dom-longtasks", "excessive-dom-size", "long-tasks", "causes", "An excessively large DOM causes long main-thread tasks during style and layout.", "large parts of the DOM are updated together", ""),
    ("virtualise-prevents", "list-virtualisation", "excessive-dom-size", "prevents", "List virtualisation prevents an excessively large DOM for long lists.", "row heights are known or measured", ""),
    ("bundle-lcp", "large-js-bundle", "lcp-slow", "causes", "A large JavaScript bundle causes slow Largest Contentful Paint for client-rendered pages.", "content renders only after the JavaScript runs", ""),
]
