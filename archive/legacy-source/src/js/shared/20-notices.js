/* ===== UNIVERSAL DISMISSIBLE CRITERION NOTICES v1.7.0 ===== */
(function(){
  "use strict";
  const platform=typeof root_element!=="undefined"
    ?root_element.querySelector("#uccIntelligencePlatform")
    :document.querySelector("#uccIntelligencePlatform");
  if(!platform||platform.dataset.criterionNoticesReady==="1")return;
  platform.dataset.criterionNoticesReady="1";

  platform.querySelectorAll("[data-notice-dismiss]").forEach(button=>{
    button.addEventListener("click",()=>{
      const notice=button.closest(".ucc-criterion-notice");
      if(!notice)return;
      notice.dataset.dismissed="1";
      notice.hidden=true;
    });
  });
})();

