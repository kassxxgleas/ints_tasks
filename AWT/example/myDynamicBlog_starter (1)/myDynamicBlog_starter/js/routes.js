import Mustache from "./mustache.js";
import processOpnFrmData from "./addOpinion.js";

export default[
    {
        hash:"welcome",
        target:"router-view",
        getTemplate: (targetElm) => {
            document.getElementById(targetElm).innerHTML = "";
            document.getElementById("hero-container").innerHTML = document.getElementById("template-hero").innerHTML;
            document.getElementById(targetElm).innerHTML = document.getElementById("template-welcome").innerHTML;
        }
    },
    {
        hash:"articles",
        target:"router-view",
          getTemplate: (targetElm, offset, limit) => {  // ← Добавлены параметры
            document.getElementById(targetElm).innerHTML = "";
            document.getElementById("hero-container").innerHTML = "";
            const offsetNum = parseInt(offset) || 0;
            const limitNum = parseInt(limit) || 20;
            fetchAndDisplayArticles(targetElm, offsetNum, limitNum);
        }
    },
    {
        hash:"opinions",
        target:"router-view",
        getTemplate: (targetElm) => {
            document.getElementById(targetElm).innerHTML = "";
            document.getElementById("hero-container").innerHTML = "";
            createHtml4opinions(targetElm);
    }
    },
    {
        hash:"addOpinion",
        target:"router-view",
        getTemplate: (targetElm) =>{
            document.getElementById(targetElm).innerHTML = "";
            document.getElementById("hero-container").innerHTML = "";
            document.getElementById(targetElm).innerHTML = document.getElementById("template-addOpinion").innerHTML;
            document.getElementById("opnFrm").onsubmit=processOpnFrmData;
        }
    }            
];

function createHtml4opinions(targetElm){
 let opinions = [];
  if (localStorage.myF1Comments) {
    opinions = JSON.parse(localStorage.myF1Comments);
  }
  const opinionsWithFormattedData = opinions.map(opinion => {
    const createdDate = new Date(opinion.created);
    return {
      name: opinion.name || '',
      email: opinion.email || '',
      imageUrl: opinion.imageUrl || '',
      imageUrlExists: opinion.imageUrl && opinion.imageUrl.trim() !== '',
      favoriteTeamDisplay: opinion.favoriteTeam || 'Not specified',
      keywordsDisplay: opinion.keywords || 'Not specified',
      comment: opinion.opinion || '',
      willReturnMessage: opinion.willReturn 
        ? "I will return to this page." 
        : "Sorry, one visit was enough.",
      createdDate: `${createdDate.getDate()}.${createdDate.getMonth() + 1}.${createdDate.getFullYear()} ${createdDate.getHours()}:${String(createdDate.getMinutes()).padStart(2, '0')}`
    };
  });

  const template = document.getElementById("template-opinions").innerHTML;
  document.getElementById(targetElm).innerHTML = Mustache.render(template, opinionsWithFormattedData);
}       

function fetchAndDisplayArticles(targetElm, offset, limit) {
  const url = `https://wt.kpi.fei.tuke.sk/api/article?offset=${offset}&max=${limit}`;
  
  function reqListener() {
    if (this.status == 200) {
      const response = JSON.parse(this.responseText);
      const articles = response.articles;
      const meta = response.meta;
      
      const templateData = {
        articles: articles,
        pagination: {
          showPrevious: offset > 0,
          previousUrl: `#articles/${Math.max(0, offset - limit)}/${limit}`,
          showNext: (offset + articles.length) < meta.totalCount,
          nextUrl: `#articles/${offset + limit}/${limit}`,
          currentPage: Math.floor(offset / limit) + 1,
          totalPages: Math.ceil(meta.totalCount / limit),
          showing: `${offset + 1}-${offset + articles.length}`,
          total: meta.totalCount
        }
      };
      
      document.getElementById(targetElm).innerHTML = Mustache.render(
        document.getElementById("template-articles").innerHTML,
        templateData
      );
    } else {
      alert("Došlo k chybe: " + this.statusText);
    }
  }

  var ajax = new XMLHttpRequest();
  ajax.addEventListener("load", reqListener);
  ajax.open("GET", url, true);
  ajax.send();
}