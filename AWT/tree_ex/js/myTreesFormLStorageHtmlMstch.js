/*
 * Created by Stefan Korecko, 2021
 */


/*
It is possible to use the .mjs extension for JavaScript modules. However, this may lead to some problems,
see the section "Aside — .mjs versus .js" at
https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide/Modules
 */

import DropdownMenuControl from "./dropdownMenuControl.js";
import OpinionsHandlerMustache from "./opinionsHandlerMustache.js";

window.drMenuCntrl = new DropdownMenuControl("menuIts", "menuTitle", "mnShow");
window.opnsHndlr = new OpinionsHandlerMustache("opnFrm","opinionsContainer","mTmplOneOpinion");
window.opnsHndlr.init();