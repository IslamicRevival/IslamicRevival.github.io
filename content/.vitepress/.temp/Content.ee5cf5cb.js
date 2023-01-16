import { shallowRef, inject, computed, ref, reactive, markRaw, readonly, nextTick, defineComponent, onUpdated, h } from "vue";
const siteData = JSON.parse('{"lang":"en-US","title":"Islamic Revival","description":"Islamic Revival - AI & NLP framework for Islamic knowledge sharing & archiving","base":"/","head":[],"appearance":true,"themeConfig":{"logo":"/logo.svg","editLink":{"pattern":"https://github.com/IslamicRevival/IslamicRevival.github.io/edit/main/content/:path","text":"Edit this page on GitHub"},"socialLinks":[{"icon":"github","link":"https://github.com/IslamicRevival/IslamicRevival.github.io"},{"icon":"twitter","link":"https://twitter.com/"}],"footer":{"copyright":"As-salamu alaykum! Content by SirVival"},"nav":[{"text":"Articles","items":[{"text":"Add/edit content","link":"/articles/how-to-content"},{"text":"Writing guide","link":"/articles/writing-guide"},{"text":"Misunderstanding Ibada","link":"/articles/misunderstanding_ibada"}]},{"text":"Blog. Theology","link":"/blogging_theology/"},{"text":"Files","link":"/files/pdfs"},{"text":"Fiqh & Tafseer","link":"/massari/"},{"text":"Mohd. Hijab","link":"/hijab/"},{"text":"Sapience","link":"/sapience/"},{"text":"Thgt Advtr.","link":"/thought_adventure/"}],"sidebar":[{"text":"Articles","items":[{"text":"How To Content","link":"articles/how-to-content"},{"text":"Misunderstanding Ibada","link":"articles/misunderstanding_ibada"},{"text":"Writing Guide","link":"articles/writing-guide"}]},{"text":"Files","items":[{"text":"Pdfs","link":"files/pdfs"}]},{"text":"Massari","items":[{"text":"02 Establishing An Islamic State Is It An Obligation Fardh","link":"massari/02_-_Establishing_an_Islamic_State__Is_it_an_Obligation_(Fardh)"},{"text":"101 Tafseer Ul Quran Surah An Nisa With Professor Dr Muhammad AL MASSARI","link":"massari/101_-_Tafseer_ul_Quran__Surah_An_Nisa_with_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"102 Tafseer Ul Quran Surat An Nisa With Professor Dr Muhammad AL MASSARI","link":"massari/102_-_Tafseer_ul_Quran__Surat_An_Nisa_with_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"103 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/103_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"104 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/104_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"105 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/105_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"106 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/106_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"107 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/107_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"108 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/108_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"109 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/109_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"110 Tafseer Ul Quran Surat Al Ma Idah Professor Dr Muhammad AL MASSARI","link":"massari/110_Tafseer_ul_Quran_Surat_Al_Ma_idah_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"120 Tafseer Ul Quran Surat Al An Am Professor Dr Muhammad AL MASSARI","link":"massari/120_Tafseer_ul_Quran_Surat_Al-An_am_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"121 Tafseer Ul Quran Surat Al An Am Professor Dr Muhammad AL MASSARI","link":"massari/121_Tafseer_ul_Quran_Surat_Al-An_am_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"122 Tafseer Ul Quran Surat Al An Am Professor Dr Muhammad AL MASSARI","link":"massari/122_Tafseer_ul_Quran_Surat_Al-An_am_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"123 Tafseer Ul Quran Surat Al An Am Professor Dr Muhammad AL MASSARI","link":"massari/123_Tafseer_ul_Quran_Surat_Al-An_am_Professor_Dr__Muhammad_AL_MASSARI"},{"text":"Session 2","link":"massari/Session_2"}]}]},"locales":{},"langs":{},"scrollOffset":90,"cleanUrls":"with-subfolders"}');
const EXTERNAL_URL_RE = /^[a-z]+:/i;
const APPEARANCE_KEY = "vitepress-theme-appearance";
const inBrowser = typeof window !== "undefined";
const notFoundPageData = {
  relativePath: "",
  title: "404",
  description: "Not Found",
  headers: [],
  frontmatter: { sidebar: false, layout: "page" },
  lastUpdated: 0
};
function findMatchRoot(route, roots) {
  roots.sort((a, b) => {
    const levelDelta = b.split("/").length - a.split("/").length;
    if (levelDelta !== 0) {
      return levelDelta;
    } else {
      return b.length - a.length;
    }
  });
  for (const r of roots) {
    if (route.startsWith(r))
      return r;
  }
}
function resolveLocales(locales, route) {
  const localeRoot = findMatchRoot(route, Object.keys(locales));
  return localeRoot ? locales[localeRoot] : void 0;
}
function createLangDictionary(siteData2) {
  const { locales } = siteData2.themeConfig || {};
  const siteLocales = siteData2.locales;
  return locales && siteLocales ? Object.keys(locales).reduce((langs, path) => {
    langs[path] = {
      label: locales[path].label,
      lang: siteLocales[path].lang
    };
    return langs;
  }, {}) : {};
}
function resolveSiteDataByRoute(siteData2, route) {
  route = cleanRoute(siteData2, route);
  const localeData = resolveLocales(siteData2.locales || {}, route);
  const localeThemeConfig = resolveLocales(siteData2.themeConfig.locales || {}, route);
  return Object.assign({}, siteData2, localeData, {
    themeConfig: Object.assign({}, siteData2.themeConfig, localeThemeConfig, {
      locales: {}
    }),
    lang: (localeData || siteData2).lang,
    locales: {},
    langs: createLangDictionary(siteData2)
  });
}
function createTitle(siteData2, pageData) {
  var _a;
  const title = pageData.title || siteData2.title;
  const template = (_a = pageData.titleTemplate) != null ? _a : siteData2.titleTemplate;
  if (typeof template === "string" && template.includes(":title")) {
    return template.replace(/:title/g, title);
  }
  const templateString = createTitleTemplate(siteData2.title, template);
  return `${title}${templateString}`;
}
function createTitleTemplate(siteTitle, template) {
  if (template === false) {
    return "";
  }
  if (template === true || template === void 0) {
    return ` | ${siteTitle}`;
  }
  if (siteTitle === template) {
    return "";
  }
  return ` | ${template}`;
}
function cleanRoute(siteData2, route) {
  if (!inBrowser) {
    return route;
  }
  const base = siteData2.base;
  const baseWithoutSuffix = base.endsWith("/") ? base.slice(0, -1) : base;
  return route.slice(baseWithoutSuffix.length);
}
function hasTag(head, tag) {
  const [tagType, tagAttrs] = tag;
  if (tagType !== "meta")
    return false;
  const keyAttr = Object.entries(tagAttrs)[0];
  if (keyAttr == null)
    return false;
  return head.some(([type, attrs]) => type === tagType && attrs[keyAttr[0]] === keyAttr[1]);
}
function mergeHead(prev, curr) {
  return [...prev.filter((tagAttrs) => !hasTag(curr, tagAttrs)), ...curr];
}
const INVALID_CHAR_REGEX = /[\u0000-\u001F"#$&*+,:;<=>?[\]^`{|}\u007F]/g;
const DRIVE_LETTER_REGEX = /^[a-z]:/i;
function sanitizeFileName(name) {
  const match = DRIVE_LETTER_REGEX.exec(name);
  const driveLetter = match ? match[0] : "";
  return driveLetter + name.slice(driveLetter.length).replace(INVALID_CHAR_REGEX, "_").replace(/(^|\/)_+(?=[^/]*$)/, "$1");
}
function joinPath(base, path) {
  return `${base}${path}`.replace(/\/+/g, "/");
}
function withBase(path) {
  return EXTERNAL_URL_RE.test(path) ? path : joinPath(siteDataRef.value.base, path);
}
function pathToFile(path) {
  let pagePath = path.replace(/\.html$/, "");
  pagePath = decodeURIComponent(pagePath);
  if (pagePath.endsWith("/")) {
    pagePath += "index";
  }
  {
    if (inBrowser) {
      const base = "/";
      pagePath = sanitizeFileName(pagePath.slice(base.length).replace(/\//g, "_") || "index") + ".md";
      const pageHash = __VP_HASH_MAP__[pagePath.toLowerCase()];
      pagePath = `${base}assets/${pagePath}.${pageHash}.js`;
    } else {
      pagePath = `./${sanitizeFileName(pagePath.slice(1).replace(/\//g, "_"))}.md.js`;
    }
  }
  return pagePath;
}
const dataSymbol = Symbol();
const siteDataRef = shallowRef(siteData);
function initData(route) {
  const site = computed(() => resolveSiteDataByRoute(siteDataRef.value, route.path));
  return {
    site,
    theme: computed(() => site.value.themeConfig),
    page: computed(() => route.data),
    frontmatter: computed(() => route.data.frontmatter),
    lang: computed(() => site.value.lang),
    localePath: computed(() => {
      const { langs, lang } = site.value;
      const path = Object.keys(langs).find((langPath) => langs[langPath].lang === lang);
      return withBase(path || "/");
    }),
    title: computed(() => {
      return createTitle(site.value, route.data);
    }),
    description: computed(() => {
      return route.data.description || site.value.description;
    }),
    isDark: ref(false)
  };
}
function useData() {
  const data = inject(dataSymbol);
  if (!data) {
    throw new Error("vitepress data not properly injected in app");
  }
  return data;
}
const RouterSymbol = Symbol();
const fakeHost = `http://a.com`;
const getDefaultRoute = () => ({
  path: "/",
  component: null,
  data: notFoundPageData
});
function createRouter(loadPageModule, fallbackComponent) {
  const route = reactive(getDefaultRoute());
  const router = {
    route,
    go
  };
  async function go(href = inBrowser ? location.href : "/") {
    var _a, _b;
    await ((_a = router.onBeforeRouteChange) == null ? void 0 : _a.call(router, href));
    const url = new URL(href, fakeHost);
    if (siteDataRef.value.cleanUrls === "disabled") {
      if (!url.pathname.endsWith("/") && !url.pathname.endsWith(".html")) {
        url.pathname += ".html";
        href = url.pathname + url.search + url.hash;
      }
    }
    if (inBrowser) {
      history.replaceState({ scrollPosition: window.scrollY }, document.title);
      history.pushState(null, "", href);
    }
    await loadPage(href);
    await ((_b = router.onAfterRouteChanged) == null ? void 0 : _b.call(router, href));
  }
  let latestPendingPath = null;
  async function loadPage(href, scrollPosition = 0, isRetry = false) {
    const targetLoc = new URL(href, fakeHost);
    const pendingPath = latestPendingPath = targetLoc.pathname;
    try {
      let page = await loadPageModule(pendingPath);
      if (latestPendingPath === pendingPath) {
        latestPendingPath = null;
        const { default: comp, __pageData } = page;
        if (!comp) {
          throw new Error(`Invalid route component: ${comp}`);
        }
        route.path = inBrowser ? pendingPath : withBase(pendingPath);
        route.component = markRaw(comp);
        route.data = true ? markRaw(__pageData) : readonly(__pageData);
        if (inBrowser) {
          nextTick(() => {
            if (targetLoc.hash && !scrollPosition) {
              let target = null;
              try {
                target = document.querySelector(decodeURIComponent(targetLoc.hash));
              } catch (e) {
                console.warn(e);
              }
              if (target) {
                scrollTo(target, targetLoc.hash);
                return;
              }
            }
            window.scrollTo(0, scrollPosition);
          });
        }
      }
    } catch (err) {
      if (!/fetch/.test(err.message) && !/^\/404(\.html|\/)?$/.test(href)) {
        console.error(err);
      }
      if (!isRetry) {
        try {
          const res = await fetch(siteDataRef.value.base + "hashmap.json");
          window.__VP_HASH_MAP__ = await res.json();
          await loadPage(href, scrollPosition, true);
          return;
        } catch (e) {
        }
      }
      if (latestPendingPath === pendingPath) {
        latestPendingPath = null;
        route.path = inBrowser ? pendingPath : withBase(pendingPath);
        route.component = fallbackComponent ? markRaw(fallbackComponent) : null;
        route.data = notFoundPageData;
      }
    }
  }
  if (inBrowser) {
    window.addEventListener("click", (e) => {
      const button = e.target.closest("button");
      if (button)
        return;
      const link = e.target.closest("a");
      if (link && !link.closest(".vp-raw") && !link.download) {
        const { href, origin, pathname, hash, search, target } = link;
        const currentUrl = window.location;
        const extMatch = pathname.match(/\.\w+$/);
        if (!e.ctrlKey && !e.shiftKey && !e.altKey && !e.metaKey && target !== `_blank` && origin === currentUrl.origin && !(extMatch && extMatch[0] !== ".html")) {
          e.preventDefault();
          if (pathname === currentUrl.pathname && search === currentUrl.search) {
            if (hash && hash !== currentUrl.hash) {
              history.pushState(null, "", hash);
              window.dispatchEvent(new Event("hashchange"));
              scrollTo(link, hash, link.classList.contains("header-anchor"));
            }
          } else {
            go(href);
          }
        }
      }
    }, { capture: true });
    window.addEventListener("popstate", (e) => {
      loadPage(location.href, e.state && e.state.scrollPosition || 0);
    });
    window.addEventListener("hashchange", (e) => {
      e.preventDefault();
    });
  }
  return router;
}
function useRouter() {
  const router = inject(RouterSymbol);
  if (!router) {
    throw new Error("useRouter() is called without provider.");
  }
  return router;
}
function useRoute() {
  return useRouter().route;
}
function scrollTo(el, hash, smooth = false) {
  let target = null;
  try {
    target = el.classList.contains("header-anchor") ? el : document.querySelector(decodeURIComponent(hash));
  } catch (e) {
    console.warn(e);
  }
  if (target) {
    let offset = siteDataRef.value.scrollOffset;
    if (typeof offset === "string") {
      offset = document.querySelector(offset).getBoundingClientRect().bottom + 24;
    }
    const targetPadding = parseInt(window.getComputedStyle(target).paddingTop, 10);
    const targetTop = window.scrollY + target.getBoundingClientRect().top - offset + targetPadding;
    if (!smooth || Math.abs(targetTop - window.scrollY) > window.innerHeight) {
      window.scrollTo(0, targetTop);
    } else {
      window.scrollTo({
        left: 0,
        top: targetTop,
        behavior: "smooth"
      });
    }
  }
}
const Content = defineComponent({
  name: "VitePressContent",
  props: {
    onContentUpdated: Function
  },
  setup(props) {
    const route = useRoute();
    onUpdated(() => {
      var _a;
      (_a = props.onContentUpdated) == null ? void 0 : _a.call(props);
    });
    return () => h("div", { style: { position: "relative" } }, [
      route.component ? h(route.component) : null
    ]);
  }
});
export {
  APPEARANCE_KEY as A,
  Content as C,
  EXTERNAL_URL_RE as E,
  RouterSymbol as R,
  useRoute as a,
  initData as b,
  createTitle as c,
  dataSymbol as d,
  createRouter as e,
  inBrowser as i,
  mergeHead as m,
  pathToFile as p,
  siteDataRef as s,
  useData as u,
  withBase as w
};
