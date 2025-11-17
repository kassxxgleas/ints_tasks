export default function processOpnFrmData(event) {
  event.preventDefault();

  const nopName = document.getElementById("nameElm").value.trim();
  const nopEmail = document.getElementById("emailElm").value.trim();
  const nopImageUrl = document.getElementById("imageElm").value.trim();
  const nopFavoriteTeam = document.querySelector('input[name="favoriteTeam"]:checked')?.value || '';
  const nopKeywords = document.getElementById("keywordsElm").value.trim();
  const nopOpn = document.getElementById("opnElm").value.trim();
  const nopWillReturn = document.getElementById("willReturnElm").checked;

  if (nopName === "" || nopOpn === "" || nopEmail === "") {
    window.alert("Please, enter your name, email and opinion");
    return;
  }

  const newOpinion = {
    name: nopName,
    email: nopEmail,
    imageUrl: nopImageUrl,
    favoriteTeam: nopFavoriteTeam,
    keywords: nopKeywords,
    opinion: nopOpn,
    willReturn: nopWillReturn,
    created: new Date()
  };

  let opinions = [];
  if (localStorage.myF1Comments) {
    opinions = JSON.parse(localStorage.myF1Comments);
  }

  opinions.push(newOpinion);
  localStorage.myF1Comments = JSON.stringify(opinions);

  window.location.hash = "opinions";
}