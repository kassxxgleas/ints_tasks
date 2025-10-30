document.addEventListener('DOMContentLoaded', function() {
  const form = document.getElementById('opnFrm');

  if (form) {
    form.addEventListener('submit', function(event) {
      event.preventDefault();
      processOpnFrmData(event);
    });
  }
  displayStoredOpinions();
});


function processOpnFrmData(event) {
  event.preventDefault();
  const nameValue = document.getElementById('nameElm').value;
  const emailValue = document.getElementById('emailElm').value;
  const imageUrlValue = document.getElementById('imageUrlElm').value;
  const opinionValue = document.getElementById('opnElm').value;
  const keywordsValue = document.getElementById('keywordsElm').value;
  const willReturnValue = document.getElementById('willReturnElm').checked;

  const favoriteTeamElms = document.getElementsByName('favoriteTeam');
  let favoriteTeamValue = '';
  for (let i = 0; i < favoriteTeamElms.length; i++) {
    if (favoriteTeamElms[i].checked) {
      favoriteTeamValue = favoriteTeamElms[i].value;
      break;
    }
  }

  const newOpinion = {
    name: nameValue,
    email: emailValue,
    imageUrl: imageUrlValue,
    favoriteTeam: favoriteTeamValue,
    willReturn: willReturnValue,
    keywords: keywordsValue,
    opinion: opinionValue,
    timestamp: new Date().toISOString()
  };

  let opinions = [];
  const storedOpinions = localStorage.getItem('f1BlogComments');

  if (storedOpinions) {
    try {
      opinions = JSON.parse(storedOpinions);
    } catch (e) {
      console.error('Error in parsing data from localStorage:', e);
      opinions = [];
    }
  }

  opinions.push(newOpinion);
  localStorage.setItem('f1BlogComments', JSON.stringify(opinions));

  console.log('New opinion added:', newOpinion);
  console.log('Number of opinions in localStorage:', opinions.length);

  alert('Thank you for your opinion! Data saved.');

  document.getElementById('opnFrm').reset();
  displayStoredOpinions();
}


function displayStoredOpinions() {
  const storedOpinions = localStorage.getItem('f1BlogComments');
  if (storedOpinions) {
    try {
      const opinions = JSON.parse(storedOpinions);
      console.log('=== Saved opinions ===');
      console.log('Count of opinions:', opinions.length);
      opinions.forEach((opinion, index) => {
        console.log(`Opinion ${index + 1}:`, opinion);
      });
    } catch (e) {
      console.error('Error in displaying opinions:', e);
    }
  } else {
    console.log('No opinions yet');
  }
}

function clearAllOpinions() {
  localStorage.removeItem('f1BlogComments');
  console.log('All opinions deleteted from localStorage');
  displayStoredOpinions();
}