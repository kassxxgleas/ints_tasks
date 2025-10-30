export default class OpinionsHandler {
  constructor(opinionsFormElmId, opinionsListElmId) {
    this.opinions = [];
    this.opinionsElm = document.getElementById(opinionsListElmId);
    this.opinionsFrmElm = document.getElementById(opinionsFormElmId);
  }

  init() {
    if (localStorage.f1BlogComments) {
      this.opinions = JSON.parse(localStorage.f1BlogComments);
    }
    this.opinionsElm.innerHTML = this.opinionArray2html(this.opinions);
    this.opinionsFrmElm.addEventListener("submit", event => this.processOpnFrmData(event));
  }

  processOpnFrmData(event) {
    event.preventDefault();
    const nopName = this.opinionsFrmElm.elements["nameElm"].value.trim();
    const nopEmail = this.opinionsFrmElm.elements["emailElm"].value.trim();
    const nopImageUrl = this.opinionsFrmElm.elements["imageUrlElm"].value.trim();
    const nopOpinion = this.opinionsFrmElm.elements["opnElm"].value.trim();
    const nopKeywords = this.opinionsFrmElm.elements["keywordsElm"].value.trim();
    const nopWillReturn = this.opinionsFrmElm.elements["willReturnElm"].checked;

    const favoriteTeamElms = this.opinionsFrmElm.elements["favoriteTeam"];
    let nopFavoriteTeam = "";
    for (let i = 0; i < favoriteTeamElms.length; i++) {
      if (favoriteTeamElms[i].checked) {
        nopFavoriteTeam = favoriteTeamElms[i].value;
        break;
      }
    }

    if (nopName === "" || nopEmail === "" || nopOpinion === "") {
      window.alert("Please, enter your name, email and opinion");
      return;
    }

    const newOpinion = {
      name: nopName,
      email: nopEmail,
      imageUrl: nopImageUrl,
      favoriteTeam: nopFavoriteTeam,
      keywords: nopKeywords,
      opinion: nopOpinion,
      willReturn: nopWillReturn,
      timestamp: new Date().toISOString()
    };
    console.log("New opinion:\n " + JSON.stringify(newOpinion));

    this.opinions.push(newOpinion);
    localStorage.f1BlogComments = JSON.stringify(this.opinions);
    this.opinionsElm.innerHTML += this.opinion2html(newOpinion);
    this.opinionsFrmElm.reset();
  }

  opinion2html(opinion) {
    const opinionTemplate = `
      <section>
        <h3>${opinion.name} <i>(${(new Date(opinion.timestamp)).toDateString()})</i></h3>
        <p><b>Email:</b> ${opinion.email ? opinion.email : ''}</p>
        ${opinion.imageUrl ? `<img src="${opinion.imageUrl}" alt="Avatar image" style="max-width:100px; border-radius:5px;">` : ''}
        <p><b>Favorite Team:</b> ${opinion.favoriteTeam ? opinion.favoriteTeam : 'Not specified'}</p>
        <p><b>Keywords:</b> ${opinion.keywords ? opinion.keywords : 'Not specified'}</p>
        <p><b>Comment:</b> ${opinion.opinion ? opinion.opinion : ''}</p>
        <p>${opinion.willReturn ? "I will return to this page." : "Sorry, one visit was enough."}</p>
      </section>
    `;
    return opinionTemplate;
  }

  opinionArray2html(sourceData) {
    let htmlWithOpinions = "";
    for (const opn of sourceData) {
      htmlWithOpinions += this.opinion2html(opn);
    }
    return htmlWithOpinions;
  }
}