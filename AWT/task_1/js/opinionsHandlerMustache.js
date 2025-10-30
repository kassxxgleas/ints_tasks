import OpinionsHandler from "./opinionsHandler.js";
import Mustache from "./mustache.js";

export default class OpinionsHandlerMustache extends OpinionsHandler {
  constructor(opinionsFormElmId, opinionsListElmId, templateElmId) {
    super(opinionsFormElmId, opinionsListElmId);
    this.mustacheTemplate = document.getElementById(templateElmId).innerHTML;
  }

  opinion2html(opinion) {
    opinion.timestampDate = (new Date(opinion.timestamp)).toDateString();
    opinion.willReturnMessage = opinion.willReturn 
      ? "I will return to this page." 
      : "Sorry, one visit was enough.";
    
    opinion.favoriteTeamDisplay = opinion.favoriteTeam || "Not specified";
    opinion.keywordsDisplay = opinion.keywords || "Not specified";
    opinion.imageUrlExists = opinion.imageUrl ? true : false;
    
    const htmlWOp = Mustache.render(this.mustacheTemplate, opinion);
    
    delete opinion.timestampDate;
    delete opinion.willReturnMessage;
    delete opinion.favoriteTeamDisplay;
    delete opinion.keywordsDisplay;
    delete opinion.imageUrlExists;
    
    return htmlWOp;
  }
}