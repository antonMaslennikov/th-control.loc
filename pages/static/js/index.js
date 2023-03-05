const initDefaultModule = module => module.default.init();

const routes = {
  log: () => {
    import("/static/js/log.js");
  }
};

const rootDomElementSelector = "html";
const PAGE_CLASS_PREFIX = "page--";

document.addEventListener("DOMContentLoaded", () => {
  const pageIndicator = document
    .querySelector(rootDomElementSelector)
    .className
    .split(" ")
    .find(cssClass => cssClass.startsWith(PAGE_CLASS_PREFIX));

  const pageName = pageIndicator && pageIndicator.slice(PAGE_CLASS_PREFIX.length);

  pageName && routes[pageName]();
});